"""Invitation model for OTP-based user invitations."""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import BaseModel


class Invitation(BaseModel):
    """
    Invitation model for OTP-based user invitations.
    
    Stores invitation data temporarily until user accepts with OTP.
    """

    __tablename__ = "invitations"

    # Email to invite
    email = Column(String(255), nullable=False, index=True)

    # Organization and role
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    role = Column(String(50), nullable=False)

    # Inviter
    invited_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # OTP (6 digits)
    otp = Column(String(6), nullable=False, index=True)
    otp_expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # Optional user info
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    # Relationships
    organization = relationship("Organization", backref="invitations")
    inviter = relationship("User", foreign_keys=[invited_by], backref="sent_invitations")

    def is_expired(self) -> bool:
        """Check if invitation OTP has expired."""
        return datetime.now(timezone.utc) > self.otp_expires_at

    def __repr__(self) -> str:
        return f"<Invitation {self.email} -> {self.organization_id} ({self.role})>"
