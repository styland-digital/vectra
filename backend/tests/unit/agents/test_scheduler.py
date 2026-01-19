"""Tests for Scheduler agent."""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from uuid import uuid4

from app.agents.scheduler.agent import SchedulerAgent
from app.services.email_generator import EmailGeneratorService
from app.services.calendly import CalendlyService
from app.db.models.lead import Lead, LeadStatus
from app.db.models.email import Email, EmailStatus


@pytest.fixture
def mock_base_config():
    """Mock base agent config."""
    mock_agent = MagicMock()
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None), \
         patch('app.agents.base.Agent', return_value=mock_agent):
        yield


@pytest.fixture
def mock_db():
    """Mock database session."""
    return Mock()


@pytest.fixture
def sample_lead_data():
    """Sample lead data for testing."""
    return {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "job_title": "VP Sales",
        "company_name": "Test Corp",
    }


@pytest.fixture
def sample_campaign_data():
    """Sample campaign data for testing."""
    return {
        "product_description": "AI Sales Agents",
        "value_prop": "Automatiser votre prospection B2B",
        "price_range": "99€-799€/mois",
    }


@pytest.mark.asyncio
async def test_scheduler_agent_execute_generate_only(mock_base_config, mock_db, sample_lead_data, sample_campaign_data):
    """Test scheduler agent execution (generate only, no send)."""
    with patch('app.agents.base.Agent', return_value=MagicMock()):
        agent = SchedulerAgent(db=mock_db, config={"llm": None, "memory": None})
    
    input_data = {
        "lead_data": sample_lead_data,
        "campaign": sample_campaign_data,
        "send_email": False,
    }
    
    result = await agent.execute(input_data)
    
    assert result["success"] is True
    assert "email_id" in result["data"] or result["data"].get("email_id") is None
    assert "subject" in result["data"]
    assert "body" in result["data"]
    assert "calendly_url" in result["data"]
    assert result["data"]["sent"] is False


@pytest.mark.asyncio
async def test_scheduler_agent_execute_with_send(mock_base_config, mock_db, sample_lead_data, sample_campaign_data):
    """Test scheduler agent execution with email sending."""
    with patch('app.services.resend.send_email') as mock_send, \
         patch('app.agents.base.Agent', return_value=MagicMock()):
        mock_send.return_value = {"id": "test_email_id"}
        
        agent = SchedulerAgent(db=mock_db, config={"llm": None, "memory": None})
        
        input_data = {
            "lead_data": sample_lead_data,
            "campaign": sample_campaign_data,
            "send_email": True,
        }
        
        result = await agent.execute(input_data)
        
        assert result["success"] is True
        assert "subject" in result["data"]
        assert "body" in result["data"]


@pytest.mark.asyncio
async def test_scheduler_agent_missing_lead_data(mock_base_config, mock_db):
    """Test scheduler agent with missing lead_data."""
    with patch('app.agents.base.Agent', return_value=MagicMock()):
        agent = SchedulerAgent(db=mock_db, config={"llm": None, "memory": None})
    
    result = await agent.execute({})
    
    assert result["success"] is False
    assert "error" in result


@pytest.mark.asyncio
async def test_scheduler_agent_generates_calendly_link(mock_base_config, mock_db, sample_lead_data, sample_campaign_data):
    """Test that scheduler agent generates Calendly link."""
    with patch('app.agents.base.Agent', return_value=MagicMock()):
        agent = SchedulerAgent(db=mock_db, config={"llm": None, "memory": None})
    
    input_data = {
        "lead_data": sample_lead_data,
        "campaign": sample_campaign_data,
        "send_email": False,
    }
    
    result = await agent.execute(input_data)
    
    assert result["success"] is True
    assert "calendly_url" in result["data"]
    assert "calendly.com" in result["data"]["calendly_url"] or result["data"]["calendly_url"].startswith("http")


def test_scheduler_agent_role():
    """Test scheduler agent role."""
    mock_agent = MagicMock()
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None), \
         patch('app.agents.base.Agent', return_value=mock_agent):
        agent = SchedulerAgent(config={"llm": None, "memory": None})
        assert agent._get_role() == "Email Outreach Specialist"


def test_scheduler_agent_goal():
    """Test scheduler agent goal."""
    mock_agent = MagicMock()
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None), \
         patch('app.agents.base.Agent', return_value=mock_agent):
        agent = SchedulerAgent(config={"llm": None, "memory": None})
        goal = agent._get_goal()
        assert "email" in goal.lower() or "email" in goal
        assert "personnalisé" in goal.lower() or "personnalisé" in goal
