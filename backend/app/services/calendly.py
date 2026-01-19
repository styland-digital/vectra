"""Calendly integration service."""

from typing import Dict, Any, Optional
import urllib.parse

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CalendlyService:
    """Service for Calendly integration."""

    def __init__(self, api_key: Optional[str] = None, event_type: Optional[str] = None):
        """
        Initialize Calendly service.
        
        Args:
            api_key: Calendly API key (defaults to settings)
            event_type: Calendly event type UUID (optional)
        """
        self.api_key = api_key or settings.CALENDLY_API_KEY
        self.event_type = event_type
        self.base_url = "https://calendly.com"

    def generate_scheduling_link(
        self,
        lead_email: str,
        lead_name: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> str:
        """
        Generate Calendly scheduling link with pre-filled information.
        
        Args:
            lead_email: Lead email address
            lead_name: Lead name (optional)
            event_type: Event type UUID (optional, uses default if not provided)
            
        Returns:
            Calendly scheduling URL
        """
        if not self.api_key and not event_type:
            logger.warning("Calendly API key and event_type not configured")
            # Return generic Calendly link
            calendly_username = settings.CALENDLY_API_KEY.split("/")[-1] if settings.CALENDLY_API_KEY else "vectra"
            return f"{self.base_url}/{calendly_username}"
        
        event_uuid = event_type or self.event_type
        
        # Build Calendly URL with pre-filled info
        # Format: https://calendly.com/{username}/{event_type}?name={name}&email={email}
        params = {
            "email": lead_email,
        }
        
        if lead_name:
            params["name"] = lead_name
        
        query_string = urllib.parse.urlencode(params)
        
        if event_uuid:
            # If we have event type, construct full URL
            calendly_username = settings.CALENDLY_API_KEY.split("/")[-1] if "/" in str(settings.CALENDLY_API_KEY) else "vectra"
            url = f"{self.base_url}/{calendly_username}/{event_uuid}?{query_string}"
        else:
            # Generic link
            calendly_username = "vectra"
            url = f"{self.base_url}/{calendly_username}?{query_string}"
        
        logger.info(f"Generated Calendly link for {lead_email}")
        
        return url
