"""Celery tasks for Prospector agent."""

from uuid import UUID
from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.agents.prospector.agent import ProspectorAgent
from app.core.logging import get_logger
import asyncio

logger = get_logger(__name__)


@celery_app.task(name="prospector.find_leads", bind=True, max_retries=3)
def find_leads(self, campaign_id: str, criteria: dict) -> dict:
    """
    Task to find leads using Prospector agent.
    
    Args:
        campaign_id: ID of the campaign
        criteria: Search criteria (job_titles, geography, company_size, etc.)
    
    Returns:
        dict: Results with found leads
    """
    db = SessionLocal()
    try:
        agent = ProspectorAgent(db=db)
        
        input_data = {
            "campaign_id": campaign_id,
            "organization_id": criteria.get("organization_id"),
            "job_titles": criteria.get("job_titles", []),
            "geography": criteria.get("geography", []),
            "company_size": criteria.get("company_size", []),
            "limit": criteria.get("limit", 50),
        }
        
        result = asyncio.run(agent.execute(input_data))
        
        return result
        
    except Exception as e:
        logger.error(f"Error in prospector.find_leads: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
    finally:
        db.close()
