"""Organization model - Multi-tenant root entity."""

from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class PlanType(str, enum.Enum):
    """Subscription plan types."""
    TRIAL = "trial"
    STARTER = "starter"
    GROWTH = "growth"
    SCALE = "scale"


class Organization(BaseModel):
    """
    Organization model - Root entity for multi-tenant isolation.

    All data in the system is scoped to an organization.
    """

    __tablename__ = "organizations"

    # Basic info
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    # Plan and billing
    plan = Column(
        SQLEnum(PlanType, name="plan_type", create_type=False, values_callable=lambda x: [e.value for e in x]),
        default=PlanType.TRIAL,
        nullable=False
    )

    # Flexible settings (timezone, branding, etc.)
    settings = Column(JSONB, default=dict, nullable=False)

    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="organization", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="organization", cascade="all, delete-orphan")
    meetings = relationship("Meeting", back_populates="organization", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="organization", uselist=False, cascade="all, delete-orphan")
    usage_records = relationship("UsageRecord", back_populates="organization", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Organization {self.name} ({self.slug})>"
