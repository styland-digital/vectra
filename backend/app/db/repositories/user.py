"""User repository for database operations."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.db.models.user import User
from app.db.models.organization import Organization


class UserRepository:
    """Repository for User CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_id_with_org(self, user_id: UUID) -> Optional[User]:
        """Get user by ID with organization eagerly loaded."""
        return (
            self.db.query(User)
            .options(joinedload(User.organization))
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_email_with_org(self, email: str) -> Optional[User]:
        """Get user by email with organization eagerly loaded."""
        return (
            self.db.query(User)
            .options(joinedload(User.organization))
            .filter(User.email == email)
            .first()
        )

    def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        return self.db.query(User).filter(User.email == email).first() is not None

    def create(
        self,
        email: str,
        password_hash: str,
        organization_id: UUID,
        first_name: str,
        last_name: str,
        role: str = "operator",
    ) -> User:
        """Create a new user."""
        from app.db.models.user import UserRole

        user = User(
            email=email,
            password_hash=password_hash,
            organization_id=organization_id,
            first_name=first_name,
            last_name=last_name,
            role=UserRole(role),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_last_login(self, user: User) -> None:
        """Update user's last login timestamp."""
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

    def update_password(self, user: User, password_hash: str) -> None:
        """Update user's password."""
        user.password_hash = password_hash
        self.db.commit()

    def verify_email(self, user: User) -> None:
        """Mark user's email as verified."""
        user.email_verified_at = datetime.now(timezone.utc)
        self.db.commit()

    def deactivate(self, user: User) -> None:
        """Deactivate a user."""
        user.is_active = False
        self.db.commit()

    def activate(self, user: User) -> None:
        """Activate a user."""
        user.is_active = True
        self.db.commit()

    def list_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """List users in an organization."""
        return (
            self.db.query(User)
            .filter(User.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
