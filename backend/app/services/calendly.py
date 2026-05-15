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
            event_type: Event type slug/UUID (optional)

        Returns:
            Calendly scheduling URL with pre-filled query parameters
        """
        params: Dict[str, str] = {}
        if lead_email:
            params["email"] = lead_email
        if lead_name:
            params["name"] = lead_name
        query_string = urllib.parse.urlencode(params)

        # Resolve the base Calendly URL from settings.
        # CALENDLY_API_KEY may hold either:
        #   - A full URL  (e.g. "https://calendly.com/my-username")
        #   - A raw API key / username  (e.g. "my-username" or "tok_...")
        calendly_cfg = (
            getattr(settings, "CALENDLY_URL", None)
            or getattr(settings, "CALENDLY_API_KEY", None)
            or ""
        )

        if calendly_cfg.startswith("https://calendly.com/"):
            # Full URL supplied — use it as the base directly.
            base = calendly_cfg.rstrip("/")
        else:
            # Treat the value as a username (or fall back to "vectra").
            username = calendly_cfg.strip("/") if calendly_cfg else "vectra"
            # If the value looks like an API token (long hex string), ignore it.
            if len(username) > 60 or " " in username:
                username = "vectra"
            base = f"{self.base_url}/{username}"

        # Append event type slug when provided.
        event_slug = event_type or self.event_type
        if event_slug:
            base = f"{base}/{event_slug.strip('/')}"

        url = f"{base}?{query_string}" if query_string else base
        logger.info(f"Generated Calendly link for {lead_email}")
        return url
