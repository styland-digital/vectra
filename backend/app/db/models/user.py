"""User model with RBAC roles."""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class UserRole(str, enum.Enum):
    """User roles for RBAC."""
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    OPERATOR = "operator"
    VIEWER = "viewer"
    PLATFORM_ADMIN = "platform_admin"


class User(BaseModel):
    """
    User model with role-based access control.

    Roles hierarchy: Owner > Admin > Manager > Operator > Viewer
    """

    __tablename__ = "users"

    # Organization (multi-tenant)
    # Nullable for platform admins (they don't belong to any organization)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profile
    first_name = Column(String(100))
    last_name = Column(String(100))

    # Role and status
    role = Column(
        SQLEnum(UserRole, name="user_role", create_type=False, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.OPERATOR,
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    email_verified_at = Column(DateTime)
    last_login_at = Column(DateTime)
    
    # Email verification OTP
    email_verification_otp = Column(String(6))
    email_verification_otp_expires_at = Column(DateTime)
    
    # Password change OTP
    password_change_otp = Column(String(6))
    password_change_otp_expires_at = Column(DateTime)

    # Relationships
    organization = relationship("Organization", back_populates="users")
    created_campaigns = relationship("Campaign", back_populates="created_by_user", foreign_keys="Campaign.created_by")
    approved_emails = relationship("Email", back_populates="approved_by_user", foreign_keys="Email.approved_by")

    @property
    def full_name(self) -> str:
        """Return user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.email

    def is_platform_admin(self) -> bool:
        """Check if user is a platform admin."""
        return self.role == UserRole.PLATFORM_ADMIN and self.organization_id is None

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"
