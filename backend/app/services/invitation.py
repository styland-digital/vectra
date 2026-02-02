"""Invitation service for user invitations."""

import secrets
from typing import Optional, Tuple
from uuid import UUID
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError
from app.core.config import settings
from app.core.security import get_password_hash, create_access_token, create_refresh_token
from app.db.repositories.user import UserRepository
from app.db.repositories.organization import OrganizationRepository
from app.db.models.user import User, UserRole
from app.db.models.invitation import Invitation
from app.services.resend import ResendService


class InvitationService:
    """Service for user invitations."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.org_repo = OrganizationRepository(db)
        self.email_service = ResendService()

    def invite_user(
        self,
        inviter: User,
        email: str,
        role: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> str:
        """
        Invite a user to the organization using OTP.
        
        Creates a 6-digit OTP and stores invitation data in the invitations table.
        Sends invitation email with OTP.
        
        Args:
            inviter: User who is sending the invitation
            email: Email address to invite
            role: Role to assign
            first_name: First name (optional)
            last_name: Last name (optional)
            
        Returns:
            OTP (6 digits)
            
        Raises:
            BadRequestError: If email already exists or user already in org
        """
        if not inviter.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        # Check if user already exists
        if self.user_repo.email_exists(email):
            existing_user = self.user_repo.get_by_email(email)
            if existing_user.organization_id == inviter.organization_id:
                raise BadRequestError("User already belongs to this organization")
            raise BadRequestError("User with this email already exists")
        
        # Check if there's already a pending invitation for this email
        existing_invitation = self.db.query(Invitation).filter(
            Invitation.email == email,
            Invitation.organization_id == inviter.organization_id,
            Invitation.otp_expires_at > datetime.now(timezone.utc)
        ).first()
        
        if existing_invitation:
            raise BadRequestError("An active invitation already exists for this email")
        
        # Validate role
        try:
            role_enum = UserRole(role.lower())
        except ValueError:
            raise BadRequestError(f"Invalid role: {role}")
        
        # Generate 6-digit OTP
        otp = f"{secrets.randbelow(1000000):06d}"
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        # Create invitation record
        invitation = Invitation(
            email=email,
            organization_id=inviter.organization_id,
            role=role,
            invited_by=inviter.id,
            otp=otp,
            otp_expires_at=expires_at,
            first_name=first_name,
            last_name=last_name,
        )
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        
        # Send invitation email with OTP
        org = self.org_repo.get_by_id(inviter.organization_id)
        invitation_url = f"{settings.APP_URL}/invite/accept"
        
        try:
            self.email_service.send_invitation_email(
                to=email,
                inviter_name=inviter.full_name,
                organization_name=org.name,
                invitation_url=invitation_url,
                role=role,
                otp=otp,  # Pass OTP to email template
            )
        except Exception:
            # Log but don't fail if email sending fails
            from app.core.logging import get_logger
            logger = get_logger(__name__)
            logger.warning(f"Failed to send invitation email to {email}", exc_info=True)
        
        return otp

    def accept_invitation(
        self,
        email: str,
        otp: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Tuple[str, str, User]:
        """
        Accept invitation using OTP and create user account.
        
        Args:
            email: Email address from invitation
            otp: 6-digit OTP code
            password: User password
            first_name: First name (optional, overrides invitation data)
            last_name: Last name (optional, overrides invitation data)
            
        Returns:
            Tuple of (access_token, refresh_token, user)
            
        Raises:
            UnauthorizedError: If OTP is invalid or expired
            BadRequestError: If user already exists
        """
        # Find invitation by email and OTP
        invitation = self.db.query(Invitation).filter(
            Invitation.email == email,
            Invitation.otp == otp,
            Invitation.otp_expires_at > datetime.now(timezone.utc)
        ).first()
        
        if not invitation:
            raise UnauthorizedError("Invalid or expired invitation OTP")
        
        # Verify organization exists
        org = self.org_repo.get_by_id(invitation.organization_id)
        if not org:
            raise NotFoundError("Organization not found")
        
        # Check if user already exists
        if self.user_repo.email_exists(email):
            # Delete invitation if user already exists
            self.db.delete(invitation)
            self.db.commit()
            raise BadRequestError("User with this email already exists")
        
        # Create user
        password_hash = get_password_hash(password)
        user = self.user_repo.create(
            email=email,
            password_hash=password_hash,
            organization_id=invitation.organization_id,
            first_name=first_name or invitation.first_name or "",
            last_name=last_name or invitation.last_name or "",
            role=invitation.role,
        )
        
        # Delete invitation after successful acceptance
        self.db.delete(invitation)
        self.db.commit()
        
        # Generate JWT tokens
        access_token = create_access_token({
            "sub": str(user.id),
            "org": str(user.organization_id),
            "role": user.role.value,
        })
        refresh_token = create_refresh_token({
            "sub": str(user.id),
        })
        
        return access_token, refresh_token, user
