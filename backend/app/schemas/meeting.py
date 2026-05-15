"""Meeting schemas for request/response validation."""

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List


class MeetingResponse(BaseModel):
    """Full meeting response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_id: UUID
    campaign_id: UUID
    organization_id: UUID
    scheduled_at: datetime
    duration_minutes: int
    meeting_url: Optional[str] = None
    calendly_event_id: Optional[str] = None
    status: str
    completed_at: Optional[datetime] = None
    no_show: bool
    notes: Optional[str] = None
    outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class MeetingListResponse(BaseModel):
    """Paginated list of meetings."""

    data: List[MeetingResponse]
    pagination: Dict[str, Any]


class MeetingUpdate(BaseModel):
    """Updatable fields for a meeting."""

    notes: Optional[str] = None
    outcome: Optional[str] = None
    status: Optional[str] = None
