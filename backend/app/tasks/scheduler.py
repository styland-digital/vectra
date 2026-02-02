"""Celery tasks for Scheduler agent."""

from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.agents.scheduler.agent import SchedulerAgent
from app.orchestrator.state_machine import LeadStateMachine, TransitionError
from app.db.models.lead import Lead, LeadStatus
from app.core.logging import get_logger
import asyncio

logger = get_logger(__name__)


@celery_app.task(name="scheduler.send_email", bind=True, max_retries=3)
def send_email(self, lead_id: str, email_data: dict) -> dict:
    """
    Task to send email using Scheduler agent.
    
    Args:
        lead_id: ID of the lead
        email_data: Email data (subject, body, etc.)
    
    Returns:
        dict: Email sending result
    """
    db = SessionLocal()
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead {lead_id} not found")
        
        agent = SchedulerAgent(db=db)
        
        input_data = {
            "lead_id": lead_id,
            "lead_data": email_data.get("lead_data", {}),
            "campaign": email_data.get("campaign", {}),
            "send_email": True,
        }
        
        result = asyncio.run(agent.execute(input_data))
        
        # Update lead status if email sent
        if result["success"] and result["data"].get("sent"):
            state_machine = LeadStateMachine()
            try:
                state_machine.transition(lead, LeadStatus.CONTACTED, db)
            except TransitionError:
                pass
        
        return result
        
    except Exception as e:
        logger.error(f"Error in scheduler.send_email: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
    finally:
        db.close()
