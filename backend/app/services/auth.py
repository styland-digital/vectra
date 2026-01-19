"""Authentication service for business logic."""

from typing import Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError, BadRequestError
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings
from app.db.repositories.user import UserRepository
from app.db.repositories.organization import OrganizationRepository
from app.db.models.user import User, UserRole
from app.services.email_verification import EmailVerificationService


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.org_repo = OrganizationRepository(db)

    def authenticate(self, email: str, password: str) -> Tuple[str, str, User]:
        """
        Authenticate user with email and password.

        Returns:
            Tuple of (access_token, refresh_token, user)

        Raises:
            UnauthorizedError: If credentials are invalid
        """
        # Try to get user with org first (for regular users)
        user = self.user_repo.get_by_email_with_org(email)
        
        # If not found or is platform admin, try without org
        if not user or (user.organization_id is None):
            user = self.user_repo.get_by_email(email)
            # Reload if needed to get organization relationship
            if user and user.organization_id:
                user = self.user_repo.get_by_id_with_org(user.id)

        if not user:
            raise UnauthorizedError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")

        if not user.is_active:
            raise UnauthorizedError("Account is disabled")

        # Update last login
        self.user_repo.update_last_login(user)

        # Create tokens
        token_data = {
            "sub": str(user.id),
            "role": user.role.value,
        }
        # Only add org to token if user belongs to an organization
        if user.organization_id:
            token_data["org"] = str(user.organization_id)
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return access_token, refresh_token, user

    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Create new access token from refresh token.

        Returns:
            New access token

        Raises:
            UnauthorizedError: If refresh token is invalid
        """
        payload = decode_token(refresh_token)

        if not payload:
            raise UnauthorizedError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid token type")

        # Verify user still exists and is active
        user_id = payload.get("sub")
        user = self.user_repo.get_by_id(UUID(user_id))

        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")

        # Create new access token
        token_data = {
            "sub": str(user.id),
            "role": user.role.value,
        }
        # Only add org to token if user belongs to an organization
        if user.organization_id:
            token_data["org"] = str(user.organization_id)
        return create_access_token(token_data)

    def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        organization_name: str,
    ) -> Tuple[str, str, User]:
        """
        Register a new user with a new organization.
        
        If email matches PLATFORM_ADMIN_EMAIL, creates a platform admin user
        without an organization.

        Returns:
            Tuple of (access_token, refresh_token, user)

        Raises:
            BadRequestError: If email already exists
        """
        # Check if email exists
        if self.user_repo.email_exists(email):
            raise BadRequestError("Email already registered")

        # Check if this is a platform admin registration
        is_platform_admin = email.lower() == settings.PLATFORM_ADMIN_EMAIL.lower()
        
        if is_platform_admin:
            # Create platform admin user without organization
            password_hash = get_password_hash(password)
            user = self.user_repo.create(
                email=email,
                password_hash=password_hash,
                organization_id=None,
                first_name=first_name,
                last_name=last_name,
                role=UserRole.PLATFORM_ADMIN.value,
            )
            # Reload user
            user = self.user_repo.get_by_id(user.id)
        else:
            # Create organization
            org = self.org_repo.create(name=organization_name)

            # Create user as owner
            password_hash = get_password_hash(password)
            user = self.user_repo.create(
                email=email,
                password_hash=password_hash,
                organization_id=org.id,
                first_name=first_name,
                last_name=last_name,
                role="owner",
            )

            # Reload user with organization
            user = self.user_repo.get_by_id_with_org(user.id)

        # Send verification email
        try:
            verification_service = EmailVerificationService(self.db)
            verification_service.send_verification_email(user.email)
        except Exception:
            # Log but don't fail registration if email sending fails
            from app.core.logging import get_logger
            logger = get_logger(__name__)
            logger.warning(f"Failed to send verification email to {user.email}", exc_info=True)

        # Create tokens
        token_data = {
            "sub": str(user.id),
            "role": user.role.value,
        }
        # Only add org to token if user belongs to an organization
        if user.organization_id:
            token_data["org"] = str(user.organization_id)
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return access_token, refresh_token, user

    def change_password(
        self, user: User, current_password: str, new_password: str
    ) -> None:
        """
        Change user's password.

        Raises:
            UnauthorizedError: If current password is incorrect
        """
        if not verify_password(current_password, user.password_hash):
            raise UnauthorizedError("Current password is incorrect")

        password_hash = get_password_hash(new_password)
        self.user_repo.update_password(user, password_hash)
