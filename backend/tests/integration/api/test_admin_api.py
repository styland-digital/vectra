"""Integration tests for Platform Admin API endpoints."""

import pytest
from fastapi import status
from uuid import uuid4


class TestAdminOverview:
    """Tests for GET /api/v1/admin/overview endpoint."""

    def test_get_overview_success(self, client, platform_admin_headers, test_organization, test_user):
        """Platform admin should get overview statistics."""
        response = client.get(
            "/api/v1/admin/overview",
            headers=platform_admin_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_organizations" in data
        assert "total_users" in data
        assert "active_campaigns" in data

    def test_get_overview_requires_platform_admin(self, client, auth_headers):
        """Regular user should not access overview."""
        response = client.get(
            "/api/v1/admin/overview",
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_overview_requires_auth(self, client):
        """Unauthenticated request should return 401."""
        response = client.get("/api/v1/admin/overview")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAdminOrganizations:
    """Tests for organization management endpoints."""

    def test_list_organizations_success(self, client, platform_admin_headers, test_organization):
        """Platform admin should list all organizations."""
        response = client.get(
            "/api/v1/admin/organizations",
            headers=platform_admin_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_organization_success(self, client, platform_admin_headers, test_organization):
        """Platform admin should get organization details."""
        response = client.get(
            f"/api/v1/admin/organizations/{test_organization.id}",
            headers=platform_admin_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(test_organization.id)
        assert data["name"] == test_organization.name

    def test_create_organization_success(self, client, platform_admin_headers):
        """Platform admin should create organization."""
        response = client.post(
            "/api/v1/admin/organizations",
            headers=platform_admin_headers,
            json={
                "name": "New Org",
                "plan": "trial",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "New Org"

    def test_update_organization_success(self, client, platform_admin_headers, test_organization):
        """Platform admin should update organization."""
        response = client.patch(
            f"/api/v1/admin/organizations/{test_organization.id}",
            headers=platform_admin_headers,
            json={
                "name": "Updated Name",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_delete_organization_success(self, client, platform_admin_headers, db_session):
        """Platform admin should delete organization."""
        from app.db.models.organization import Organization, PlanType

        # Create organization to delete
        org = Organization(
            name="To Delete",
            slug="to-delete",
            plan=PlanType.TRIAL,
            settings={},
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        response = client.delete(
            f"/api/v1/admin/organizations/{org.id}",
            headers=platform_admin_headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestAdminUsers:
    """Tests for GET /api/v1/admin/users endpoint."""

    def test_list_users_success(self, client, platform_admin_headers, test_user):
        """Platform admin should list all users."""
        response = client.get(
            "/api/v1/admin/users",
            headers=platform_admin_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_users_with_filters(self, client, platform_admin_headers, test_user):
        """Platform admin should filter users."""
        response = client.get(
            "/api/v1/admin/users",
            headers=platform_admin_headers,
            params={
                "role": "operator",
                "is_active": True,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestAdminSystemMetrics:
    """Tests for GET /api/v1/admin/system/metrics endpoint."""

    def test_get_system_metrics_success(self, client, platform_admin_headers):
        """Platform admin should get system metrics."""
        response = client.get(
            "/api/v1/admin/system/metrics",
            headers=platform_admin_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "api_requests_per_minute" in data
        assert "average_response_time_ms" in data


class TestAdminNotifications:
    """Tests for POST /api/v1/admin/notifications/send endpoint."""

    @pytest.mark.skip(reason="Requires email service mocking")
    def test_send_notification_vectra_to_users(self, client, platform_admin_headers, test_user):
        """Platform admin should send notification to all users."""
        response = client.post(
            "/api/v1/admin/notifications/send",
            headers=platform_admin_headers,
            json={
                "type": "vectra_to_users",
                "recipients": ["all"],
                "subject": "Test Notification",
                "body": "Test body",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
