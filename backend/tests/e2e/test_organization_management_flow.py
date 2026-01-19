"""E2E tests for organization management flow."""

import pytest
from fastapi import status


class TestOrganizationManagementFlow:
    """E2E tests for organization management functionality."""

    def test_organization_owner_full_flow(self, client, db_session, test_organization):
        """Test complete organization owner flow: login, manage org, invite users, manage members."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash, create_access_token
        
        # Create owner
        owner = User(
            email="owner@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OWNER,
            is_active=True,
        )
        db_session.add(owner)
        db_session.commit()
        
        # Login
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "owner@example.com",
                "password": "password123",
            },
        )
        assert login_response.status_code == status.HTTP_200_OK
        login_data = login_response.json()
        owner_token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {owner_token}"}
        
        # 1. Get my profile
        me_response = client.get("/api/v1/user/me", headers=headers)
        assert me_response.status_code == status.HTTP_200_OK
        me_data = me_response.json()
        assert me_data["role"] == "owner"
        
        # 2. Get my organization
        org_response = client.get("/api/v1/user/organizations/me", headers=headers)
        assert org_response.status_code == status.HTTP_200_OK
        org_data = org_response.json()
        assert org_data["id"] == str(test_organization.id)
        
        # 3. Update organization
        update_response = client.patch(
            "/api/v1/user/organizations/me",
            headers=headers,
            json={
                "name": "Updated Org Name",
            },
        )
        assert update_response.status_code == status.HTTP_200_OK
        updated_org = update_response.json()
        assert updated_org["name"] == "Updated Org Name"
        
        # 4. List organization users
        users_response = client.get(
            "/api/v1/user/organizations/me/users",
            headers=headers,
        )
        assert users_response.status_code == status.HTTP_200_OK
        users = users_response.json()
        assert isinstance(users, list)
        
        # 5. Create regular user for testing role update
        regular_user = User(
            email="regular@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add(regular_user)
        db_session.commit()
        
        # 6. Update user role
        update_role_response = client.patch(
            f"/api/v1/user/organizations/me/users/{regular_user.id}/role",
            headers=headers,
            json={
                "role": "admin",
            },
        )
        assert update_role_response.status_code == status.HTTP_200_OK
        updated_user = update_role_response.json()
        assert updated_user["role"] == "admin"
        
        # 7. Remove user
        remove_response = client.delete(
            f"/api/v1/user/organizations/me/users/{regular_user.id}",
            headers=headers,
        )
        assert remove_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify user is removed
        db_session.refresh(regular_user)
        assert regular_user.organization_id is None
