"""Campaign orchestrator — async pipeline: Prospect → BANT → Schedule."""

import json
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus
from app.orchestrator.state_machine import LeadStateMachine, TransitionError
from app.agents.prospector.agent import ProspectorAgent
from app.agents.bant.agent import BANTAgent
from app.agents.scheduler.agent import SchedulerAgent
from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)


class CampaignRunner:
    """
    Async orchestrator for the 3-phase prospection pipeline.

    Phase 1 — Prospecting  : ProspectorAgent finds leads via RocketReach.
    Phase 2 — Qualification: BANTAgent scores each ENRICHED lead.
    Phase 3 — Scheduling   : SchedulerAgent emails each QUALIFIED lead.

    Pause signal: after each phase the runner re-reads campaign.status from DB.
    If PAUSED, it resets any leads stuck in SCORING back to ENRICHED so that a
    subsequent resume can pick up cleanly, then returns early.
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        self.state_machine = LeadStateMachine()

        # Redis is optional — failure to connect never blocks the campaign.
        self._redis: Any = None
        try:
            if settings.REDIS_URL:
                import redis as _redis
                self._redis = _redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        except Exception as exc:
            logger.warning(f"Redis unavailable — state tracking disabled: {exc}")

        self.prospector = ProspectorAgent(db=db)
        self.bant = BANTAgent(db=db)
        self.scheduler = SchedulerAgent(db=db)

    # ─── Public entry point ───────────────────────────────────────────────────

    async def run_campaign(self, campaign_id: UUID) -> Dict[str, Any]:
        """
        Execute the full campaign pipeline asynchronously.

        Returns a result dict; on pause/error the campaign is left in PAUSED
        status so the user can resume or investigate.
        """
        campaign = self._fetch_campaign(campaign_id)
        if not campaign:
            logger.error(f"Campaign {campaign_id} not found — aborting background task")
            return {"success": False, "error": "Campaign not found"}

        try:
            # Ensure the campaign is still ACTIVE (could have been paused just after launch).
            if campaign.status != CampaignStatus.ACTIVE:
                logger.info(f"Campaign {campaign_id} is {campaign.status} — skipping run")
                return {"success": False, "paused": True, "campaign_id": str(campaign_id)}

            self._set_state(campaign_id, {"status": "running", "phase": "prospecting"})

            # ── Phase 1: Prospecting ──────────────────────────────────────────
            logger.info(f"[{campaign_id}] Phase 1 — Prospecting")
            prospecting_result = await self._run_prospecting(campaign)

            if self._is_paused(campaign_id):
                return self._paused_result(campaign_id)

            # ── Phase 2: BANT Qualification ───────────────────────────────────
            logger.info(f"[{campaign_id}] Phase 2 — BANT Qualification")
            self._set_state(campaign_id, {"status": "running", "phase": "qualification"})
            qualification_result = await self._run_qualification(campaign)

            if self._is_paused(campaign_id):
                self._cleanup_scoring_leads(campaign_id)
                return self._paused_result(campaign_id)

            # ── Phase 3: Email Scheduling ─────────────────────────────────────
            logger.info(f"[{campaign_id}] Phase 3 — Email Scheduling")
            self._set_state(campaign_id, {"status": "running", "phase": "scheduling"})
            scheduling_result = await self._run_scheduling(campaign)

            # ── Complete ──────────────────────────────────────────────────────
            campaign = self._fetch_campaign(campaign_id)
            if campaign and campaign.status == CampaignStatus.ACTIVE:
                campaign.status = CampaignStatus.COMPLETED
                campaign.completed_at = datetime.now(timezone.utc)
                self.db.commit()

            self._set_state(campaign_id, {
                "status": "completed",
                "completed_at": datetime.now(timezone.utc).isoformat(),
            })
            logger.info(f"[{campaign_id}] Campaign completed successfully")

            return {
                "success": True,
                "campaign_id": str(campaign_id),
                "prospecting": prospecting_result,
                "qualification": qualification_result,
                "scheduling": scheduling_result,
            }

        except Exception as exc:
            logger.error(f"[{campaign_id}] Fatal error: {exc}", exc_info=True)
            self._set_paused(campaign_id)
            self._cleanup_scoring_leads(campaign_id)
            self._set_state(campaign_id, {"status": "error", "error": str(exc)})
            return {"success": False, "campaign_id": str(campaign_id), "error": str(exc)}

    # ─── Phase implementations ────────────────────────────────────────────────

    async def _run_prospecting(self, campaign: Campaign) -> Dict[str, Any]:
        try:
            criteria = campaign.target_criteria or {}
            input_data = {
                "campaign_id": str(campaign.id),
                "organization_id": str(campaign.organization_id),
                "job_titles": criteria.get("job_titles", []),
                "locations": criteria.get("geography", criteria.get("locations", [])),
                "company_sizes": criteria.get("company_size", criteria.get("company_sizes", [])),
                "industries": criteria.get("industries", []),
                "limit": campaign.daily_limit,
                "target_criteria": criteria,
            }

            result = await self.prospector.execute(input_data)

            if not result.get("success"):
                logger.warning(f"[{campaign.id}] Prospecting returned failure: {result.get('error')}")
                return result

            prospects = result.get("data", {}).get("prospects", [])
            leads_created = 0

            for prospect in prospects:
                email = prospect.get("email")
                if not email:
                    continue  # Lead.email is NOT NULL

                existing = (
                    self.db.query(Lead)
                    .filter(Lead.campaign_id == campaign.id, Lead.email == email)
                    .first()
                )
                if existing:
                    continue

                lead = Lead(
                    campaign_id=campaign.id,
                    organization_id=campaign.organization_id,
                    email=email,
                    first_name=prospect.get("first_name"),
                    last_name=prospect.get("last_name"),
                    job_title=prospect.get("job_title"),
                    company_name=prospect.get("company_name"),
                    company_size=prospect.get("company_size"),
                    linkedin_url=prospect.get("linkedin_url"),
                    enrichment_data=prospect.get("enrichment_data", {}),
                    status=LeadStatus.ENRICHED,
                    source=prospect.get("source", "rocketreach"),
                    enriched_at=datetime.now(timezone.utc),
                )
                self.db.add(lead)
                leads_created += 1

            self.db.commit()
            logger.info(f"[{campaign.id}] Prospecting done: {leads_created} new leads")

            return {
                "success": True,
                "leads_found": len(prospects),
                "leads_created": leads_created,
            }

        except Exception as exc:
            logger.error(f"[{campaign.id}] Prospecting error: {exc}", exc_info=True)
            return {"success": False, "error": str(exc)}

    async def _run_qualification(self, campaign: Campaign) -> Dict[str, Any]:
        qualified_count = 0
        rejected_count = 0

        try:
            leads = (
                self.db.query(Lead)
                .filter(
                    Lead.campaign_id == campaign.id,
                    Lead.status.in_([LeadStatus.ENRICHED, LeadStatus.SCORING]),
                )
                .all()
            )

            for lead in leads:
                # Abort this phase if user paused mid-qualification.
                if self._is_paused(campaign.id):
                    break

                try:
                    # Transition to SCORING (idempotent — skip if already there).
                    if lead.status == LeadStatus.ENRICHED:
                        try:
                            self.state_machine.transition(lead, LeadStatus.SCORING, self.db)
                        except TransitionError:
                            lead.status = LeadStatus.SCORING
                            self.db.commit()

                    input_data = {
                        "lead_id": str(lead.id),
                        "lead_data": {
                            "company_size": lead.company_size,
                            "job_title": lead.job_title,
                            "company_industry": lead.company_name,
                            "enrichment_data": lead.enrichment_data or {},
                            "linkedin_url": lead.linkedin_url,
                        },
                        "campaign": {
                            "product_description": campaign.description or "",
                            "bant_threshold": campaign.bant_threshold,
                        },
                    }

                    result = await self.bant.execute(input_data)

                    if result.get("success"):
                        if result["data"].get("qualified"):
                            qualified_count += 1
                        else:
                            rejected_count += 1
                    else:
                        # Agent failure → reject the lead to unblock the pipeline.
                        lead.status = LeadStatus.REJECTED
                        self.db.commit()
                        rejected_count += 1

                except Exception as exc:
                    logger.error(f"[{campaign.id}] BANT error for lead {lead.id}: {exc}")
                    try:
                        lead.status = LeadStatus.REJECTED
                        self.db.commit()
                    except Exception:
                        pass
                    rejected_count += 1

            logger.info(
                f"[{campaign.id}] Qualification done: "
                f"{qualified_count} qualified, {rejected_count} rejected"
            )
            return {"success": True, "qualified": qualified_count, "rejected": rejected_count}

        except Exception as exc:
            logger.error(f"[{campaign.id}] Qualification phase error: {exc}", exc_info=True)
            return {"success": False, "error": str(exc)}

    async def _run_scheduling(self, campaign: Campaign) -> Dict[str, Any]:
        sent_count = 0
        failed_count = 0

        try:
            leads = (
                self.db.query(Lead)
                .filter(
                    Lead.campaign_id == campaign.id,
                    Lead.status == LeadStatus.QUALIFIED,
                )
                .all()
            )

            for lead in leads:
                if self._is_paused(campaign.id):
                    break

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
                            "value_prop": (campaign.target_criteria or {}).get("value_prop", ""),
                        },
                        "send_email": True,
                    }

                    result = await self.scheduler.execute(input_data)

                    if result.get("success") and result.get("data", {}).get("sent"):
                        sent_count += 1
                    else:
                        failed_count += 1

                except Exception as exc:
                    logger.error(f"[{campaign.id}] Scheduling error for lead {lead.id}: {exc}")
                    failed_count += 1

            logger.info(
                f"[{campaign.id}] Scheduling done: {sent_count} sent, {failed_count} failed"
            )
            return {"success": True, "sent": sent_count, "failed": failed_count}

        except Exception as exc:
            logger.error(f"[{campaign.id}] Scheduling phase error: {exc}", exc_info=True)
            return {"success": False, "error": str(exc)}

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _fetch_campaign(self, campaign_id: UUID) -> Optional[Campaign]:
        """Re-fetch the campaign from the DB (bypasses any cached state)."""
        self.db.expire_all()
        return self.db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def _is_paused(self, campaign_id: UUID) -> bool:
        """Check whether the user has signalled a pause."""
        c = self._fetch_campaign(campaign_id)
        return c is not None and c.status == CampaignStatus.PAUSED

    def _set_paused(self, campaign_id: UUID) -> None:
        """Persist PAUSED status (best-effort)."""
        try:
            c = self._fetch_campaign(campaign_id)
            if c and c.status == CampaignStatus.ACTIVE:
                c.status = CampaignStatus.PAUSED
                self.db.commit()
        except Exception as exc:
            logger.warning(f"Could not set campaign {campaign_id} to PAUSED: {exc}")

    def _cleanup_scoring_leads(self, campaign_id: UUID) -> None:
        """Reset any leads stuck in SCORING back to ENRICHED for clean resume."""
        try:
            self.db.query(Lead).filter(
                Lead.campaign_id == campaign_id,
                Lead.status == LeadStatus.SCORING,
            ).update({"status": LeadStatus.ENRICHED}, synchronize_session=False)
            self.db.commit()
        except Exception as exc:
            logger.warning(f"Could not cleanup SCORING leads for {campaign_id}: {exc}")

    def _paused_result(self, campaign_id: UUID) -> Dict[str, Any]:
        logger.info(f"[{campaign_id}] Campaign paused — background task exiting cleanly")
        return {"success": True, "paused": True, "campaign_id": str(campaign_id)}

    def _set_state(self, campaign_id: UUID, state: Dict[str, Any]) -> None:
        if not self._redis:
            return
        try:
            key = f"campaign:{campaign_id}:state"
            self._redis.setex(key, 86_400, json.dumps(state, default=str))
        except Exception as exc:
            logger.debug(f"Redis state write failed (non-fatal): {exc}")
