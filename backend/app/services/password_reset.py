"""Password reset service for business logic."""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, UnauthorizedError
from app.core.security import (
    create_password_reset_token,
    decode_token,
    get_password_hash,
)
from app.core.config import settings
from app.db.repositories.user import UserRepository
from app.db.models.user import User
from app.services.resend import send_password_reset_email


class PasswordResetService:
    """Service for password reset operations."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def generate_reset_token(self, user: User) -> str:
        """
        Generate a password reset token for a user.

        Returns:
            JWT password reset token (expires in 1 hour)

        Raises:
            BadRequestError: If user not found
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
        }
        return create_password_reset_token(token_data)

    def reset_password_with_token(self, token: str, new_password: str) -> User:
        """
        Reset user password using reset token.

        Returns:
            User with updated password

        Raises:
            UnauthorizedError: If token is invalid or expired
        """
        payload = decode_token(token)

        if not payload:
            raise UnauthorizedError("Invalid or expired reset token")

        if payload.get("type") != "password_reset":
            raise UnauthorizedError("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Invalid token payload")

        user = self.user_repo.get_by_id(UUID(user_id))
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")

        # Update password
        password_hash = get_password_hash(new_password)
        self.user_repo.update_password(user, password_hash)

        return user

    def send_reset_email(self, email: str) -> None:
        """
        Send password reset email to user.

        Raises:
            BadRequestError: If user not found
        """
        user = self.user_repo.get_by_email_with_org(email)
        if not user:
            # Don't reveal if email exists (security)
            return

        if not user.is_active:
            raise BadRequestError("Account is disabled")

        reset_token = self.generate_reset_token(user)
        reset_url = f"{settings.APP_URL}/reset-password?token={reset_token}"

        # Send email via Resend
        user_name = user.full_name if hasattr(user, 'full_name') else user.first_name or "utilisateur"
        send_password_reset_email(
            to=user.email,
            reset_url=reset_url,
            user_name=user_name,
        )
