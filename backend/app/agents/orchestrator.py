"""Campaign orchestrator for coordinating the 3 Vectra AI agents."""

from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

from app.agents.prospector.agent import ProspectorAgent
from app.agents.bant.agent import BANTAgent
from app.agents.scheduler.agent import SchedulerAgent
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus
from app.services.analytics_service import AnalyticsService, AnalyticsEvent
from app.core.logging import get_logger

logger = get_logger(__name__)


class CampaignOrchestrator:
    """
    Orchestrates the 3 Vectra AI agents for a complete campaign flow.

    Flow:
    1. Prospector Agent: Find prospects based on criteria
    2. BANT Agent: Qualify each prospect (score >= 60)
    3. Scheduler Agent: Generate emails for qualified prospects
    """

    def __init__(
        self,
        db: Session,
        organization_id: UUID,
        agent_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize campaign orchestrator.

        Args:
            db: Database session
            organization_id: Organization ID for multi-tenant isolation
            agent_config: Configuration for agents (optional)
        """
        self.db = db
        self.organization_id = organization_id
        self.agent_config = agent_config or {}

        # Initialize agents
        self.prospector = ProspectorAgent(config=agent_config, db=db)
        self.bant = BANTAgent(config=agent_config, db=db)
        self.scheduler = SchedulerAgent(config=agent_config, db=db)

        # Analytics service for tracking
        self.analytics = AnalyticsService(db)

        self.logger = logger

    async def run_campaign(self, campaign_id: UUID) -> Dict[str, Any]:
        """
        Run complete campaign workflow.

        Args:
            campaign_id: Campaign ID to execute

        Returns:
            Dictionary with execution results and metrics
        """
        try:
            # Get campaign
            campaign = self.db.query(Campaign).filter(
                Campaign.id == campaign_id,
                Campaign.organization_id == self.organization_id
            ).first()

            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")

            # Update campaign status
            campaign.status = CampaignStatus.RUNNING
            campaign.started_at = datetime.utcnow()
            self.db.commit()

            self.logger.info(f"Starting campaign {campaign_id}: {campaign.name}")

            # Track campaign start event
            await self.analytics.track_event(
                organization_id=self.organization_id,
                event_type=AnalyticsEvent.CAMPAIGN_STARTED,
                properties={"campaign_id": str(campaign_id), "campaign_name": campaign.name}
            )

            # Step 1: Prospection
            prospects_result = await self._run_prospection(campaign)
            if not prospects_result["success"]:
                raise Exception(f"Prospection failed: {prospects_result.get('error')}")

            prospects = prospects_result["data"]["prospects"]
            self.logger.info(f"Found {len(prospects)} prospects")

            # Track prospection event
            await self.analytics.track_event(
                organization_id=self.organization_id,
                event_type=AnalyticsEvent.LEADS_IMPORTED,
                properties={"campaign_id": str(campaign_id), "leads_count": len(prospects)}
            )

            # Step 2: BANT Qualification
            qualified_leads = await self._run_bant_qualification(campaign, prospects)
            self.logger.info(f"Qualified {len(qualified_leads)} out of {len(prospects)} prospects")

            # Step 3: Email Generation
            emails_generated = await self._run_email_generation(campaign, qualified_leads)
            self.logger.info(f"Generated {len(emails_generated)} emails")

            # Update campaign status
            campaign.status = CampaignStatus.COMPLETED
            campaign.completed_at = datetime.utcnow()
            self.db.commit()

            # Track campaign completion
            await self.analytics.track_event(
                organization_id=self.organization_id,
                event_type=AnalyticsEvent.CAMPAIGN_COMPLETED,
                properties={
                    "campaign_id": str(campaign_id),
                    "prospects_found": len(prospects),
                    "leads_qualified": len(qualified_leads),
                    "emails_generated": len(emails_generated)
                }
            )

            result = {
                "campaign_id": str(campaign_id),
                "status": "completed",
                "prospects_found": len(prospects),
                "leads_qualified": len(qualified_leads),
                "qualification_rate": round(len(qualified_leads) / len(prospects) * 100, 2) if prospects else 0,
                "emails_generated": len(emails_generated),
                "execution_time": (datetime.utcnow() - campaign.started_at).total_seconds() if campaign.started_at else 0
            }

            self.logger.info(f"Campaign {campaign_id} completed successfully: {result}")
            return {"success": True, "data": result}

        except Exception as e:
            self.logger.error(f"Campaign execution failed: {e}", exc_info=True)

            # Update campaign status to failed
            try:
                campaign = self.db.query(Campaign).filter(Campaign.id == campaign_id).first()
                if campaign:
                    campaign.status = CampaignStatus.FAILED
                    self.db.commit()
            except Exception as db_error:
                self.logger.error(f"Failed to update campaign status: {db_error}")

            return {"success": False, "error": str(e)}

    async def _run_prospection(self, campaign: Campaign) -> Dict[str, Any]:
        """Run prospection phase using Prospector agent."""
        try:
            # Prepare input data for prospector
            target_criteria = campaign.target_criteria or {}

            input_data = {
                "campaign_id": str(campaign.id),
                "organization_id": str(self.organization_id),
                "job_titles": target_criteria.get("job_titles", []),
                "industries": target_criteria.get("industries", []),
                "company_sizes": target_criteria.get("company_sizes", []),
                "locations": target_criteria.get("locations", []),
                "limit": target_criteria.get("limit", 50),
                "target_criteria": target_criteria
            }

            # Execute prospector agent
            result = await self.prospector.execute(input_data)

            if result["success"]:
                # Save prospects as leads in database
                prospects = result["data"]["prospects"]
                for prospect_data in prospects:
                    lead = Lead(
                        campaign_id=campaign.id,
                        email=prospect_data.get("email"),
                        first_name=prospect_data.get("first_name"),
                        last_name=prospect_data.get("last_name"),
                        company_name=prospect_data.get("company_name"),
                        job_title=prospect_data.get("job_title"),
                        linkedin_url=prospect_data.get("linkedin_url"),
                        company_size=prospect_data.get("company_size"),
                        status=LeadStatus.PROSPECTED,
                        enrichment_data=prospect_data.get("enrichment_data", {}),
                        firmographic_score=prospect_data.get("firmographic_score", 0)
                    )
                    self.db.add(lead)

                self.db.commit()
                self.logger.info(f"Saved {len(prospects)} prospects to database")

            return result

        except Exception as e:
            self.logger.error(f"Prospection phase failed: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def _run_bant_qualification(self, campaign: Campaign, prospects: List[Dict]) -> List[Lead]:
        """Run BANT qualification phase using BANT agent."""
        qualified_leads = []

        try:
            # Get leads from database (just created in prospection)
            leads = self.db.query(Lead).filter(
                Lead.campaign_id == campaign.id,
                Lead.status == LeadStatus.PROSPECTED
            ).all()

            for lead in leads:
                try:
                    # Prepare input data for BANT agent
                    lead_data = {
                        "email": lead.email,
                        "job_title": lead.job_title,
                        "company_name": lead.company_name,
                        "company_size": lead.company_size,
                        "linkedin_url": lead.linkedin_url,
                        "enrichment_data": lead.enrichment_data or {}
                    }

                    input_data = {
                        "lead_id": str(lead.id),
                        "lead_data": lead_data,
                        "campaign": {
                            "product_description": campaign.description or "Vectra AI agents for B2B sales automation",
                            "bant_threshold": 60
                        }
                    }

                    # Execute BANT agent
                    result = await self.bant.execute(input_data)

                    if result["success"] and result["data"]["qualified"]:
                        qualified_leads.append(lead)

                        # Track qualification event
                        await self.analytics.track_event(
                            organization_id=self.organization_id,
                            event_type=AnalyticsEvent.LEAD_QUALIFIED,
                            properties={
                                "lead_id": str(lead.id),
                                "bant_score": result["data"]["bant_score"],
                                "campaign_id": str(campaign.id)
                            }
                        )

                except Exception as e:
                    self.logger.error(f"BANT qualification failed for lead {lead.id}: {e}")
                    continue

            return qualified_leads

        except Exception as e:
            self.logger.error(f"BANT qualification phase failed: {e}", exc_info=True)
            return []

    async def _run_email_generation(self, campaign: Campaign, qualified_leads: List[Lead]) -> List[Dict]:
        """Run email generation phase using Scheduler agent."""
        emails_generated = []

        try:
            for lead in qualified_leads:
                try:
                    # Prepare input data for Scheduler agent
                    lead_data = {
                        "email": lead.email,
                        "first_name": lead.first_name,
                        "last_name": lead.last_name,
                        "company_name": lead.company_name,
                        "job_title": lead.job_title
                    }

                    input_data = {
                        "lead_id": str(lead.id),
                        "lead_data": lead_data,
                        "campaign": {
                            "name": campaign.name,
                            "description": campaign.description,
                            "product_description": "Vectra AI agents for B2B sales automation"
                        },
                        "send_email": False  # Only generate, don't send automatically
                    }

                    # Execute Scheduler agent
                    result = await self.scheduler.execute(input_data)

                    if result["success"]:
                        emails_generated.append(result["data"])

                        # Track email generation event
                        await self.analytics.track_event(
                            organization_id=self.organization_id,
                            event_type=AnalyticsEvent.EMAIL_GENERATED,
                            properties={
                                "lead_id": str(lead.id),
                                "email_id": result["data"].get("email_id"),
                                "campaign_id": str(campaign.id)
                            }
                        )

                except Exception as e:
                    self.logger.error(f"Email generation failed for lead {lead.id}: {e}")
                    continue

            return emails_generated

        except Exception as e:
            self.logger.error(f"Email generation phase failed: {e}", exc_info=True)
            return []

    async def get_campaign_progress(self, campaign_id: UUID) -> Dict[str, Any]:
        """Get current progress of a running campaign.

        Args:
            campaign_id: Campaign ID to check

        Returns:
            Progress information dictionary
        """
        try:
            campaign = self.db.query(Campaign).filter(
                Campaign.id == campaign_id,
                Campaign.organization_id == self.organization_id
            ).first()

            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")

            # Count leads by status
            leads = self.db.query(Lead).filter(Lead.campaign_id == campaign_id).all()

            status_counts = {}
            for status in LeadStatus:
                status_counts[status.value] = len([l for l in leads if l.status == status])

            return {
                "success": True,
                "data": {
                    "campaign_id": str(campaign_id),
                    "status": campaign.status.value,
                    "started_at": campaign.started_at.isoformat() if campaign.started_at else None,
                    "total_leads": len(leads),
                    "lead_status_breakdown": status_counts,
                    "progress_percentage": self._calculate_progress_percentage(campaign, leads)
                }
            }

        except Exception as e:
            self.logger.error(f"Failed to get campaign progress: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _calculate_progress_percentage(self, campaign: Campaign, leads: List[Lead]) -> int:
        """Calculate campaign progress percentage."""
        if campaign.status == CampaignStatus.COMPLETED:
            return 100
        elif campaign.status == CampaignStatus.FAILED:
            return 0
        elif campaign.status == CampaignStatus.RUNNING:
            if not leads:
                return 0

            # Simple calculation based on lead status progression
            total_leads = len(leads)
            completed_leads = len([l for l in leads if l.status in [
                LeadStatus.QUALIFIED, LeadStatus.CONTACTED, LeadStatus.REJECTED
            ]])

            return min(int((completed_leads / total_leads) * 100), 99)  # Max 99% for running campaigns

        return 0