"""Password change service with OTP verification."""

import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, UnauthorizedError
from app.core.security import get_password_hash
from app.db.repositories.user import UserRepository
from app.db.models.user import User
from app.services.resend import send_password_change_otp_email


class PasswordChangeService:
    """Service for password change with OTP verification."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def request_password_change(self, user: User) -> None:
        """
        Request password change by sending OTP to user's email.
        
        Args:
            user: User requesting password change
            
        Raises:
            BadRequestError: If user email not verified
        """
        if not user.email_verified_at:
            raise BadRequestError("Email must be verified before changing password")
        
        # Generate 6-digit OTP
        otp = f"{secrets.randbelow(1000000):06d}"
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        
        # Store OTP in user record
        user.password_change_otp = otp
        user.password_change_otp_expires_at = expires_at
        self.db.commit()
        
        # Send OTP email
        try:
            send_password_change_otp_email(
                to=user.email,
                otp=otp,
                user_name=user.full_name,
            )
        except Exception:
            # Log but don't fail if email sending fails
            from app.core.logging import get_logger
            logger = get_logger(__name__)
            logger.warning(f"Failed to send password change OTP to {user.email}", exc_info=True)

    def change_password_with_otp(
        self,
        user: User,
        otp: str,
        new_password: str,
    ) -> None:
        """
        Change password after OTP verification.
        
        Args:
            user: User changing password
            otp: 6-digit OTP code
            new_password: New password
            
        Raises:
            UnauthorizedError: If OTP is invalid or expired
        """
        if not user.password_change_otp:
            raise UnauthorizedError("Password change OTP not requested")
        
        # Check expiration
        expires_at = user.password_change_otp_expires_at
        if expires_at and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        if not expires_at or expires_at < now:
            # Clear expired OTP
            user.password_change_otp = None
            user.password_change_otp_expires_at = None
            self.db.commit()
            raise UnauthorizedError("Password change OTP has expired")
        
        # Verify OTP
        if user.password_change_otp != otp:
            raise UnauthorizedError("Invalid password change OTP")
        
        # Change password and clear OTP
        password_hash = get_password_hash(new_password)
        self.user_repo.update_password(user, password_hash)
        user.password_change_otp = None
        user.password_change_otp_expires_at = None
        self.db.commit()
