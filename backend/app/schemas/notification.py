"""Notification schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class NotificationType(str):
    """Notification types."""
    # Platform admin notifications
    VECTRA_TO_USERS = "vectra_to_users"
    VECTRA_TO_ORG_OWNER = "vectra_to_org_owner"
    SYSTEM_ALERTS = "system_alerts"
    # Organization notifications
    ORG_TO_PROSPECTS = "org_to_prospects"
    ORG_OWNER_TO_MEMBERS = "org_owner_to_members"


class SendNotificationRequest(BaseModel):
    """Request to send a notification."""
    type: str = Field(..., description="Notification type")
    recipients: List[str] = Field(..., description="Recipients (emails, organization_id, or 'all')")
    subject: str = Field(..., max_length=255)
    body: str = Field(..., description="Plain text body")
    body_html: Optional[str] = Field(None, description="HTML body (optional)")
    action_url: Optional[str] = Field(None, description="Action button URL (optional)")
    action_text: Optional[str] = Field(None, max_length=50, description="Action button text (optional)")


class NotificationResponse(BaseModel):
    """Notification response."""
    success: bool
    message: str
    sent_count: int
    failed_count: int
