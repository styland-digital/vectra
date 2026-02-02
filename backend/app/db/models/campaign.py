"""Campaign model for prospection campaigns."""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class CampaignStatus(str, enum.Enum):
    """Campaign status values."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Campaign(BaseModel):
    """
    Campaign model for B2B prospection campaigns.

    Each campaign targets specific criteria and uses AI agents
    to find, qualify, and contact leads.
    """

    __tablename__ = "campaigns"

    # Organization (multi-tenant)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Creator
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Campaign info
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Status
    status = Column(
        SQLEnum(CampaignStatus, name="campaign_status", create_type=False),
        default=CampaignStatus.DRAFT,
        nullable=False,
        index=True
    )

    # Targeting criteria for Prospector agent
    target_criteria = Column(JSONB, default=dict, nullable=False)

    # Email template for Scheduler agent
    email_template = Column(JSONB)

    # BANT qualification settings
    bant_threshold = Column(Integer, default=60, nullable=False)

    # Rate limiting
    daily_limit = Column(Integer, default=50, nullable=False)

    # Lifecycle timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
    created_by_user = relationship("User", back_populates="created_campaigns", foreign_keys=[created_by])
    leads = relationship("Lead", back_populates="campaign", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="campaign", cascade="all, delete-orphan")
    meetings = relationship("Meeting", back_populates="campaign", cascade="all, delete-orphan")
    agent_runs = relationship("AgentRun", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Campaign {self.name} ({self.status.value})>"
