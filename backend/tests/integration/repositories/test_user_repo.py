"""Integration tests for UserRepository."""

import pytest
from uuid import uuid4

from app.db.repositories.user import UserRepository
from app.db.models.user import User, UserRole
from app.core.security import get_password_hash


class TestUserRepository:
    """Tests for UserRepository CRUD operations."""

    def test_get_by_id_found(self, db_session, test_user):
        """Should return user when ID exists."""
        repo = UserRepository(db_session)

        user = repo.get_by_id(test_user.id)

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_by_id_not_found(self, db_session):
        """Should return None when ID doesn't exist."""
        repo = UserRepository(db_session)

        user = repo.get_by_id(uuid4())

        assert user is None

    def test_get_by_id_with_org(self, db_session, test_user):
        """Should return user with organization loaded."""
        repo = UserRepository(db_session)

        user = repo.get_by_id_with_org(test_user.id)

        assert user is not None
        assert user.organization is not None
        assert user.organization.name == "Test Organization"

    def test_get_by_email_found(self, db_session, test_user):
        """Should return user when email exists."""
        repo = UserRepository(db_session)

        user = repo.get_by_email("test@example.com")

        assert user is not None
        assert user.email == "test@example.com"

    def test_get_by_email_not_found(self, db_session):
        """Should return None when email doesn't exist."""
        repo = UserRepository(db_session)

        user = repo.get_by_email("nonexistent@example.com")

        assert user is None

    def test_get_by_email_with_org(self, db_session, test_user):
        """Should return user with organization loaded."""
        repo = UserRepository(db_session)

        user = repo.get_by_email_with_org("test@example.com")

        assert user is not None
        assert user.organization is not None

    def test_email_exists_true(self, db_session, test_user):
        """Should return True when email exists."""
        repo = UserRepository(db_session)

        exists = repo.email_exists("test@example.com")

        assert exists is True

    def test_email_exists_false(self, db_session):
        """Should return False when email doesn't exist."""
        repo = UserRepository(db_session)

        exists = repo.email_exists("nonexistent@example.com")

        assert exists is False

    def test_create_user(self, db_session, test_organization):
        """Should create a new user."""
        repo = UserRepository(db_session)

        user = repo.create(
            email="newuser@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            first_name="New",
            last_name="User",
            role="operator",
        )

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.first_name == "New"
        assert user.role == UserRole.OPERATOR

    def test_create_user_with_admin_role(self, db_session, test_organization):
        """Should create a user with admin role."""
        repo = UserRepository(db_session)

        user = repo.create(
            email="admin@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            first_name="Admin",
            last_name="User",
            role="admin",
        )

        assert user.role == UserRole.ADMIN

    def test_update_last_login(self, db_session, test_user):
        """Should update last_login_at timestamp."""
        repo = UserRepository(db_session)
        assert test_user.last_login_at is None

        repo.update_last_login(test_user)

        db_session.refresh(test_user)
        assert test_user.last_login_at is not None

    def test_update_password(self, db_session, test_user):
        """Should update password hash."""
        repo = UserRepository(db_session)
        old_hash = test_user.password_hash
        new_hash = get_password_hash("newpassword456")

        repo.update_password(test_user, new_hash)

        db_session.refresh(test_user)
        assert test_user.password_hash != old_hash
        assert test_user.password_hash == new_hash

    def test_deactivate_user(self, db_session, test_user):
        """Should set is_active to False."""
        repo = UserRepository(db_session)
        assert test_user.is_active is True

        repo.deactivate(test_user)

        db_session.refresh(test_user)
        assert test_user.is_active is False

    def test_activate_user(self, db_session, inactive_user):
        """Should set is_active to True."""
        repo = UserRepository(db_session)
        assert inactive_user.is_active is False

        repo.activate(inactive_user)

        db_session.refresh(inactive_user)
        assert inactive_user.is_active is True

    def test_verify_email(self, db_session, test_user):
        """Should set email_verified_at timestamp."""
        repo = UserRepository(db_session)
        assert test_user.email_verified_at is None

        repo.verify_email(test_user)

        db_session.refresh(test_user)
        assert test_user.email_verified_at is not None

    def test_list_by_organization(self, db_session, test_organization):
        """Should return users in organization."""
        repo = UserRepository(db_session)

        # Create multiple users
        for i in range(3):
            repo.create(
                email=f"user{i}@example.com",
                password_hash=get_password_hash("password123"),
                organization_id=test_organization.id,
                first_name=f"User{i}",
                last_name="Test",
            )

        users = repo.list_by_organization(test_organization.id)

        assert len(users) == 3

    def test_list_by_organization_with_pagination(self, db_session, test_organization):
        """Should support pagination."""
        repo = UserRepository(db_session)

        # Create 5 users
        for i in range(5):
            repo.create(
                email=f"paginated{i}@example.com",
                password_hash=get_password_hash("password123"),
                organization_id=test_organization.id,
                first_name=f"User{i}",
                last_name="Test",
            )

        # Get first page
        users_page1 = repo.list_by_organization(test_organization.id, skip=0, limit=2)
        assert len(users_page1) == 2

        # Get second page
        users_page2 = repo.list_by_organization(test_organization.id, skip=2, limit=2)
        assert len(users_page2) == 2

        # Pages should have different users
        assert users_page1[0].id != users_page2[0].id

    def test_list_by_organization_isolation(self, db_session, test_organization):
        """Should only return users from specified organization."""
        repo = UserRepository(db_session)

        # Create user in test_organization
        repo.create(
            email="org1user@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            first_name="Org1",
            last_name="User",
        )

        # Create another organization with user
        from app.db.models.organization import Organization, PlanType
        other_org = Organization(
            name="Other Org",
            slug="other-org",
            plan=PlanType.TRIAL,
            settings={},
        )
        db_session.add(other_org)
        db_session.commit()

        repo.create(
            email="org2user@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=other_org.id,
            first_name="Org2",
            last_name="User",
        )

        # Should only return users from test_organization
        users = repo.list_by_organization(test_organization.id)
        assert len(users) == 1
        assert users[0].email == "org1user@example.com"
