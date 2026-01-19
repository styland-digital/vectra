"""Usage record model for tracking resource consumption."""

from sqlalchemy import Column, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import BaseModel


class UsageRecord(BaseModel):
    """
    Usage record model - Track resource consumption per billing period.

    Used for metered billing and quota enforcement.
    """

    __tablename__ = "usage_records"
    __table_args__ = (
        UniqueConstraint("organization_id", "period_start", name="uq_usage_org_period"),
    )

    # Organization
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Billing period
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)

    # Leads usage
    leads_used = Column(Integer, default=0, nullable=False)
    leads_limit = Column(Integer)

    # Email usage
    emails_sent = Column(Integer, default=0, nullable=False)
    emails_limit = Column(Integer)

    # API calls
    api_calls = Column(Integer, default=0, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="usage_records")

    @property
    def leads_remaining(self) -> int | None:
        """Get remaining leads quota."""
        if self.leads_limit is None:
            return None
        return max(0, self.leads_limit - self.leads_used)

    @property
    def emails_remaining(self) -> int | None:
        """Get remaining emails quota."""
        if self.emails_limit is None:
            return None
        return max(0, self.emails_limit - self.emails_sent)

    def __repr__(self) -> str:
        return f"<UsageRecord {self.period_start} - {self.period_end}>"
