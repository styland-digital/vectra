"""Unit tests for CampaignService."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone
from app.services.campaign import CampaignService
from app.core.exceptions import BadRequestError, NotFoundError
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus


class TestListCampaigns:
    """Tests for CampaignService.list_campaigns method."""

    def test_list_campaigns_success(self, db_session, test_user, test_organization):
        """Should return list of campaigns for organization."""
        # Create test campaigns
        campaign1 = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign 1",
            status=CampaignStatus.DRAFT,
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

        service = CampaignService(db_session)
        campaigns = service.list_campaigns(user=test_user)

        assert len(campaigns) == 2
        # Sorted by created_at desc, so newest first
        campaign_names = [c.name for c in campaigns]
        assert "Campaign 1" in campaign_names
        assert "Campaign 2" in campaign_names

    def test_list_campaigns_with_status_filter(self, db_session, test_user, test_organization):
        """Should filter campaigns by status."""
        campaign1 = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Draft Campaign",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        campaign2 = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Active Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add_all([campaign1, campaign2])
        db_session.commit()

        service = CampaignService(db_session)
        campaigns = service.list_campaigns(user=test_user, status_filter="draft")

        assert len(campaigns) == 1
        assert campaigns[0].status == CampaignStatus.DRAFT


class TestGetCampaign:
    """Tests for CampaignService.get_campaign method."""

    def test_get_campaign_success(self, db_session, test_user, test_organization):
        """Should return campaign by ID."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Test Campaign",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)
        result = service.get_campaign(user=test_user, campaign_id=campaign.id)

        assert result.id == campaign.id
        assert result.name == "Test Campaign"

    def test_get_campaign_not_found_raises(self, db_session, test_user):
        """Should raise NotFoundError if campaign doesn't exist."""
        service = CampaignService(db_session)

        with pytest.raises(NotFoundError) as exc_info:
            service.get_campaign(user=test_user, campaign_id=uuid4())

        assert "Campaign not found" in str(exc_info.value.detail)


class TestCreateCampaign:
    """Tests for CampaignService.create_campaign method."""

    def test_create_campaign_success(self, db_session, test_user, test_organization):
        """Should create a new campaign."""
        service = CampaignService(db_session)
        campaign = service.create_campaign(
            user=test_user,
            name="New Campaign",
            description="Test description",
            target_criteria={"job_titles": ["VP Sales"]},
            bant_threshold=70,
            daily_limit=100,
        )

        assert campaign.id is not None
        assert campaign.name == "New Campaign"
        assert campaign.status == CampaignStatus.DRAFT
        assert campaign.bant_threshold == 70
        assert campaign.daily_limit == 100


class TestUpdateCampaign:
    """Tests for CampaignService.update_campaign method."""

    def test_update_campaign_success(self, db_session, test_user, test_organization):
        """Should update draft campaign."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Original Name",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)
        updated = service.update_campaign(
            user=test_user,
            campaign_id=campaign.id,
            name="Updated Name",
            bant_threshold=75,
        )

        assert updated.name == "Updated Name"
        assert updated.bant_threshold == 75

    def test_update_campaign_non_draft_raises(self, db_session, test_user, test_organization):
        """Should raise BadRequestError for non-draft campaigns."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Active Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.update_campaign(
                user=test_user,
                campaign_id=campaign.id,
                name="Updated Name",
            )

        assert "Can only update DRAFT" in str(exc_info.value.detail)


class TestLaunchCampaign:
    """Tests for CampaignService.launch_campaign method."""

    def test_launch_campaign_success(self, db_session, test_user, test_organization):
        """Should launch a draft campaign."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign to Launch",
            status=CampaignStatus.DRAFT,
            target_criteria={"job_titles": ["VP Sales"]},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)
        launched = service.launch_campaign(user=test_user, campaign_id=campaign.id)

        assert launched.status == CampaignStatus.ACTIVE
        assert launched.started_at is not None

    def test_launch_campaign_non_draft_raises(self, db_session, test_user, test_organization):
        """Should raise BadRequestError for non-draft campaigns."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Active Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.launch_campaign(user=test_user, campaign_id=campaign.id)

        assert "Can only launch DRAFT" in str(exc_info.value.detail)

    def test_launch_campaign_no_criteria_raises(self, db_session, test_user, test_organization):
        """Should raise BadRequestError if no target criteria."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign without criteria",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.launch_campaign(user=test_user, campaign_id=campaign.id)

        assert "Target criteria required" in str(exc_info.value.detail)


class TestPauseCampaign:
    """Tests for CampaignService.pause_campaign method."""

    def test_pause_campaign_success(self, db_session, test_user, test_organization):
        """Should pause an active campaign."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Active Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)
        paused = service.pause_campaign(user=test_user, campaign_id=campaign.id)

        assert paused.status == CampaignStatus.PAUSED


class TestResumeCampaign:
    """Tests for CampaignService.resume_campaign method."""

    def test_resume_campaign_success(self, db_session, test_user, test_organization):
        """Should resume a paused campaign."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Paused Campaign",
            status=CampaignStatus.PAUSED,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)
        resumed = service.resume_campaign(user=test_user, campaign_id=campaign.id)

        assert resumed.status == CampaignStatus.ACTIVE


class TestDeleteCampaign:
    """Tests for CampaignService.delete_campaign method."""

    def test_delete_campaign_success(self, db_session, test_user, test_organization):
        """Should archive a campaign."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Campaign to Delete",
            status=CampaignStatus.DRAFT,
            target_criteria={},
        )
        db_session.add(campaign)
        db_session.commit()

        service = CampaignService(db_session)
        service.delete_campaign(user=test_user, campaign_id=campaign.id)

        db_session.refresh(campaign)
        assert campaign.status == CampaignStatus.ARCHIVED


class TestGetCampaignStats:
    """Tests for CampaignService.get_campaign_stats method."""

    def test_get_campaign_stats_success(self, db_session, test_user, test_organization):
        """Should return campaign statistics."""
        campaign = Campaign(
            organization_id=test_organization.id,
            created_by=test_user.id,
            name="Stats Campaign",
            status=CampaignStatus.ACTIVE,
            target_criteria={},
            bant_threshold=60,
        )
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

        service = CampaignService(db_session)
        stats = service.get_campaign_stats(user=test_user, campaign_id=campaign.id)

        assert stats["campaign_id"] == str(campaign.id)
        assert stats["leads"]["total"] == 2
        assert stats["leads"]["qualified"] == 1
        assert stats["leads"]["rejected"] == 1
        assert stats["bant"]["average_score"] == 57.5
        assert stats["bant"]["threshold"] == 60
