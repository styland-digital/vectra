"""Tests for Calendly service."""

import pytest
from unittest.mock import patch

from app.services.calendly import CalendlyService


class TestGenerateSchedulingLink:
    """Test Calendly scheduling link generation."""

    def test_generate_link_with_email(self):
        """Should generate link with email parameter."""
        service = CalendlyService()
        link = service.generate_scheduling_link("test@example.com")
        
        assert "calendly.com" in link
        assert "test@example.com" in link or "email=" in link

    def test_generate_link_with_name(self):
        """Should generate link with name parameter."""
        service = CalendlyService()
        link = service.generate_scheduling_link("test@example.com", lead_name="John Doe")
        
        assert "calendly.com" in link
        assert "test@example.com" in link or "email=" in link
        assert "John" in link or "Doe" in link or "name=" in link

    def test_generate_link_with_event_type(self):
        """Should generate link with event type."""
        service = CalendlyService(event_type="test-event-uuid")
        link = service.generate_scheduling_link("test@example.com")
        
        assert "calendly.com" in link

    def test_generate_link_custom_api_key(self):
        """Should generate link with custom API key."""
        service = CalendlyService(api_key="custom-key")
        link = service.generate_scheduling_link("test@example.com")
        
        assert "calendly.com" in link

    @patch('app.services.calendly.settings')
    def test_generate_link_no_config(self, mock_settings):
        """Should generate generic link when no config."""
        mock_settings.CALENDLY_API_KEY = None
        service = CalendlyService()
        link = service.generate_scheduling_link("test@example.com")
        
        assert "calendly.com" in link


class TestCalendlyServiceInit:
    """Test Calendly service initialization."""

    def test_init_with_defaults(self):
        """Should initialize with default settings."""
        service = CalendlyService()
        
        assert service.base_url == "https://calendly.com"
        assert service.event_type is None

    def test_init_with_custom_api_key(self):
        """Should initialize with custom API key."""
        service = CalendlyService(api_key="custom-key")
        
        assert service.api_key == "custom-key"

    def test_init_with_custom_event_type(self):
        """Should initialize with custom event type."""
        service = CalendlyService(event_type="test-event")
        
        assert service.event_type == "test-event"
