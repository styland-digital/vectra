"""Integration tests for emails API endpoints."""

import pytest
from uuid import uuid4
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus
from app.db.models.email import Email, EmailStatus


class TestListEmails:
    """Tests for GET /api/v1/user/emails."""

    def test_list_emails_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should return list of emails."""
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

        email = Email(
            lead_id=lead.id,
            campaign_id=campaign.id,
            subject="Test Email",
            body="Test body",
            status=EmailStatus.PENDING,
        )
        db_session.add(email)
        db_session.commit()

        response = client.get("/api/v1/user/emails", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) >= 1

    def test_list_emails_with_filters(self, client, auth_headers, db_session, test_user, test_organization):
        """Should filter emails by campaign and status."""
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

        email1 = Email(
            lead_id=lead.id,
            campaign_id=campaign.id,
            subject="Email 1",
            body="Body 1",
            status=EmailStatus.PENDING,
        )
        email2 = Email(
            lead_id=lead.id,
            campaign_id=campaign.id,
            subject="Email 2",
            body="Body 2",
            status=EmailStatus.SENT,
        )
        db_session.add_all([email1, email2])
        db_session.commit()

        response = client.get(
            f"/api/v1/user/emails?campaign_id={campaign.id}&status=pending",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(email["status"] == "pending" for email in data["data"])

    def test_list_emails_requires_auth(self, client):
        """Should require authentication."""
        response = client.get("/api/v1/user/emails")

        assert response.status_code == 401


class TestGetEmail:
    """Tests for GET /api/v1/user/emails/{email_id}."""

    def test_get_email_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should return email details."""
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

        email = Email(
            lead_id=lead.id,
            campaign_id=campaign.id,
            subject="Test Email",
            body="Test body",
            status=EmailStatus.PENDING,
        )
        db_session.add(email)
        db_session.commit()

        response = client.get(f"/api/v1/user/emails/{email.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(email.id)
        assert data["subject"] == "Test Email"
        assert "tracking" in data

    def test_get_email_not_found(self, client, auth_headers):
        """Should return 404 if email doesn't exist."""
        response = client.get(f"/api/v1/user/emails/{uuid4()}", headers=auth_headers)

        assert response.status_code == 404


class TestApproveEmail:
    """Tests for POST /api/v1/user/emails/{email_id}/approve."""

    def test_approve_email_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should approve an email."""
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

        email = Email(
            lead_id=lead.id,
            campaign_id=campaign.id,
            subject="Test Email",
            body="Test body",
            status=EmailStatus.PENDING,
        )
        db_session.add(email)
        db_session.commit()

        payload = {
            "modifications": {}
        }

        response = client.post(f"/api/v1/user/emails/{email.id}/approve", json=payload, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"
        assert data["approved_at"] is not None

    def test_approve_email_with_modifications(self, client, auth_headers, db_session, test_user, test_organization):
        """Should approve email with modifications."""
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

        email = Email(
            lead_id=lead.id,
            campaign_id=campaign.id,
            subject="Old Subject",
            body="Old body",
            status=EmailStatus.PENDING,
        )
        db_session.add(email)
        db_session.commit()

        payload = {
            "modifications": {
                "subject": "New Subject",
                "body_html": "New body"
            }
        }

        response = client.post(f"/api/v1/user/emails/{email.id}/approve", json=payload, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"


class TestRejectEmail:
    """Tests for POST /api/v1/user/emails/{email_id}/reject."""

    def test_reject_email_success(self, client, auth_headers, db_session, test_user, test_organization):
        """Should reject an email."""
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

        email = Email(
            lead_id=lead.id,
            campaign_id=campaign.id,
            subject="Test Email",
            body="Test body",
            status=EmailStatus.PENDING,
        )
        db_session.add(email)
        db_session.commit()

        payload = {
            "reason": "Not suitable for this campaign"
        }

        response = client.post(f"/api/v1/user/emails/{email.id}/reject", json=payload, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "rejected"
