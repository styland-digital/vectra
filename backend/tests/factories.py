"""Test data factories using factory-boy."""

import factory
from uuid import uuid4

from app.db.models.user import User, UserRole
from app.db.models.organization import Organization, PlanType
from app.core.security import get_password_hash


class OrganizationFactory(factory.Factory):
    """Factory for creating Organization test data."""

    class Meta:
        model = Organization

    id = factory.LazyFunction(uuid4)
    name = factory.Sequence(lambda n: f"Test Organization {n}")
    slug = factory.Sequence(lambda n: f"test-org-{n}")
    plan = PlanType.TRIAL
    settings = factory.LazyFunction(dict)


class UserFactory(factory.Factory):
    """Factory for creating User test data."""

    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    password_hash = factory.LazyFunction(lambda: get_password_hash("password123"))
    first_name = "Test"
    last_name = "User"
    role = UserRole.OPERATOR
    is_active = True
    organization_id = None  # Must be set when creating

    @classmethod
    def create_with_org(cls, db_session, **kwargs):
        """Create user with a new organization."""
        org = OrganizationFactory()
        db_session.add(org)
        db_session.commit()

        user = cls(organization_id=org.id, **kwargs)
        db_session.add(user)
        db_session.commit()
        return user, org


class AdminUserFactory(UserFactory):
    """Factory for creating admin users."""

    role = UserRole.ADMIN


class OwnerUserFactory(UserFactory):
    """Factory for creating owner users."""

    role = UserRole.OWNER
