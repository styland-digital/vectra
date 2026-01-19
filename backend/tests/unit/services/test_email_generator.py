"""Tests for email generator service."""

import pytest

from app.services.email_generator import EmailGeneratorService


@pytest.fixture
def sample_lead_data():
    """Sample lead data for testing."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "job_title": "VP Sales",
        "company_name": "Test Corp",
        "email": "john@testcorp.com",
    }


@pytest.fixture
def sample_campaign_data():
    """Sample campaign data for testing."""
    return {
        "product_description": "AI Sales Agents platform",
        "value_prop": "Automatiser votre prospection B2B",
        "price_range": "99€-799€/mois",
    }


class TestGenerateSubject:
    """Test email subject generation."""

    def test_generate_subject_with_first_name(self, sample_lead_data, sample_campaign_data):
        """Should generate subject with first name."""
        subject = EmailGeneratorService.generate_subject(sample_lead_data, sample_campaign_data)
        
        assert "John" in subject
        assert "Test Corp" in subject or "votre équipe" in subject
        assert sample_campaign_data["value_prop"] in subject

    def test_generate_subject_without_first_name(self, sample_campaign_data):
        """Should generate subject without first name."""
        lead_data = {"company_name": "Test Corp"}
        subject = EmailGeneratorService.generate_subject(lead_data, sample_campaign_data)
        
        assert sample_campaign_data["value_prop"] in subject

    def test_generate_subject_empty_data(self):
        """Should generate subject with defaults."""
        subject = EmailGeneratorService.generate_subject({}, {})
        
        assert "Automatiser" in subject or len(subject) > 0


class TestGenerateBody:
    """Test email body generation."""

    def test_generate_body_with_all_data(self, sample_lead_data, sample_campaign_data):
        """Should generate body with all lead data."""
        body = EmailGeneratorService.generate_body(sample_lead_data, sample_campaign_data)
        
        assert "John" in body or "Bonjour" in body
        assert "Test Corp" in body
        assert sample_campaign_data["value_prop"] in body or "prospection" in body

    def test_generate_body_with_calendly_url(self, sample_lead_data, sample_campaign_data):
        """Should include Calendly URL in body."""
        calendly_url = "https://calendly.com/vectra/demo"
        body = EmailGeneratorService.generate_body(sample_lead_data, sample_campaign_data, calendly_url)
        
        assert calendly_url in body
        assert "calendly" in body.lower() or "créneau" in body.lower() or "Réserver" in body

    def test_generate_body_without_calendly_url(self, sample_lead_data, sample_campaign_data):
        """Should generate body without Calendly URL."""
        body = EmailGeneratorService.generate_body(sample_lead_data, sample_campaign_data)
        
        assert "créneau" in body.lower() or "démonstration" in body.lower() or "15" in body


class TestGenerateEmail:
    """Test complete email generation."""

    def test_generate_email_complete(self, sample_lead_data, sample_campaign_data):
        """Should generate complete email with subject and body."""
        calendly_url = "https://calendly.com/vectra/demo"
        email = EmailGeneratorService.generate_email(sample_lead_data, sample_campaign_data, calendly_url)
        
        assert "subject" in email
        assert "body" in email
        assert len(email["subject"]) > 0
        assert len(email["body"]) > 0

    def test_generate_email_subject_contains_lead_info(self, sample_lead_data, sample_campaign_data):
        """Subject should contain lead information."""
        email = EmailGeneratorService.generate_email(sample_lead_data, sample_campaign_data)
        
        assert sample_lead_data["first_name"] in email["subject"] or sample_lead_data["company_name"] in email["subject"]

    def test_generate_email_body_contains_lead_info(self, sample_lead_data, sample_campaign_data):
        """Body should contain lead information."""
        email = EmailGeneratorService.generate_email(sample_lead_data, sample_campaign_data)
        
        assert sample_lead_data["first_name"] in email["body"] or "Bonjour" in email["body"]
        assert sample_lead_data["company_name"] in email["body"]
