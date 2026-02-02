"""Integration model for CRM and external service connections."""

from sqlalchemy import Column, String, ForeignKey, DateTime, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class IntegrationType(str, enum.Enum):
    """Supported integration types."""
    HUBSPOT = "hubspot"
    SALESFORCE = "salesforce"
    CALENDLY = "calendly"
    GOOGLE_CALENDAR = "google_calendar"
    SLACK = "slack"


class IntegrationStatus(str, enum.Enum):
    """Integration connection status."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"


class Integration(BaseModel):
    """
    Integration model - External service connections.

    Stores OAuth credentials and sync settings for each integration.
    One integration per type per organization.
    """

    __tablename__ = "integrations"
    __table_args__ = (
        UniqueConstraint("organization_id", "type", name="uq_integration_org_type"),
    )

    # Organization
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Integration type
    type = Column(
        SQLEnum(IntegrationType, name="integration_type", create_type=False),
        nullable=False
    )

    # Connection status
    status = Column(
        SQLEnum(IntegrationStatus, name="integration_status", create_type=False),
        default=IntegrationStatus.DISCONNECTED,
        nullable=False
    )

    # OAuth credentials (encrypted in production)
    credentials = Column(JSONB)

    # Integration-specific settings
    settings = Column(JSONB, default=dict, nullable=False)

    # Sync tracking
    last_sync_at = Column(DateTime)

    # Relationships
    organization = relationship("Organization", back_populates="integrations")

    @property
    def is_connected(self) -> bool:
        """Check if integration is connected."""
        return self.status == IntegrationStatus.CONNECTED

    def __repr__(self) -> str:
        return f"<Integration {self.type.value} ({self.status.value})>"
