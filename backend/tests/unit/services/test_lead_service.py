"""Unit tests for LeadService."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone
from app.services.lead import LeadService
from app.core.exceptions import BadRequestError, NotFoundError
from app.db.models.lead import Lead, LeadStatus, LeadIntent
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.email import Email, EmailStatus
from app.db.models.meeting import Meeting, MeetingStatus


class TestListLeads:
    """Tests for LeadService.list_leads method."""

    def test_list_leads_success(self, db_session, test_user, test_organization):
        """Should return list of leads for organization."""
        # Create test campaign
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        # Create test leads
        lead1 = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead1@example.com",
            first_name="Lead",
            last_name="One",
            status=LeadStatus.NEW,
            bant_score=75,
            enrichment_data={},
        )
        lead2 = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead2@example.com",
            first_name="Lead",
            last_name="Two",
            status=LeadStatus.QUALIFIED,
            bant_score=80,
            enrichment_data={},
        )
        db_session.add_all([lead1, lead2])
        db_session.commit()

        service = LeadService(db_session)
        leads, total = service.list_leads(user=test_user)

        assert len(leads) == 2
        assert total == 2
        assert all(lead.organization_id == test_organization.id for lead in leads)

    def test_list_leads_with_campaign_filter(self, db_session, test_user, test_organization):
        """Should filter leads by campaign."""
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

        service = LeadService(db_session)
        leads, total = service.list_leads(user=test_user, campaign_id=campaign1.id)

        assert len(leads) == 1
        assert leads[0].campaign_id == campaign1.id

    def test_list_leads_with_status_filter(self, db_session, test_user, test_organization):
        """Should filter leads by status."""
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

        service = LeadService(db_session)
        leads, total = service.list_leads(user=test_user, status_filter="qualified")

        assert len(leads) == 1
        assert leads[0].status == LeadStatus.QUALIFIED

    def test_list_leads_with_bant_score_filter(self, db_session, test_user, test_organization):
        """Should filter leads by BANT score range."""
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
            bant_score=50,
            enrichment_data={},
        )
        lead2 = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="lead2@example.com",
            status=LeadStatus.NEW,
            bant_score=75,
            enrichment_data={},
        )
        db_session.add_all([lead1, lead2])
        db_session.commit()

        service = LeadService(db_session)
        leads, total = service.list_leads(user=test_user, bant_score_min=60, bant_score_max=80)

        assert len(leads) == 1
        assert leads[0].bant_score == 75

    def test_list_leads_with_search(self, db_session, test_user, test_organization):
        """Should search leads by name, email, or company."""
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
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            company_name="Acme Corp",
            enrichment_data={},
        )
        lead2 = Lead(
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            email="jane@example.com",
            first_name="Jane",
            last_name="Smith",
            company_name="Tech Inc",
            enrichment_data={},
        )
        db_session.add_all([lead1, lead2])
        db_session.commit()

        service = LeadService(db_session)
        leads, total = service.list_leads(user=test_user, search="Acme")

        assert len(leads) == 1
        assert leads[0].company_name == "Acme Corp"

    def test_list_leads_without_organization_raises(self, db_session):
        """Should raise BadRequestError if user has no organization."""
        from app.db.models.user import User, UserRole
        user_no_org = User(
            email="noorg@example.com",
            password_hash="hash",
            organization_id=None,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add(user_no_org)
        db_session.commit()

        service = LeadService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.list_leads(user=user_no_org)

        assert "does not belong to an organization" in str(exc_info.value.detail)


class TestGetLead:
    """Tests for LeadService.get_lead method."""

    def test_get_lead_success(self, db_session, test_user, test_organization):
        """Should return lead by ID with relationships."""
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

        service = LeadService(db_session)
        result = service.get_lead(user=test_user, lead_id=lead.id)

        assert result.id == lead.id
        assert result.email == "lead@example.com"

    def test_get_lead_not_found_raises(self, db_session, test_user):
        """Should raise NotFoundError if lead doesn't exist."""
        service = LeadService(db_session)

        with pytest.raises(NotFoundError) as exc_info:
            service.get_lead(user=test_user, lead_id=uuid4())

        assert "Lead not found" in str(exc_info.value.detail)


class TestGetLeadInteractions:
    """Tests for LeadService.get_lead_interactions method."""

    def test_get_lead_interactions_includes_emails(self, db_session, test_user, test_organization):
        """Should include emails as interactions."""
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
            status=EmailStatus.SENT,
        )
        db_session.add(email)
        db_session.commit()

        service = LeadService(db_session)
        interactions, total = service.get_lead_interactions(user=test_user, lead_id=lead.id)

        assert total >= 1
        assert any("email" in i["type"] for i in interactions)

    def test_get_lead_interactions_includes_meetings(self, db_session, test_user, test_organization):
        """Should include meetings as interactions."""
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

        meeting = Meeting(
            lead_id=lead.id,
            campaign_id=campaign.id,
            organization_id=test_organization.id,
            scheduled_at=datetime.now(timezone.utc),
            status=MeetingStatus.SCHEDULED,
        )
        db_session.add(meeting)
        db_session.commit()

        service = LeadService(db_session)
        interactions, total = service.get_lead_interactions(user=test_user, lead_id=lead.id)

        assert total >= 1
        assert any("meeting" in i["type"] for i in interactions)


class TestUpdateLead:
    """Tests for LeadService.update_lead method."""

    def test_update_lead_success(self, db_session, test_user, test_organization):
        """Should update lead fields."""
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

        service = LeadService(db_session)
        result = service.update_lead(
            user=test_user,
            lead_id=lead.id,
            first_name="New",
            last_name="Name",
            status="qualified",
        )

        assert result.first_name == "New"
        assert result.last_name == "Name"
        assert result.status == LeadStatus.QUALIFIED

    def test_update_lead_with_notes(self, db_session, test_user, test_organization):
        """Should store notes in enrichment_data."""
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

        service = LeadService(db_session)
        result = service.update_lead(
            user=test_user,
            lead_id=lead.id,
            notes="Test note",
        )
        
        # Refresh to ensure enrichment_data is loaded
        db_session.refresh(result)

        assert result.enrichment_data is not None
        assert result.enrichment_data.get("notes") == "Test note"
