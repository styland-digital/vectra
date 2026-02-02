"""Integration tests for campaign API endpoints."""

import pytest
from uuid import uuid4
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus


class TestListCampaigns:
    """Tests for GET /api/v1/user/campaigns."""

    def test_list_campaigns_success(self, client, auth_headers, test_user, test_organization):
        """Should return list of campaigns."""
        # Create test campaigns
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        from app.db.base import Base
        from sqlalchemy.orm import Session
        db = client.app.dependency_overrides.get("get_db")
        if db:
            db_session = db()
            db_session.add(campaign)
            db_session.commit()

        response = client.get("/api/v1/user/campaigns", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_list_campaigns_requires_auth(self, client):
        """Should require authentication."""
        response = client.get("/api/v1/user/campaigns")

        assert response.status_code == 401


class TestCreateCampaign:
    """Tests for POST /api/v1/user/campaigns."""

    def test_create_campaign_success(self, client, auth_headers):
        """Should create a new campaign."""
        payload = {
            "name": "New Campaign",
            "description": "Test description",
            "target_criteria": {"job_titles": ["VP Sales"]},
            "bant_threshold": 70,
            "daily_limit": 100,
        }

        response = client.post("/api/v1/user/campaigns", json=payload, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Campaign"
        assert data["status"] == CampaignStatus.DRAFT.value
        assert data["bant_threshold"] == 70

    def test_create_campaign_requires_auth(self, client):
        """Should require authentication."""
        payload = {"name": "New Campaign"}

        response = client.post("/api/v1/user/campaigns", json=payload)

        assert response.status_code == 401


class TestGetCampaign:
    """Tests for GET /api/v1/user/campaigns/{id}."""

    def test_get_campaign_success(self, client, auth_headers, test_user, test_organization):
        """Should return campaign details."""
        # Create test campaign
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        from app.db.base import Base
        from sqlalchemy.orm import Session
        db = client.app.dependency_overrides.get("get_db")
        if db:
            db_session = db()
            db_session.add(campaign)
            db_session.commit()

            response = client.get(f"/api/v1/user/campaigns/{campaign.id}", headers=auth_headers)

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == str(campaign.id)
            assert data["name"] == "Test Campaign"

    def test_get_campaign_not_found(self, client, auth_headers):
        """Should return 404 for non-existent campaign."""
        response = client.get(f"/api/v1/user/campaigns/{uuid4()}", headers=auth_headers)

        assert response.status_code == 404


class TestUpdateCampaign:
    """Tests for PATCH /api/v1/user/campaigns/{id}."""

    def test_update_campaign_success(self, client, auth_headers, test_user, test_organization):
        """Should update draft campaign."""
        # Create test campaign
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Original Name",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        from app.db.base import Base
        from sqlalchemy.orm import Session
        db = client.app.dependency_overrides.get("get_db")
        if db:
            db_session = db()
            db_session.add(campaign)
            db_session.commit()

            payload = {"name": "Updated Name", "bant_threshold": 75}

            response = client.patch(
                f"/api/v1/user/campaigns/{campaign.id}",
                json=payload,
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Updated Name"
            assert data["bant_threshold"] == 75


class TestLaunchCampaign:
    """Tests for POST /api/v1/user/campaigns/{id}/launch."""

    def test_launch_campaign_success(self, client, auth_headers, test_user, test_organization):
        """Should launch a draft campaign."""
        # Create test campaign
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign to Launch",
            status=CampaignStatus.DRAFT,
            target_criteria={"job_titles": ["VP Sales"]},
        )
        from app.db.base import Base
        from sqlalchemy.orm import Session
        db = client.app.dependency_overrides.get("get_db")
        if db:
            db_session = db()
            db_session.add(campaign)
            db_session.commit()

            response = client.post(
                f"/api/v1/user/campaigns/{campaign.id}/launch",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == CampaignStatus.ACTIVE.value
            assert data.get("started_at") is not None


class TestPauseCampaign:
    """Tests for POST /api/v1/user/campaigns/{id}/pause."""

    def test_pause_campaign_success(self, client, auth_headers, test_user, test_organization):
        """Should pause an active campaign."""
        # Create test campaign
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Active Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        from app.db.base import Base
        from sqlalchemy.orm import Session
        db = client.app.dependency_overrides.get("get_db")
        if db:
            db_session = db()
            db_session.add(campaign)
            db_session.commit()

            response = client.post(
                f"/api/v1/user/campaigns/{campaign.id}/pause",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == CampaignStatus.PAUSED.value


class TestDeleteCampaign:
    """Tests for DELETE /api/v1/user/campaigns/{id}."""

    def test_delete_campaign_success(self, client, auth_headers, test_user, test_organization):
        """Should archive a campaign."""
        # Create test campaign
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign to Delete",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        from app.db.base import Base
        from sqlalchemy.orm import Session
        db = client.app.dependency_overrides.get("get_db")
        if db:
            db_session = db()
            db_session.add(campaign)
            db_session.commit()

            response = client.delete(
                f"/api/v1/user/campaigns/{campaign.id}",
                headers=auth_headers
            )

            assert response.status_code == 204


class TestGetCampaignStats:
    """Tests for GET /api/v1/user/campaigns/{id}/stats."""

    def test_get_campaign_stats_success(self, client, auth_headers, test_user, test_organization):
        """Should return campaign statistics."""
        # Create test campaign
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Stats Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
            bant_threshold=60,
        )
        from app.db.base import Base
        from sqlalchemy.orm import Session
        db = client.app.dependency_overrides.get("get_db")
        if db:
            db_session = db()
            db_session.add(campaign)
            db_session.commit()

            # Create test leads
            lead1 = Lead(
                campaign_id=campaign.id,
                organization_id=test_organization.id,
                email="lead1@example.com",
                status=LeadStatus.QUALIFIED,
                bant_score=75,
            )
            lead2 = Lead(
                campaign_id=campaign.id,
                organization_id=test_organization.id,
                email="lead2@example.com",
                status=LeadStatus.REJECTED,
                bant_score=40,
            )
            db_session.add_all([lead1, lead2])
            db_session.commit()

            response = client.get(
                f"/api/v1/user/campaigns/{campaign.id}/stats",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["campaign_id"] == str(campaign.id)
            assert data["leads"]["total"] == 2
            assert data["leads"]["qualified"] == 1
            assert data["leads"]["rejected"] == 1
