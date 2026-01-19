"""Tests for Prospector agent."""

import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
from uuid import uuid4

from app.agents.prospector.agent import ProspectorAgent
from app.services.rocketreach import RocketReachService
from app.services.enrichment import EnrichmentService


@pytest.fixture
def mock_base_config():
    """Mock base agent config."""
    mock_agent = MagicMock()
    with patch('app.agents.crew.get_llm', return_value=None), \
         patch('app.agents.crew.get_memory', return_value=None), \
         patch('app.agents.base.Agent', return_value=mock_agent):
        yield


@pytest.fixture
def mock_rocketreach_service():
    """Mock RocketReach service."""
    service = Mock(spec=RocketReachService)
    service.search_people = AsyncMock(return_value=[
        {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "job_title": "VP Sales",
            "company_name": "Test Corp",
            "company_size": "51-200",
        }
    ])
    return service


@pytest.fixture
def mock_db():
    """Mock database session."""
    return Mock()


@pytest.mark.asyncio
async def test_prospector_execute_success(mock_base_config, mock_rocketreach_service, mock_db):
    """Test prospector agent execution."""
    with patch('app.agents.base.Agent', return_value=MagicMock()):
        agent = ProspectorAgent(db=mock_db, rocketreach_service=mock_rocketreach_service, config={"llm": None, "memory": None})
    
    input_data = {
        "campaign_id": str(uuid4()),
        "organization_id": str(uuid4()),
        "job_titles": ["VP Sales"],
        "limit": 10,
    }
    
    result = await agent.execute(input_data)
    
    assert result["success"] is True
    assert "prospects" in result["data"]
    assert result["data"]["total_found"] >= 0


@pytest.mark.asyncio
async def test_prospector_missing_params(mock_base_config):
    """Test prospector with missing parameters."""
    with patch('app.agents.base.Agent', return_value=MagicMock()):
        agent = ProspectorAgent(config={"llm": None, "memory": None})
    
    result = await agent.execute({})
    
    assert result["success"] is False
    assert "error" in result
