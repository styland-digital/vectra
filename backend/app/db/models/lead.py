"""Lead model with BANT qualification."""

from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class LeadStatus(str, enum.Enum):
    """Lead status in the prospection pipeline."""
    NEW = "new"
    ENRICHED = "enriched"
    SCORING = "scoring"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    MEETING_SCHEDULED = "meeting_scheduled"
    COMPLETED = "completed"
    REJECTED = "rejected"


class LeadIntent(str, enum.Enum):
    """Lead intent classification from responses."""
    INTERESTED_NOW = "interested_now"
    INTERESTED_LATER = "interested_later"
    OBJECTION_PRICE = "objection_price"
    OBJECTION_TIMING = "objection_timing"
    POLITE_DECLINE = "polite_decline"
    NOT_INTERESTED = "not_interested"
    OUT_OF_OFFICE = "out_of_office"
    WRONG_PERSON = "wrong_person"


class Lead(BaseModel):
    """
    Lead model - Prospect identified and qualified by AI agents.

    BANT Score = Budget(0-25) + Authority(0-25) + Need(0-25) + Timeline(0-25)
    Total: 0-100
    """

    __tablename__ = "leads"
    __table_args__ = (
        UniqueConstraint("campaign_id", "email", name="uq_lead_campaign_email"),
    )

    # Foreign keys
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

    # Contact info
    email = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(50))

    # Professional info
    job_title = Column(String(200))
    company_name = Column(String(255))
    company_size = Column(String(50))
    linkedin_url = Column(String(500))

    # Enrichment data from RocketReach/APIs
    enrichment_data = Column(JSONB, default=dict, nullable=False)

    # BANT qualification
    bant_score = Column(Integer, index=True)
    bant_breakdown = Column(JSONB)  # {budget: 20, authority: 25, need: 18, timeline: 15}

    # Intent classification (from email responses)
    intent = Column(
        SQLEnum(LeadIntent, name="lead_intent", create_type=False),
        nullable=True
    )

    # Status
    status = Column(
        SQLEnum(LeadStatus, name="lead_status", create_type=False),
        default=LeadStatus.NEW,
        nullable=False,
        index=True
    )

    # Source tracking
    source = Column(String(100))

    # Relationships
    campaign = relationship("Campaign", back_populates="leads")
    organization = relationship("Organization", back_populates="leads")
    emails = relationship("Email", back_populates="lead", cascade="all, delete-orphan")
    meetings = relationship("Meeting", back_populates="lead", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        """Return lead's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.email

    @property
    def is_qualified(self) -> bool:
        """Check if lead is qualified based on BANT score."""
        return self.bant_score is not None and self.bant_score >= 60

    def __repr__(self) -> str:
        return f"<Lead {self.email} (score={self.bant_score})>"
