"""Email schemas for request/response validation."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List


class LeadSummary(BaseModel):
    """Lead summary for email context."""
    email: str
    name: Optional[str] = None
    company: Optional[str] = None


class TrackingInfo(BaseModel):
    """Email tracking information."""
    opened_count: int = 0
    first_opened_at: Optional[datetime] = None
    last_opened_at: Optional[datetime] = None
    clicked_count: int = 0
    first_clicked_at: Optional[datetime] = None


class EmailResponse(BaseModel):
    """Email response with details."""
    id: UUID
    lead_id: UUID
    campaign_id: UUID
    lead: Optional[LeadSummary] = None
    subject: str
    body_preview: Optional[str] = None
    status: str
    generated_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class EmailDetailResponse(BaseModel):
    """Detailed email response."""
    id: UUID
    lead_id: UUID
    campaign_id: UUID
    subject: str
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    from_email: Optional[str] = None
    from_name: Optional[str] = None
    to_email: Optional[str] = None
    status: str
    generated_by: Optional[str] = None
    generation_model: Optional[str] = None
    approved_by: Optional[Dict[str, Any]] = None
    approved_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    tracking: Optional[TrackingInfo] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ApproveEmailRequest(BaseModel):
    """Request to approve an email."""
    modifications: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Optional subject or body_html modifications"
    )


class RejectEmailRequest(BaseModel):
    """Request to reject an email."""
    reason: str = Field(..., min_length=1, max_length=500)


class EmailApproveResponse(BaseModel):
    """Response after approving an email."""
    id: UUID
    status: str
    approved_at: Optional[datetime] = None
    scheduled_send_at: Optional[datetime] = None


class EmailListResponse(BaseModel):
    """Paginated list of emails."""
    data: List[EmailResponse]
    pagination: Dict[str, Any]
