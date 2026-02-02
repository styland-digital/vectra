"""State machine for lead status transitions."""

from typing import Dict, Optional, List
from enum import Enum
from sqlalchemy.orm import Session

from app.db.models.lead import Lead, LeadStatus
from app.core.logging import get_logger

logger = get_logger(__name__)


class TransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class LeadStateMachine:
    """
    State machine for managing lead status transitions.
    
    Valid transitions:
    - NEW → ENRICHED
    - ENRICHED → SCORING
    - SCORING → QUALIFIED | REJECTED
    - QUALIFIED → CONTACTED
    - CONTACTED → MEETING_SCHEDULED
    - MEETING_SCHEDULED → COMPLETED
    """
    
    # Valid transitions mapping
    VALID_TRANSITIONS: Dict[LeadStatus, List[LeadStatus]] = {
        LeadStatus.NEW: [LeadStatus.ENRICHED, LeadStatus.REJECTED],
        LeadStatus.ENRICHED: [LeadStatus.SCORING, LeadStatus.REJECTED],
        LeadStatus.SCORING: [LeadStatus.QUALIFIED, LeadStatus.REJECTED],
        LeadStatus.QUALIFIED: [LeadStatus.CONTACTED, LeadStatus.REJECTED],
        LeadStatus.CONTACTED: [LeadStatus.MEETING_SCHEDULED, LeadStatus.REJECTED],
        LeadStatus.MEETING_SCHEDULED: [LeadStatus.COMPLETED, LeadStatus.REJECTED],
        LeadStatus.REJECTED: [],  # Terminal state
        LeadStatus.COMPLETED: [],  # Terminal state
    }
    
    @classmethod
    def can_transition(cls, from_status: LeadStatus, to_status: LeadStatus) -> bool:
        """
        Check if a transition is valid.
        
        Args:
            from_status: Current status
            to_status: Target status
            
        Returns:
            True if transition is valid
        """
        allowed = cls.VALID_TRANSITIONS.get(from_status, [])
        return to_status in allowed
    
    @classmethod
    def transition(
        cls,
        lead: Lead,
        to_status: LeadStatus,
        db: Session,
        reason: Optional[str] = None,
    ) -> Lead:
        """
        Transition a lead to a new status.
        
        Args:
            lead: Lead instance
            to_status: Target status
            db: Database session
            reason: Optional reason for transition
            
        Returns:
            Updated lead instance
            
        Raises:
            TransitionError: If transition is invalid
        """
        from_status = lead.status
        
        if not cls.can_transition(from_status, to_status):
            raise TransitionError(
                f"Invalid transition from {from_status.value} to {to_status.value}"
            )
        
        lead.status = to_status
        db.commit()
        
        logger.info(
            f"Lead {lead.id} transitioned from {from_status.value} to {to_status.value}",
            extra={
                "lead_id": str(lead.id),
                "from_status": from_status.value,
                "to_status": to_status.value,
                "reason": reason,
            }
        )
        
        return lead
    
    @classmethod
    def get_next_states(cls, current_status: LeadStatus) -> List[LeadStatus]:
        """
        Get all valid next states from current status.
        
        Args:
            current_status: Current lead status
            
        Returns:
            List of valid next states
        """
        return cls.VALID_TRANSITIONS.get(current_status, [])
