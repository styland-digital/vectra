"""E2E tests for platform admin flow."""

import pytest
from fastapi import status


class TestPlatformAdminFlow:
    """E2E tests for platform admin functionality."""

    def test_platform_admin_full_flow(self, client, db_session):
        """Test complete platform admin flow: register, login, create org, manage users."""
        from app.core.config import settings
        from app.core.security import get_password_hash
        from app.db.models.user import User, UserRole
        from app.db.models.organization import Organization, PlanType
        
        # 1. Register as platform admin
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": settings.PLATFORM_ADMIN_EMAIL,
                "password": "password123",
                "first_name": "Platform",
                "last_name": "Admin",
                "organization_name": "Vectra",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        platform_admin_token = data["access_token"]
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        
        # Verify user is platform admin
        user_response = client.get("/api/v1/user/me", headers=headers)
        assert user_response.status_code == status.HTTP_200_OK
        user_data = user_response.json()
        assert user_data["role"] == "platform_admin"
        assert user_data["organization_id"] is None
        
        # 2. Get platform overview
        overview_response = client.get("/api/v1/admin/overview", headers=headers)
        assert overview_response.status_code == status.HTTP_200_OK
        overview_data = overview_response.json()
        assert "total_organizations" in overview_data
        
        # 3. Create organization
        create_org_response = client.post(
            "/api/v1/admin/organizations",
            headers=headers,
            json={
                "name": "Test Organization",
                "plan": "trial",
            },
        )
        assert create_org_response.status_code == status.HTTP_201_CREATED
        org_data = create_org_response.json()
        org_id = org_data["id"]
        
        # 4. List organizations
        list_orgs_response = client.get("/api/v1/admin/organizations", headers=headers)
        assert list_orgs_response.status_code == status.HTTP_200_OK
        orgs = list_orgs_response.json()
        assert len(orgs) >= 1
        
        # 5. Get organization details
        get_org_response = client.get(
            f"/api/v1/admin/organizations/{org_id}",
            headers=headers,
        )
        assert get_org_response.status_code == status.HTTP_200_OK
        
        # 6. Update organization
        update_org_response = client.patch(
            f"/api/v1/admin/organizations/{org_id}",
            headers=headers,
            json={
                "name": "Updated Organization",
            },
        )
        assert update_org_response.status_code == status.HTTP_200_OK
        updated_org = update_org_response.json()
        assert updated_org["name"] == "Updated Organization"
        
        # 7. List users (should be empty initially)
        list_users_response = client.get("/api/v1/admin/users", headers=headers)
        assert list_users_response.status_code == status.HTTP_200_OK
        users = list_users_response.json()
        # Should only show organization users, not platform admin
        assert all(user.get("organization_id") for user in users)
