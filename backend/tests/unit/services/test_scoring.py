"""Tests for BANT scoring service."""

import pytest

from app.services.scoring import BANTScoringService


def test_calculate_budget_score():
    """Test budget score calculation."""
    service = BANTScoringService()
    
    score, reasoning = service.calculate_budget_score("51-200")
    assert 0 <= score <= 25
    assert reasoning


def test_calculate_authority_score():
    """Test authority score calculation."""
    service = BANTScoringService()
    
    score, reasoning = service.calculate_authority_score("VP Sales")
    assert 0 <= score <= 25
    assert reasoning


def test_calculate_bant_score_complete():
    """Test complete BANT score calculation."""
    service = BANTScoringService()
    
    result = service.calculate_bant_score(
        company_size="51-200",
        job_title="VP Sales",
        industry="Technology",
    )
    
    assert "bant_score" in result
    assert "bant_breakdown" in result
    assert "qualified" in result
    assert 0 <= result["bant_score"] <= 100
    assert result["bant_score"] == (
        result["bant_breakdown"]["budget"]["score"] +
        result["bant_breakdown"]["authority"]["score"] +
        result["bant_breakdown"]["need"]["score"] +
        result["bant_breakdown"]["timeline"]["score"]
    )
