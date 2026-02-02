"""Integration tests for User/Organization API endpoints."""

import pytest
from fastapi import status
from uuid import uuid4


class TestUserMe:
    """Tests for GET /api/v1/user/me endpoint."""

    def test_get_me_success(self, client, auth_headers, test_user):
        """Should return current user profile."""
        response = client.get(
            "/api/v1/user/me",
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(test_user.id)
        assert data["email"] == test_user.email

    def test_get_me_requires_auth(self, client):
        """Unauthenticated request should return 401."""
        response = client.get("/api/v1/user/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestOrganizationMe:
    """Tests for organization endpoints."""

    def test_get_my_organization_success(self, client, auth_headers, test_user, test_organization):
        """Should return user's organization."""
        response = client.get(
            "/api/v1/user/organizations/me",
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(test_organization.id)

    def test_get_my_organization_requires_org_user(self, client, platform_admin_headers):
        """Platform admin should not access organization endpoints."""
        response = client.get(
            "/api/v1/user/organizations/me",
            headers=platform_admin_headers,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_my_organization_as_owner(self, client, db_session, test_organization):
        """Owner should update organization."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash, create_access_token

        owner = User(
            email="owner2@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OWNER,
            is_active=True,
        )
        db_session.add(owner)
        db_session.commit()

        token = create_access_token({
            "sub": str(owner.id),
            "org": str(owner.organization_id),
            "role": owner.role.value,
        })
        headers = {"Authorization": f"Bearer {token}"}

        response = client.patch(
            "/api/v1/user/organizations/me",
            headers=headers,
            json={
                "name": "Updated Org Name",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Org Name"

    def test_update_my_organization_as_operator_raises(self, client, auth_headers, test_user):
        """Operator should not update organization."""
        response = client.patch(
            "/api/v1/user/organizations/me",
            headers=auth_headers,
            json={
                "name": "Should Fail",
            },
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestOrganizationUsers:
    """Tests for organization user management endpoints."""

    def test_list_organization_users_as_owner(self, client, db_session, test_organization):
        """Owner should list organization users."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash, create_access_token

        owner = User(
            email="owner3@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OWNER,
            is_active=True,
        )
        db_session.add(owner)
        db_session.commit()

        token = create_access_token({
            "sub": str(owner.id),
            "org": str(owner.organization_id),
            "role": owner.role.value,
        })
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/v1/user/organizations/me/users",
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.skip(reason="Requires email service mocking")
    def test_invite_user_as_owner(self, client, db_session, test_organization):
        """Owner should invite user."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash, create_access_token

        owner = User(
            email="owner4@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OWNER,
            is_active=True,
        )
        db_session.add(owner)
        db_session.commit()

        token = create_access_token({
            "sub": str(owner.id),
            "org": str(owner.organization_id),
            "role": owner.role.value,
        })
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/v1/user/organizations/me/users/invite",
            headers=headers,
            json={
                "email": "invited@example.com",
                "role": "operator",
            },
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_user_role_as_owner(self, client, db_session, test_organization, test_user):
        """Owner should update user role."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash, create_access_token

        owner = User(
            email="owner5@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OWNER,
            is_active=True,
        )
        db_session.add(owner)
        db_session.commit()

        token = create_access_token({
            "sub": str(owner.id),
            "org": str(owner.organization_id),
            "role": owner.role.value,
        })
        headers = {"Authorization": f"Bearer {token}"}

        response = client.patch(
            f"/api/v1/user/organizations/me/users/{test_user.id}/role",
            headers=headers,
            json={
                "role": "admin",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["role"] == "admin"

    def test_remove_user_as_owner(self, client, db_session, test_organization):
        """Owner should remove user."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash, create_access_token

        owner = User(
            email="owner6@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OWNER,
            is_active=True,
        )
        # Create user to remove
        user_to_remove = User(
            email="toremove@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add_all([owner, user_to_remove])
        db_session.commit()

        token = create_access_token({
            "sub": str(owner.id),
            "org": str(owner.organization_id),
            "role": owner.role.value,
        })
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(
            f"/api/v1/user/organizations/me/users/{user_to_remove.id}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestUserNotifications:
    """Tests for POST /api/v1/user/notifications/send endpoint."""

    @pytest.mark.skip(reason="Requires email service mocking")
    def test_send_notification_org_to_prospects(self, client, db_session, test_organization):
        """Owner should send notification to prospects."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash, create_access_token

        owner = User(
            email="owner7@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OWNER,
            is_active=True,
        )
        db_session.add(owner)
        db_session.commit()

        token = create_access_token({
            "sub": str(owner.id),
            "org": str(owner.organization_id),
            "role": owner.role.value,
        })
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/v1/user/notifications/send",
            headers=headers,
            json={
                "type": "org_to_prospects",
                "recipients": ["prospect@example.com"],
                "subject": "Test Subject",
                "body": "Test Body",
            },
        )

        assert response.status_code == status.HTTP_200_OK
