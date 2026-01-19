"""Subscription model for Stripe billing."""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class SubscriptionStatus(str, enum.Enum):
    """Stripe subscription status values."""
    ACTIVE = "active"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    TRIALING = "trialing"
    PAUSED = "paused"


class BillingCycle(str, enum.Enum):
    """Billing cycle options."""
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Subscription(BaseModel):
    """
    Subscription model - Stripe billing integration.

    One subscription per organization.
    """

    __tablename__ = "subscriptions"

    # Organization (one-to-one)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    # Stripe IDs
    stripe_customer_id = Column(String(255), index=True)
    stripe_subscription_id = Column(String(255), unique=True, index=True)

    # Plan info
    plan = Column(String(50), nullable=False)
    billing_cycle = Column(
        SQLEnum(BillingCycle, name="billing_cycle", create_type=False),
        nullable=True
    )

    # Status
    status = Column(
        SQLEnum(SubscriptionStatus, name="subscription_status", create_type=False),
        nullable=False
    )

    # Billing period
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)

    # Trial
    trial_end = Column(DateTime)

    # Cancellation
    cancel_at_period_end = Column(Boolean, default=False, nullable=False)
    canceled_at = Column(DateTime)

    # Relationships
    organization = relationship("Organization", back_populates="subscription")

    @property
    def is_active(self) -> bool:
        """Check if subscription is in good standing."""
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]

    def __repr__(self) -> str:
        return f"<Subscription {self.plan} ({self.status.value})>"
