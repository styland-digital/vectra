"""Email verification service for business logic."""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, UnauthorizedError
from app.core.config import settings

# Default APP_URL if not set
if not settings.APP_URL:
    settings.APP_URL = "http://localhost:3000"
from app.db.repositories.user import UserRepository
from app.db.models.user import User


class EmailVerificationService:
    """Service for email verification operations."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def generate_verification_otp(self, user: User) -> str:
        """
        Generate a 6-digit OTP for email verification.

        Returns:
            6-digit OTP string

        Raises:
            BadRequestError: If user email is already verified
        """
        if user.email_verified_at:
            raise BadRequestError("Email is already verified")

        otp = f"{secrets.randbelow(1000000):06d}"
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        
        user.email_verification_otp = otp
        user.email_verification_otp_expires_at = expires_at
        self.db.commit()
        
        return otp

    def verify_email_with_otp(self, email: str, otp: str) -> User:
        """
        Verify user email using 6-digit OTP.

        Returns:
            Verified user

        Raises:
            UnauthorizedError: If OTP is invalid or expired
            BadRequestError: If email is already verified
        """
        user = self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid OTP")

        if user.email_verified_at:
            raise BadRequestError("Email is already verified")

        if not user.email_verification_otp:
            raise UnauthorizedError("Invalid OTP")

        # Normalize expires_at to timezone-aware for comparison
        expires_at = user.email_verification_otp_expires_at
        if expires_at and expires_at.tzinfo is None:
            # Assume UTC if timezone-naive (from database)
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        if expires_at and expires_at < now:
            user.email_verification_otp = None
            user.email_verification_otp_expires_at = None
            self.db.commit()
            raise UnauthorizedError("OTP has expired")

        if user.email_verification_otp != otp:
            raise UnauthorizedError("Invalid OTP")

        # Verify email and clear OTP
        self.user_repo.verify_email(user)
        user.email_verification_otp = None
        user.email_verification_otp_expires_at = None
        self.db.commit()

        return user

    def send_verification_email(self, email: str) -> None:
        """
        Send verification email with OTP to user.

        Raises:
            BadRequestError: If user not found or email already verified
        """
        user = self.user_repo.get_by_email_with_org(email)
        if not user:
            # Don't reveal if email exists (security)
            return

        if user.email_verified_at:
            raise BadRequestError("Email is already verified")

        otp = self.generate_verification_otp(user)

        # Send email via Resend
        from app.services.resend import send_verification_email as resend_verification_email
        
        user_name = user.full_name if hasattr(user, 'full_name') else user.first_name or "utilisateur"
        resend_verification_email(
            to=user.email,
            otp=otp,
            user_name=user_name,
        )

    def resend_verification_email(self, user: User) -> None:
        """
        Resend verification email with OTP to user.

        Raises:
            BadRequestError: If email is already verified
        """
        if user.email_verified_at:
            raise BadRequestError("Email is already verified")

        otp = self.generate_verification_otp(user)

        # Send email via Resend
        from app.services.resend import send_verification_email as resend_verification_email
        
        user_name = user.full_name if hasattr(user, 'full_name') else user.first_name or "utilisateur"
        resend_verification_email(
            to=user.email,
            otp=otp,
            user_name=user_name,
        )
