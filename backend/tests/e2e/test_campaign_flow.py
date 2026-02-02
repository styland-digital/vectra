"""End-to-end tests for complete campaign flow."""

import pytest
from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus
from app.orchestrator.campaign_runner import CampaignRunner
from tests.conftest import test_organization


@pytest.fixture
def e2e_campaign(db_session, test_organization):
    """Create a campaign for E2E testing."""
    campaign = Campaign(
        organization_id=test_organization.id,
        name="E2E Test Campaign",
        description="E2E test campaign",
        status=CampaignStatus.DRAFT,
        target_criteria={
            "job_titles": ["VP Sales"],
            "geography": ["France"],
            "company_size": ["51-200"],
            "value_prop": "Automatiser votre prospection B2B",
        },
        bant_threshold=60,
        daily_limit=5,
    )
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)
    return campaign


@pytest.mark.e2e
def test_complete_campaign_flow(db_session, e2e_campaign, mock_crew_llm):
    """Test complete campaign flow from start to finish."""
    from unittest.mock import patch, AsyncMock
    
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None):
        
        runner = CampaignRunner(db_session)
        
        # Mock prospector to return test leads
        mock_prospects = [
            {
                "email": "test1@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "job_title": "VP Sales",
                "company_name": "Test Corp",
                "company_size": "51-200",
                "enrichment_data": {},
                "source": "rocketreach",
            }
        ]
        runner.prospector.execute = AsyncMock(return_value={
            "success": True,
            "data": {"prospects": mock_prospects, "total_found": 1}
        })
        
        # Mock BANT to qualify the lead
        runner.bant.execute = AsyncMock(return_value={
            "success": True,
            "data": {
                "qualified": True,
                "bant_score": 75,
                "bant_breakdown": {
                    "budget": {"score": 20},
                    "authority": {"score": 20},
                    "need": {"score": 18},
                    "timeline": {"score": 17},
                }
            }
        })
        
        # Mock scheduler to send email
        runner.scheduler.execute = AsyncMock(return_value={
            "success": True,
            "data": {
                "sent": True,
                "email_id": str(uuid4()),
                "subject": "Test Subject",
            }
        })
        
        # Run campaign
        result = runner.run_campaign(e2e_campaign.id)
        
        # Verify campaign completed
        assert result["success"] is True
        campaign = db_session.query(Campaign).filter(Campaign.id == e2e_campaign.id).first()
        assert campaign.status == CampaignStatus.COMPLETED
        
        # Verify lead was created and processed
        lead = db_session.query(Lead).filter(Lead.campaign_id == e2e_campaign.id).first()
        assert lead is not None
        assert lead.email == "test1@example.com"
        assert lead.status == LeadStatus.CONTACTED


@pytest.mark.e2e
def test_campaign_flow_with_rejection(db_session, e2e_campaign, mock_crew_llm):
    """Test campaign flow where lead is rejected."""
    from unittest.mock import patch, AsyncMock
    
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None):
        
        runner = CampaignRunner(db_session)
        
        # Mock prospector
        mock_prospects = [
            {
                "email": "test2@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "job_title": "Sales Rep",
                "company_name": "Small Corp",
                "company_size": "1-10",
                "enrichment_data": {},
                "source": "rocketreach",
            }
        ]
        runner.prospector.execute = AsyncMock(return_value={
            "success": True,
            "data": {"prospects": mock_prospects, "total_found": 1}
        })
        
        # Mock BANT to reject the lead (low score)
        runner.bant.execute = AsyncMock(return_value={
            "success": True,
            "data": {
                "qualified": False,
                "bant_score": 35,
            }
        })
        
        # Run campaign
        result = runner.run_campaign(e2e_campaign.id)
        
        # Verify lead was rejected
        lead = db_session.query(Lead).filter(Lead.campaign_id == e2e_campaign.id).first()
        assert lead is not None
        assert lead.status == LeadStatus.REJECTED
