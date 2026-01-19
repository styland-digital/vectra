"""Data access repositories."""

from app.db.repositories.user import UserRepository
from app.db.repositories.organization import OrganizationRepository

__all__ = ["UserRepository", "OrganizationRepository"]
