"""Celery tasks for campaign pipeline execution."""

import asyncio
from uuid import UUID
from datetime import datetime, timedelta, timezone

from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(
    name="campaign.run",
    bind=True,
    max_retries=2,
    acks_late=True,
    reject_on_worker_lost=True,
)
def run_campaign(self, campaign_id: str) -> dict:
    from app.orchestrator.campaign_runner import CampaignRunner

    db = SessionLocal()
    try:
        runner = CampaignRunner(db=db)
        result = asyncio.run(runner.run_campaign(UUID(campaign_id)))
        return result
    except Exception as exc:
        logger.error(f"Campaign {campaign_id} failed: {exc}", exc_info=True)
        raise self.retry(exc=exc, countdown=120 * (2 ** self.request.retries))
    finally:
        db.close()


@celery_app.task(name="campaign.cleanup_stale_scoring")
def cleanup_stale_scoring() -> dict:
    """Reset leads stuck in SCORING for more than 1h back to ENRICHED (worker crash recovery)."""
    db = SessionLocal()
    try:
        from app.db.models.lead import Lead, LeadStatus

        cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
        stale = (
            db.query(Lead)
            .filter(Lead.status == LeadStatus.SCORING, Lead.updated_at < cutoff)
            .all()
        )
        for lead in stale:
            lead.status = LeadStatus.ENRICHED
        if stale:
            db.commit()
        logger.info(f"cleanup_stale_scoring: reset {len(stale)} stale SCORING leads")
        return {"reset": len(stale)}
    finally:
        db.close()
