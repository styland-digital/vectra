"""Unit tests for CampaignOrchestrator."""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from uuid import uuid4

from app.agents.orchestrator import CampaignOrchestrator
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus


class TestCampaignOrchestrator:
    """Test CampaignOrchestrator functionality."""

    @pytest.fixture
    def db_session(self):
        """Mock database session."""
        return Mock()

    @pytest.fixture
    def organization_id(self):
        """Test organization ID."""
        return uuid4()

    @pytest.fixture
    def campaign_id(self):
        """Test campaign ID."""
        return uuid4()

    @pytest.fixture
    def sample_campaign(self, campaign_id, organization_id):
        """Sample campaign for testing."""
        return Mock(
            id=campaign_id,
            organization_id=organization_id,
            name="Test Campaign",
            description="Test campaign for prospection",
            target_criteria={
                "job_titles": ["CTO", "VP Engineering"],
                "industries": ["Technology"],
                "company_sizes": ["100-1000"],
                "locations": ["France"],
                "limit": 10
            },
            status=CampaignStatus.DRAFT,
            started_at=None,
            completed_at=None
        )

    @pytest.fixture
    def orchestrator(self, db_session, organization_id):
        """CampaignOrchestrator instance with mocked dependencies."""
        with patch('app.agents.orchestrator.ProspectorAgent') as mock_prospector, \
             patch('app.agents.orchestrator.BANTAgent') as mock_bant, \
             patch('app.agents.orchestrator.SchedulerAgent') as mock_scheduler, \
             patch('app.agents.orchestrator.AnalyticsService') as mock_analytics:

            orchestrator = CampaignOrchestrator(
                db=db_session,
                organization_id=organization_id
            )

            # Setup mocks
            orchestrator.prospector = Mock()
            orchestrator.prospector.execute = AsyncMock()

            orchestrator.bant = Mock()
            orchestrator.bant.execute = AsyncMock()

            orchestrator.scheduler = Mock()
            orchestrator.scheduler.execute = AsyncMock()

            orchestrator.analytics = Mock()
            orchestrator.analytics.track_event = AsyncMock()

            return orchestrator

    @pytest.mark.asyncio
    async def test_run_campaign_success(
        self, orchestrator, db_session, campaign_id, sample_campaign
    ):
        """Test successful campaign execution."""
        # Setup database query mock
        db_session.query.return_value.filter.return_value.first.return_value = sample_campaign

        # Mock prospector response
        prospects_data = [
            {
                "email": "john@company.com",
                "first_name": "John",
                "last_name": "Doe",
                "company_name": "Tech Corp",
                "job_title": "CTO",
                "firmographic_score": 85
            },
            {
                "email": "jane@startup.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "company_name": "Startup Inc",
                "job_title": "VP Engineering",
                "firmographic_score": 75
            }
        ]

        orchestrator.prospector.execute.return_value = {
            "success": True,
            "data": {"prospects": prospects_data}
        }

        # Mock leads query for BANT qualification
        mock_leads = [
            Mock(
                id=uuid4(),
                campaign_id=campaign_id,
                email="john@company.com",
                first_name="John",
                last_name="Doe",
                company_name="Tech Corp",
                job_title="CTO",
                status=LeadStatus.PROSPECTED,
                enrichment_data={}
            ),
            Mock(
                id=uuid4(),
                campaign_id=campaign_id,
                email="jane@startup.com",
                first_name="Jane",
                last_name="Smith",
                company_name="Startup Inc",
                job_title="VP Engineering",
                status=LeadStatus.PROSPECTED,
                enrichment_data={}
            )
        ]

        db_session.query.return_value.filter.return_value.all.return_value = mock_leads

        # Mock BANT agent responses
        orchestrator.bant.execute.side_effect = [
            {
                "success": True,
                "data": {
                    "qualified": True,
                    "bant_score": 75,
                    "bant_breakdown": {"budget": 20, "authority": 25, "need": 15, "timeline": 15}
                }
            },
            {
                "success": True,
                "data": {
                    "qualified": True,
                    "bant_score": 68,
                    "bant_breakdown": {"budget": 18, "authority": 20, "need": 15, "timeline": 15}
                }
            }
        ]

        # Mock scheduler agent responses
        orchestrator.scheduler.execute.side_effect = [
            {
                "success": True,
                "data": {
                    "email_id": str(uuid4()),
                    "subject": "Partnership Opportunity - Vectra AI",
                    "body": "<html>Personalized email content</html>",
                    "sent": False
                }
            },
            {
                "success": True,
                "data": {
                    "email_id": str(uuid4()),
                    "subject": "AI Solutions for Startup Inc",
                    "body": "<html>Another personalized email</html>",
                    "sent": False
                }
            }
        ]

        # Execute campaign
        result = await orchestrator.run_campaign(campaign_id)

        # Verify result
        assert result["success"] is True
        data = result["data"]
        assert data["status"] == "completed"
        assert data["prospects_found"] == 2
        assert data["leads_qualified"] == 2
        assert data["qualification_rate"] == 100.0
        assert data["emails_generated"] == 2

        # Verify database operations
        assert db_session.add.call_count >= 2  # At least 2 leads added
        assert db_session.commit.call_count >= 3  # Campaign status updates + leads + emails

        # Verify agent calls
        orchestrator.prospector.execute.assert_called_once()
        assert orchestrator.bant.execute.call_count == 2
        assert orchestrator.scheduler.execute.call_count == 2

        # Verify analytics tracking
        assert orchestrator.analytics.track_event.call_count >= 4  # Start, import, qualified events, complete

    @pytest.mark.asyncio
    async def test_run_campaign_prospection_failure(
        self, orchestrator, db_session, campaign_id, sample_campaign
    ):
        """Test campaign failure during prospection phase."""
        db_session.query.return_value.filter.return_value.first.return_value = sample_campaign

        # Mock prospector failure
        orchestrator.prospector.execute.return_value = {
            "success": False,
            "error": "RocketReach API error"
        }

        # Execute campaign
        result = await orchestrator.run_campaign(campaign_id)

        # Verify failure handling
        assert result["success"] is False
        assert "RocketReach API error" in result["error"]

        # Verify campaign status updated to failed
        assert sample_campaign.status == CampaignStatus.FAILED

    @pytest.mark.asyncio
    async def test_run_campaign_no_prospects_found(
        self, orchestrator, db_session, campaign_id, sample_campaign
    ):
        """Test campaign with no prospects found."""
        db_session.query.return_value.filter.return_value.first.return_value = sample_campaign

        # Mock empty prospects response
        orchestrator.prospector.execute.return_value = {
            "success": True,
            "data": {"prospects": []}
        }

        # Mock empty leads query
        db_session.query.return_value.filter.return_value.all.return_value = []

        # Execute campaign
        result = await orchestrator.run_campaign(campaign_id)

        # Verify result
        assert result["success"] is True
        data = result["data"]
        assert data["prospects_found"] == 0
        assert data["leads_qualified"] == 0
        assert data["emails_generated"] == 0

    @pytest.mark.asyncio
    async def test_run_campaign_no_qualified_leads(
        self, orchestrator, db_session, campaign_id, sample_campaign
    ):
        """Test campaign where no leads qualify (BANT score < 60)."""
        db_session.query.return_value.filter.return_value.first.return_value = sample_campaign

        # Mock prospector with one prospect
        orchestrator.prospector.execute.return_value = {
            "success": True,
            "data": {
                "prospects": [{
                    "email": "lowquality@company.com",
                    "first_name": "Low",
                    "last_name": "Quality",
                    "company_name": "Small Corp",
                    "job_title": "Junior Developer"
                }]
            }
        }

        # Mock lead for BANT qualification
        mock_lead = Mock(
            id=uuid4(),
            campaign_id=campaign_id,
            email="lowquality@company.com",
            first_name="Low",
            last_name="Quality",
            status=LeadStatus.PROSPECTED,
            enrichment_data={}
        )

        db_session.query.return_value.filter.return_value.all.return_value = [mock_lead]

        # Mock BANT agent with low score
        orchestrator.bant.execute.return_value = {
            "success": True,
            "data": {
                "qualified": False,
                "bant_score": 45,
                "bant_breakdown": {"budget": 10, "authority": 15, "need": 10, "timeline": 10}
            }
        }

        # Execute campaign
        result = await orchestrator.run_campaign(campaign_id)

        # Verify result
        assert result["success"] is True
        data = result["data"]
        assert data["prospects_found"] == 1
        assert data["leads_qualified"] == 0
        assert data["qualification_rate"] == 0.0
        assert data["emails_generated"] == 0

        # BANT agent should be called, but scheduler shouldn't
        orchestrator.bant.execute.assert_called_once()
        orchestrator.scheduler.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_campaign_progress(
        self, orchestrator, db_session, campaign_id, sample_campaign
    ):
        """Test getting campaign progress."""
        # Setup campaign
        sample_campaign.status = CampaignStatus.RUNNING
        sample_campaign.started_at = datetime.utcnow()

        db_session.query.return_value.filter.return_value.first.return_value = sample_campaign

        # Setup leads with different statuses
        mock_leads = [
            Mock(status=LeadStatus.PROSPECTED),
            Mock(status=LeadStatus.QUALIFIED),
            Mock(status=LeadStatus.CONTACTED),
            Mock(status=LeadStatus.REJECTED)
        ]

        db_session.query.return_value.filter.return_value.all.return_value = mock_leads

        # Get progress
        result = await orchestrator.get_campaign_progress(campaign_id)

        # Verify result
        assert result["success"] is True
        data = result["data"]
        assert data["campaign_id"] == str(campaign_id)
        assert data["status"] == "running"
        assert data["total_leads"] == 4
        assert data["lead_status_breakdown"]["prospected"] == 1
        assert data["lead_status_breakdown"]["qualified"] == 1
        assert data["lead_status_breakdown"]["contacted"] == 1
        assert data["lead_status_breakdown"]["rejected"] == 1
        assert 0 < data["progress_percentage"] < 100

    @pytest.mark.asyncio
    async def test_campaign_not_found(self, orchestrator, db_session, campaign_id):
        """Test error handling for non-existent campaign."""
        db_session.query.return_value.filter.return_value.first.return_value = None

        result = await orchestrator.run_campaign(campaign_id)

        assert result["success"] is False
        assert "not found" in result["error"]

    @pytest.mark.asyncio
    async def test_bant_agent_partial_failure(
        self, orchestrator, db_session, campaign_id, sample_campaign
    ):
        """Test resilience when BANT agent fails for some leads but not others."""
        db_session.query.return_value.filter.return_value.first.return_value = sample_campaign

        # Mock prospector with two prospects
        orchestrator.prospector.execute.return_value = {
            "success": True,
            "data": {
                "prospects": [
                    {"email": "good@company.com", "first_name": "Good"},
                    {"email": "bad@company.com", "first_name": "Bad"}
                ]
            }
        }

        # Mock two leads
        mock_leads = [
            Mock(id=uuid4(), email="good@company.com", status=LeadStatus.PROSPECTED, enrichment_data={}),
            Mock(id=uuid4(), email="bad@company.com", status=LeadStatus.PROSPECTED, enrichment_data={})
        ]

        db_session.query.return_value.filter.return_value.all.return_value = mock_leads

        # Mock BANT agent: one success, one failure
        orchestrator.bant.execute.side_effect = [
            {"success": True, "data": {"qualified": True, "bant_score": 70}},
            {"success": False, "error": "Processing error"}
        ]

        # Mock scheduler for successful lead
        orchestrator.scheduler.execute.return_value = {
            "success": True,
            "data": {"email_id": str(uuid4()), "subject": "Test", "sent": False}
        }

        # Execute campaign
        result = await orchestrator.run_campaign(campaign_id)

        # Should still succeed with partial results
        assert result["success"] is True
        data = result["data"]
        assert data["prospects_found"] == 2
        assert data["leads_qualified"] == 1  # Only one qualified due to error
        assert data["emails_generated"] == 1

        # Both BANT calls made, but only one scheduler call
        assert orchestrator.bant.execute.call_count == 2
        orchestrator.scheduler.execute.assert_called_once()