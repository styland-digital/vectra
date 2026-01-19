"""Tests for BANT agent."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from uuid import uuid4

from app.agents.bant.agent import BANTAgent
from app.services.scoring import BANTScoringService


@pytest.fixture
def mock_db():
    """Mock database session."""
    return Mock()


def test_bant_scoring_service():
    """Test BANT scoring service."""
    service = BANTScoringService()
    
    result = service.calculate_bant_score(
        company_size="51-200",
        job_title="VP Sales",
        industry="Technology",
    )
    
    assert "bant_score" in result
    assert "bant_breakdown" in result
    assert result["bant_score"] >= 0
    assert result["bant_score"] <= 100


@pytest.mark.asyncio
@patch('app.agents.crew.get_llm', return_value=None)
@patch('app.agents.crew.get_memory', return_value=None)
async def test_bant_agent_execute(mock_memory, mock_llm, mock_db):
    """Test BANT agent execution."""
    with patch('app.agents.base.Agent', return_value=MagicMock()):
        agent = BANTAgent(db=mock_db, config={"llm": None, "memory": None})
    
    input_data = {
        "lead_data": {
            "company_size": "51-200",
            "job_title": "VP Sales",
            "company_industry": "Technology",
        },
        "campaign": {
            "product_description": "AI Sales Agents",
            "bant_threshold": 60,
        },
    }
    
    result = await agent.execute(input_data)
    
    assert result["success"] is True
    assert "bant_score" in result["data"]
    assert result["data"]["bant_score"] >= 0
    assert result["data"]["bant_score"] <= 100
