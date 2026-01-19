"""Unit tests for EmailService."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone
from app.services.email import EmailService
from app.core.exceptions import BadRequestError, NotFoundError
from app.db.models.email import Email, EmailStatus
from app.db.models.lead import Lead, LeadStatus
from app.db.models.campaign import Campaign, CampaignStatus


class TestListEmails:
    """Tests for EmailService.list_emails method."""

    def test_list_emails_success(self, db_session, test_user, test_organization):
        """Should return list of emails for organization."""
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

        service = EmailService(db_session)
        emails, total = service.list_emails(user=test_user)

        assert len(emails) == 2
        assert total == 2

    def test_list_emails_with_campaign_filter(self, db_session, test_user, test_organization):
        """Should filter emails by campaign."""
        campaign1 = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign 1",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        campaign2 = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign 2",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add_all([campaign1, campaign2])
        db_session.commit()

        lead1 = Lead(
            campaign_id=campaign1.id,
            organization_id=test_organization.id,
            email="lead1@example.com",
            status=LeadStatus.NEW,
            enrichment_data={},
        )
        lead2 = Lead(
            campaign_id=campaign2.id,
            organization_id=test_organization.id,
            email="lead2@example.com",
            status=LeadStatus.NEW,
            enrichment_data={},
        )
        db_session.add_all([lead1, lead2])
        db_session.commit()

        email1 = Email(
            lead_id=lead1.id,
            campaign_id=campaign1.id,
            subject="Email 1",
            body="Body 1",
            status=EmailStatus.PENDING,
        )
        email2 = Email(
            lead_id=lead2.id,
            campaign_id=campaign2.id,
            subject="Email 2",
            body="Body 2",
            status=EmailStatus.PENDING,
        )
        db_session.add_all([email1, email2])
        db_session.commit()

        service = EmailService(db_session)
        emails, total = service.list_emails(user=test_user, campaign_id=campaign1.id)

        assert len(emails) == 1
        assert emails[0].campaign_id == campaign1.id

    def test_list_emails_with_status_filter(self, db_session, test_user, test_organization):
        """Should filter emails by status."""
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

        service = EmailService(db_session)
        emails, total = service.list_emails(user=test_user, status_filter="pending")

        assert len(emails) == 1
        assert emails[0].status == EmailStatus.PENDING


class TestGetEmail:
    """Tests for EmailService.get_email method."""

    def test_get_email_success(self, db_session, test_user, test_organization):
        """Should return email by ID with relationships."""
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

        service = EmailService(db_session)
        result = service.get_email(user=test_user, email_id=email.id)

        assert result.id == email.id
        assert result.subject == "Test Email"

    def test_get_email_not_found_raises(self, db_session, test_user):
        """Should raise NotFoundError if email doesn't exist."""
        service = EmailService(db_session)

        with pytest.raises(NotFoundError) as exc_info:
            service.get_email(user=test_user, email_id=uuid4())

        assert "Email not found" in str(exc_info.value.detail)


class TestApproveEmail:
    """Tests for EmailService.approve_email method."""

    def test_approve_email_success(self, db_session, test_user, test_organization):
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

        service = EmailService(db_session)
        result = service.approve_email(user=test_user, email_id=email.id)

        assert result.status == EmailStatus.APPROVED
        assert result.approved_by == test_user.id
        assert result.approved_at is not None

    def test_approve_email_with_modifications(self, db_session, test_user, test_organization):
        """Should approve email with subject/body modifications."""
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

        service = EmailService(db_session)
        result = service.approve_email(
            user=test_user,
            email_id=email.id,
            subject="New Subject",
            body_html="New body",
        )

        assert result.status == EmailStatus.APPROVED
        assert result.subject == "New Subject"
        assert result.body == "New body"

    def test_approve_email_not_pending_raises(self, db_session, test_user, test_organization):
        """Should raise BadRequestError if email is not pending."""
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
            status=EmailStatus.APPROVED,
        )
        db_session.add(email)
        db_session.commit()

        service = EmailService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.approve_email(user=test_user, email_id=email.id)

        assert "Cannot approve email with status" in str(exc_info.value.detail)


class TestRejectEmail:
    """Tests for EmailService.reject_email method."""

    def test_reject_email_success(self, db_session, test_user, test_organization):
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

        service = EmailService(db_session)
        result = service.reject_email(user=test_user, email_id=email.id, reason="Not suitable")

        assert result.status == EmailStatus.REJECTED

    def test_reject_email_not_pending_raises(self, db_session, test_user, test_organization):
        """Should raise BadRequestError if email is not pending."""
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
            status=EmailStatus.APPROVED,
        )
        db_session.add(email)
        db_session.commit()

        service = EmailService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.reject_email(user=test_user, email_id=email.id, reason="Test")

        assert "Cannot reject email with status" in str(exc_info.value.detail)
