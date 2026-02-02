"""Integration tests for campaign runner."""

import pytest
from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus
from app.orchestrator.campaign_runner import CampaignRunner
from tests.conftest import test_organization
from app.db.models.campaign import Campaign, CampaignStatus


@pytest.fixture
def test_campaign_with_criteria(db_session, test_organization):
    """Create a test campaign with criteria."""
    campaign = Campaign(
        organization_id=test_organization.id,
        name="Test Campaign",
        description="Test campaign description",
        status=CampaignStatus.DRAFT,
        target_criteria={
            "job_titles": ["VP Sales"],
            "geography": ["France"],
            "company_size": ["51-200"],
        },
        bant_threshold=60,
        daily_limit=10,
    )
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)
    return campaign


def test_campaign_runner_initialization(db_session):
    """Test campaign runner initialization."""
    from unittest.mock import patch
    
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None):
        runner = CampaignRunner(db_session)
        assert runner.db == db_session
        assert runner.prospector is not None
        assert runner.bant is not None
        assert runner.scheduler is not None


def test_run_campaign_not_found(db_session):
    """Test running a non-existent campaign."""
    from unittest.mock import patch
    
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None):
        runner = CampaignRunner(db_session)
        result = runner.run_campaign(uuid4())
        
        assert result["success"] is False
        assert "not found" in result["error"].lower()


def test_run_campaign_success(db_session, test_campaign_with_criteria):
    """Test running a campaign successfully."""
    from unittest.mock import patch, AsyncMock
    
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None):
        
        runner = CampaignRunner(db_session)
        
        # Mock agents to return success
        runner.prospector.execute = AsyncMock(return_value={"success": True, "data": {"prospects": [], "total_found": 0}})
        runner.bant.execute = AsyncMock(return_value={"success": True, "data": {"qualified": False, "bant_score": 50}})
        runner.scheduler.execute = AsyncMock(return_value={"success": True, "data": {"sent": False}})
        
        result = runner.run_campaign(test_campaign_with_criteria.id)
        
        # Campaign should be marked as completed
        campaign = db_session.query(Campaign).filter(Campaign.id == test_campaign_with_criteria.id).first()
        assert campaign.status == CampaignStatus.COMPLETED
