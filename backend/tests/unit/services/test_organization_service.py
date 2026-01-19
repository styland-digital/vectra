"""Unit tests for OrganizationService."""

import pytest
from uuid import uuid4
from fastapi import HTTPException, status
from app.services.organization import OrganizationService
from app.core.exceptions import NotFoundError, BadRequestError
from app.db.models.user import User, UserRole


class TestGetMyOrganization:
    """Tests for OrganizationService.get_my_organization method."""

    def test_get_my_organization_success(self, db_session, test_user, test_organization):
        """Should return user's organization."""
        service = OrganizationService(db_session)
        org = service.get_my_organization(test_user)

        assert org.id == test_organization.id
        assert org.name == test_organization.name

    def test_get_my_organization_no_org_raises(self, db_session):
        """User without organization should raise NotFoundError."""
        # Create platform admin (no organization)
        platform_admin = User(
            email="admin@vectra.io",
            password_hash="hash",
            organization_id=None,
            role=UserRole.PLATFORM_ADMIN,
            is_active=True,
        )
        db_session.add(platform_admin)
        db_session.commit()

        service = OrganizationService(db_session)

        with pytest.raises(NotFoundError) as exc_info:
            service.get_my_organization(platform_admin)

        assert "does not belong" in str(exc_info.value.detail).lower()


class TestUpdateMyOrganization:
    """Tests for OrganizationService.update_my_organization method."""

    def test_update_my_organization_name_as_owner(self, db_session, test_owner_user, test_organization):
        """Owner should be able to update organization name."""
        service = OrganizationService(db_session)
        org = service.update_my_organization(
            user=test_owner_user,
            name="Updated Name",
        )

        assert org.name == "Updated Name"

    def test_update_my_organization_name_as_admin(self, db_session, test_admin_user, test_organization):
        """Admin should be able to update organization name."""
        service = OrganizationService(db_session)
        org = service.update_my_organization(
            user=test_admin_user,
            name="Updated By Admin",
        )

        assert org.name == "Updated By Admin"

    def test_update_my_organization_as_operator_raises(self, db_session, test_user, test_organization):
        """Operator should not be able to update organization."""
        service = OrganizationService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.update_my_organization(
                user=test_user,
                name="Should Fail",
            )

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Owner/Admin" in str(exc_info.value.detail)

    def test_update_my_organization_settings(self, db_session, test_owner_user, test_organization):
        """Should update organization settings."""
        service = OrganizationService(db_session)
        new_settings = {"timezone": "EST", "language": "en"}
        org = service.update_my_organization(
            user=test_owner_user,
            settings=new_settings,
        )

        assert org.settings == new_settings


class TestListUsers:
    """Tests for OrganizationService.list_users method."""

    def test_list_users_as_owner(self, db_session, test_owner_user, test_organization):
        """Owner should be able to list users."""
        # Create additional users
        user1 = User(
            email="user1@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add(user1)
        db_session.commit()

        service = OrganizationService(db_session)
        users = service.list_users(user=test_owner_user)

        assert len(users) >= 1

    def test_list_users_as_manager(self, db_session, test_organization):
        """Manager should be able to list users."""
        manager = User(
            email="manager@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.MANAGER,
            is_active=True,
        )
        db_session.add(manager)
        db_session.commit()

        service = OrganizationService(db_session)
        users = service.list_users(user=manager)

        assert len(users) >= 0

    def test_list_users_as_operator_raises(self, db_session, test_user, test_organization):
        """Operator should not be able to list users."""
        service = OrganizationService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.list_users(user=test_user)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "permissions" in str(exc_info.value.detail).lower()


class TestUpdateUserRole:
    """Tests for OrganizationService.update_user_role method."""

    def test_update_user_role_as_owner(self, db_session, test_owner_user, test_user, test_organization):
        """Owner should be able to update user roles."""
        service = OrganizationService(db_session)
        updated_user = service.update_user_role(
            user=test_owner_user,
            target_user_id=test_user.id,
            new_role="admin",
        )

        assert updated_user.role == UserRole.ADMIN

    def test_update_user_role_as_admin(self, db_session, test_admin_user, test_user, test_organization):
        """Admin should be able to update user roles."""
        service = OrganizationService(db_session)
        updated_user = service.update_user_role(
            user=test_admin_user,
            target_user_id=test_user.id,
            new_role="manager",
        )

        assert updated_user.role == UserRole.MANAGER

    def test_update_user_role_as_operator_raises(self, db_session, test_user, test_organization):
        """Operator should not be able to update roles."""
        # Create another user
        other_user = User(
            email="other@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add(other_user)
        db_session.commit()

        service = OrganizationService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.update_user_role(
                user=test_user,
                target_user_id=other_user.id,
                new_role="admin",
            )
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    def test_update_owner_role_raises(self, db_session, test_owner_user, test_admin_user):
        """Should not allow changing Owner role."""
        service = OrganizationService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.update_user_role(
                user=test_admin_user,
                target_user_id=test_owner_user.id,
                new_role="admin",
            )

        assert "Cannot change Owner role" in str(exc_info.value.detail)

    def test_assign_owner_role_as_admin_raises(self, db_session, test_admin_user, test_user):
        """Non-owner should not be able to assign Owner role."""
        service = OrganizationService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.update_user_role(
                user=test_admin_user,
                target_user_id=test_user.id,
                new_role="owner",
            )

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Only Owner" in str(exc_info.value.detail)

    def test_update_user_role_invalid_role_raises(self, db_session, test_owner_user, test_user):
        """Invalid role should raise BadRequestError."""
        service = OrganizationService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.update_user_role(
                user=test_owner_user,
                target_user_id=test_user.id,
                new_role="invalid_role",
            )

        assert "Invalid role" in str(exc_info.value.detail)


class TestRemoveUser:
    """Tests for OrganizationService.remove_user method."""

    def test_remove_user_as_owner(self, db_session, test_owner_user, test_user, test_organization):
        """Owner should be able to remove users."""
        service = OrganizationService(db_session)
        user_id = test_user.id

        service.remove_user(
            user=test_owner_user,
            target_user_id=user_id,
        )

        # Verify user is removed (organization_id set to None)
        db_session.refresh(test_user)
        assert test_user.organization_id is None

    def test_remove_owner_raises(self, db_session, test_owner_user, test_organization):
        """Should not allow removing Owner."""
        service = OrganizationService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.remove_user(
                user=test_owner_user,
                target_user_id=test_owner_user.id,  # Trying to remove self
            )

        assert "Cannot remove Owner" in str(exc_info.value.detail)

    def test_remove_user_as_operator_raises(self, db_session, test_user, test_organization):
        """Operator should not be able to remove users."""
        # Create another user
        other_user = User(
            email="other@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add(other_user)
        db_session.commit()

        service = OrganizationService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.remove_user(
                user=test_user,
                target_user_id=other_user.id,
            )
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
