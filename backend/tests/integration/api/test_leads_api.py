"""Integration tests for leads API endpoints."""

import pytest
from uuid import uuid4
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus


class TestListLeads:
    """Tests for GET /api/v1/user/leads."""

    def test_list_leads_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should return list of leads."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        lead = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead@example.com",
            first_name="Test",
            last_name="Lead",
            status=LeadStatus.NEW,
            bant_score=75,
            enrichment_data={},
        )
        db_session.add(lead)
        db_session.commit()

        response = client.get("/api/v1/user/leads", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) >= 1

    def test_list_leads_with_filters(self, client, auth_headers, db_session, test_user, test_organization):
        """Should filter leads by campaign and status."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        lead1 = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead1@example.com",
            status=LeadStatus.NEW,
            enrichment_data={},
        )
        lead2 = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead2@example.com",
            status=LeadStatus.QUALIFIED,
            enrichment_data={},
        )
        db_session.add_all([lead1, lead2])
        db_session.commit()

        response = client.get(
            f"/api/v1/user/leads?campaign_id={campaign.id}&status=qualified",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(lead["status"] == "qualified" for lead in data["data"])

    def test_list_leads_requires_auth(self, client):
        """Should require authentication."""
        response = client.get("/api/v1/user/leads")

        assert response.status_code == 401


class TestGetLead:
    """Tests for GET /api/v1/user/leads/{lead_id}."""

    def test_get_lead_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should return lead details."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        lead = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead@example.com",
            first_name="Test",
            last_name="Lead",
            status=LeadStatus.NEW,
            enrichment_data={},
        )
        db_session.add(lead)
        db_session.commit()

        response = client.get(f"/api/v1/user/leads/{lead.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(lead.id)
        assert data["email"] == "lead@example.com"
        assert "interactions" in data
        assert "emails" in data
        assert "meetings" in data

    def test_get_lead_not_found(self, client, auth_headers):
        """Should return 404 if lead doesn't exist."""
        response = client.get(f"/api/v1/user/leads/{uuid4()}", headers=auth_headers)

        assert response.status_code == 404


class TestGetLeadInteractions:
    """Tests for GET /api/v1/user/leads/{lead_id}/interactions."""

    def test_get_lead_interactions_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should return lead interactions."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        lead = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead@example.com",
            status=LeadStatus.NEW,
            enrichment_data={},
        )
        db_session.add(lead)
        db_session.commit()

        response = client.get(f"/api/v1/user/leads/{lead.id}/interactions", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data


class TestUpdateLead:
    """Tests for PATCH /api/v1/user/leads/{lead_id}."""

    def test_update_lead_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should update lead."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        lead = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead@example.com",
            first_name="Old",
            last_name="Name",
            status=LeadStatus.NEW,
            enrichment_data={},
        )
        db_session.add(lead)
        db_session.commit()

        payload = {
            "first_name": "New",
            "last_name": "Name",
            "status": "qualified",
        }

        response = client.patch(f"/api/v1/user/leads/{lead.id}", json=payload, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "New"
        assert data["last_name"] == "Name"
        assert data["status"] == "qualified"
