"""Meeting model for scheduled meetings via Calendly."""

from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class MeetingStatus(str, enum.Enum):
    """Meeting status values."""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELED = "canceled"
    NO_SHOW = "no_show"


class MeetingOutcome(str, enum.Enum):
    """Meeting outcome classification."""
    QUALIFIED = "qualified"
    NEEDS_FOLLOWUP = "needs_followup"
    NOT_INTERESTED = "not_interested"
    WRONG_FIT = "wrong_fit"
    DEAL_CLOSED = "deal_closed"


class Meeting(BaseModel):
    """
    Meeting model - Calendly meetings scheduled with qualified leads.

    Meetings are the final step in the prospection pipeline.
    """

    __tablename__ = "meetings"

    # Foreign keys
    lead_id = Column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    campaign_id = Column(
        UUID(as_uuid=True),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Meeting details
    scheduled_at = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, default=30, nullable=False)
    meeting_url = Column(String(500))

    # Calendly integration
    calendly_event_id = Column(String(255))

    # Status
    status = Column(
        SQLEnum(MeetingStatus, name="meeting_status", create_type=False),
        default=MeetingStatus.SCHEDULED,
        nullable=False,
        index=True
    )

    # Completion
    completed_at = Column(DateTime)
    no_show = Column(Boolean, default=False, nullable=False)

    # Notes and outcome
    notes = Column(Text)
    outcome = Column(
        SQLEnum(MeetingOutcome, name="meeting_outcome", create_type=False),
        nullable=True
    )

    # Relationships
    lead = relationship("Lead", back_populates="meetings")
    campaign = relationship("Campaign", back_populates="meetings")
    organization = relationship("Organization", back_populates="meetings")

    def __repr__(self) -> str:
        return f"<Meeting {self.scheduled_at} ({self.status.value})>"
