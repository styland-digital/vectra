"""Campaign orchestrator for running prospection campaigns."""

from typing import Dict, Any, Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus
from app.db.models.user import User
from app.orchestrator.state_machine import LeadStateMachine, TransitionError
from app.agents.prospector.agent import ProspectorAgent
from app.agents.bant.agent import BANTAgent
from app.agents.scheduler.agent import SchedulerAgent
from app.core.logging import get_logger
from app.core.config import settings
import redis

logger = get_logger(__name__)


class CampaignRunner:
    """
    Orchestrator for running prospection campaigns.
    
    Flow:
    PROSPECTING → QUALIFYING → SCHEDULING → COMPLETED
    """
    
    def __init__(self, db: Session):
        """
        Initialize campaign runner.
        
        Args:
            db: Database session
        """
        self.db = db
        self.redis_client = redis.from_url(settings.REDIS_URL) if settings.REDIS_URL else None
        self.state_machine = LeadStateMachine()
        
        # Initialize agents
        self.prospector = ProspectorAgent(db=db)
        self.bant = BANTAgent(db=db)
        self.scheduler = SchedulerAgent(db=db)
    
    def run_campaign(self, campaign_id: UUID) -> Dict[str, Any]:
        """
        Run a complete campaign.
        
        Args:
            campaign_id: Campaign UUID
            
        Returns:
            Result dictionary with campaign execution status
        """
        try:
            campaign = self.db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")
            
            # Check email verification
            if campaign.created_by:
                creator = self.db.query(User).filter(User.id == campaign.created_by).first()
                if creator and not creator.email_verified_at:
                    raise ValueError("Email verification required to launch campaigns. Please verify your email first.")
            
            # Update campaign status
            campaign.status = CampaignStatus.ACTIVE
            if not campaign.started_at:
                campaign.started_at = datetime.utcnow()
            self.db.commit()
            
            # Store campaign state in Redis
            self._set_campaign_state(campaign_id, {"status": "running", "started_at": datetime.utcnow().isoformat()})
            
            # Step 1: Prospecting
            logger.info(f"Starting prospecting for campaign {campaign_id}")
            prospecting_result = self._run_prospecting(campaign)
            
            # Step 2: Qualification (BANT)
            logger.info(f"Starting qualification for campaign {campaign_id}")
            qualification_result = self._run_qualification(campaign)
            
            # Step 3: Scheduling (Email sending)
            logger.info(f"Starting email scheduling for campaign {campaign_id}")
            scheduling_result = self._run_scheduling(campaign)
            
            # Update campaign status
            campaign.status = CampaignStatus.COMPLETED
            campaign.completed_at = datetime.utcnow()
            self.db.commit()
            
            self._set_campaign_state(campaign_id, {"status": "completed", "completed_at": datetime.utcnow().isoformat()})
            
            return {
                "success": True,
                "campaign_id": str(campaign_id),
                "prospecting": prospecting_result,
                "qualification": qualification_result,
                "scheduling": scheduling_result,
            }
            
        except Exception as e:
            logger.error(f"Error running campaign {campaign_id}: {e}", exc_info=True)
            
            # Update campaign status to paused on error
            campaign = self.db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if campaign:
                campaign.status = CampaignStatus.PAUSED
                self.db.commit()
            
            return {
                "success": False,
                "campaign_id": str(campaign_id),
                "error": str(e),
            }
    
    def _run_prospecting(self, campaign: Campaign) -> Dict[str, Any]:
        """Run prospecting phase."""
        try:
            input_data = {
                "campaign_id": str(campaign.id),
                "organization_id": str(campaign.organization_id),
                "job_titles": campaign.target_criteria.get("job_titles", []),
                "geography": campaign.target_criteria.get("geography", []),
                "company_size": campaign.target_criteria.get("company_size", []),
                "limit": campaign.daily_limit,
            }
            
            import asyncio
            result = asyncio.run(self.prospector.execute(input_data))
            
            if result["success"]:
                prospects = result["data"].get("prospects", [])
                leads_created = 0
                
                for prospect in prospects:
                    # Check for duplicates
                    existing = self.db.query(Lead).filter(
                        Lead.campaign_id == campaign.id,
                        Lead.email == prospect.get("email")
                    ).first()
                    
                    if not existing:
                        lead = Lead(
                            campaign_id=campaign.id,
                            organization_id=campaign.organization_id,
                            email=prospect.get("email"),
                            first_name=prospect.get("first_name"),
                            last_name=prospect.get("last_name"),
                            job_title=prospect.get("job_title"),
                            company_name=prospect.get("company_name"),
                            company_size=prospect.get("company_size"),
                            linkedin_url=prospect.get("linkedin_url"),
                            enrichment_data=prospect.get("enrichment_data", {}),
                            status=LeadStatus.ENRICHED,
                            source=prospect.get("source", "rocketreach"),
                        )
                        self.db.add(lead)
                        leads_created += 1
                
                self.db.commit()
                
                return {
                    "success": True,
                    "leads_found": len(prospects),
                    "leads_created": leads_created,
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error in prospecting: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    def _run_qualification(self, campaign: Campaign) -> Dict[str, Any]:
        """Run BANT qualification phase."""
        try:
            # Get all enriched leads
            leads = self.db.query(Lead).filter(
                Lead.campaign_id == campaign.id,
                Lead.status == LeadStatus.ENRICHED
            ).all()
            
            qualified_count = 0
            rejected_count = 0
            
            for lead in leads:
                try:
                    # Transition to scoring
                    self.state_machine.transition(lead, LeadStatus.SCORING, self.db)
                    
                    # Run BANT qualification
                    input_data = {
                        "lead_id": str(lead.id),
                        "lead_data": {
                            "company_size": lead.company_size,
                            "job_title": lead.job_title,
                            "company_industry": lead.company_name,
                            "enrichment_data": lead.enrichment_data,
                            "linkedin_url": lead.linkedin_url,
                        },
                        "campaign": {
                            "product_description": campaign.description or "",
                            "bant_threshold": campaign.bant_threshold,
                        },
                    }
                    
                    import asyncio
                    result = asyncio.run(self.bant.execute(input_data))
                    
                    if result["success"]:
                        qualified = result["data"].get("qualified", False)
                        
                        if qualified:
                            self.state_machine.transition(lead, LeadStatus.QUALIFIED, self.db)
                            qualified_count += 1
                        else:
                            self.state_machine.transition(lead, LeadStatus.REJECTED, self.db)
                            rejected_count += 1
                    else:
                        self.state_machine.transition(lead, LeadStatus.REJECTED, self.db, reason=result.get("error"))
                        rejected_count += 1
                        
                except TransitionError as e:
                    logger.warning(f"Transition error for lead {lead.id}: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Error qualifying lead {lead.id}: {e}", exc_info=True)
                    try:
                        self.state_machine.transition(lead, LeadStatus.REJECTED, self.db, reason=str(e))
                    except:
                        pass
                    rejected_count += 1
            
            return {
                "success": True,
                "qualified": qualified_count,
                "rejected": rejected_count,
            }
            
        except Exception as e:
            logger.error(f"Error in qualification: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    def _run_scheduling(self, campaign: Campaign) -> Dict[str, Any]:
        """Run email scheduling phase."""
        try:
            # Get all qualified leads
            leads = self.db.query(Lead).filter(
                Lead.campaign_id == campaign.id,
                Lead.status == LeadStatus.QUALIFIED
            ).all()
            
            sent_count = 0
            failed_count = 0
            
            for lead in leads:
                try:
                    input_data = {
                        "lead_id": str(lead.id),
                        "lead_data": {
                            "email": lead.email,
                            "first_name": lead.first_name,
                            "last_name": lead.last_name,
                            "job_title": lead.job_title,
                            "company_name": lead.company_name,
                        },
                        "campaign": {
                            "product_description": campaign.description or "",
                            "value_prop": campaign.target_criteria.get("value_prop", ""),
                        },
                        "send_email": True,
                    }
                    
                    import asyncio
                    result = asyncio.run(self.scheduler.execute(input_data))
                    
                    if result["success"] and result["data"].get("sent"):
                        self.state_machine.transition(lead, LeadStatus.CONTACTED, self.db)
                        sent_count += 1
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    logger.error(f"Error sending email to lead {lead.id}: {e}", exc_info=True)
                    failed_count += 1
            
            return {
                "success": True,
                "sent": sent_count,
                "failed": failed_count,
            }
            
        except Exception as e:
            logger.error(f"Error in scheduling: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    def _set_campaign_state(self, campaign_id: UUID, state: Dict[str, Any]) -> None:
        """Store campaign state in Redis."""
        if self.redis_client:
            key = f"campaign:{campaign_id}:state"
            self.redis_client.setex(key, 86400, str(state))  # 24h TTL
    
    def _get_campaign_state(self, campaign_id: UUID) -> Optional[Dict[str, Any]]:
        """Get campaign state from Redis."""
        if self.redis_client:
            key = f"campaign:{campaign_id}:state"
            data = self.redis_client.get(key)
            if data:
                import json
                return json.loads(data)
        return None
