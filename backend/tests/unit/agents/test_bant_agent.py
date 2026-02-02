"""Unit tests for BANT Agent."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from uuid import uuid4

from app.agents.bant.agent import BANTAgent
from app.db.models.lead import Lead, LeadStatus


class TestBANTAgent:
    """Test BANT Agent functionality."""

    @pytest.fixture
    def bant_agent(self):
        """BANT Agent instance with mocked dependencies."""
        with patch('app.services.scoring.BANTScoringService') as mock_scoring:
            agent = BANTAgent()
            agent.scoring_service = mock_scoring.return_value
            return agent

    @pytest.mark.asyncio
    async def test_execute_success_qualified_lead(self, bant_agent):
        """Test successful BANT qualification for a qualified lead."""
        
        # Mock scoring service response
        bant_agent.scoring_service.calculate_bant_score.return_value = {
            "bant_score": 75,
            "bant_breakdown": {
                "budget": 20,
                "authority": 25,
                "need": 15,
                "timeline": 15
            },
            "qualified": True,
            "recommendation": "High priority prospect"
        }

        input_data = {
            "lead_data": {
                "email": "john.doe@techcorp.com",
                "job_title": "CTO",
                "company_name": "TechCorp",
                "company_size": "200-1000"
            },
            "campaign": {
                "product_description": "AI sales automation",
                "bant_threshold": 60
            }
        }

        result = await bant_agent.execute(input_data)

        # Verify successful result
        assert result["success"] is True
        data = result["data"]
        assert data["bant_score"] == 75
        assert data["qualified"] is True

    def test_agent_info(self, bant_agent):
        """Test agent info retrieval."""
        info = bant_agent.get_agent_info()
        assert info["name"] == "BANTAgent"
