"""Celery tasks for BANT qualifier agent."""

from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.agents.bant.agent import BANTAgent
from app.orchestrator.state_machine import LeadStateMachine, TransitionError
from app.db.models.lead import Lead, LeadStatus
from app.core.logging import get_logger
import asyncio

logger = get_logger(__name__)


@celery_app.task(name="bant.qualify_lead", bind=True, max_retries=3)
def qualify_lead(self, lead_id: str, lead_data: dict) -> dict:
    """
    Task to qualify a lead using BANT agent.
    
    Args:
        lead_id: ID of the lead to qualify
        lead_data: Lead data (job_title, company_size, etc.)
    
    Returns:
        dict: BANT score and qualification result
    """
    db = SessionLocal()
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead {lead_id} not found")
        
        # Transition to scoring
        state_machine = LeadStateMachine()
        try:
            state_machine.transition(lead, LeadStatus.SCORING, db)
        except TransitionError:
            pass  # Already in scoring or invalid transition
        
        agent = BANTAgent(db=db)
        
        input_data = {
            "lead_id": lead_id,
            "lead_data": lead_data,
            "campaign": lead_data.get("campaign", {}),
        }
        
        result = asyncio.run(agent.execute(input_data))
        
        # Update lead status based on result
        if result["success"]:
            qualified = result["data"].get("qualified", False)
            try:
                if qualified:
                    state_machine.transition(lead, LeadStatus.QUALIFIED, db)
                else:
                    state_machine.transition(lead, LeadStatus.REJECTED, db)
            except TransitionError:
                pass
        
        return result
        
    except Exception as e:
        logger.error(f"Error in bant.qualify_lead: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
    finally:
        db.close()
