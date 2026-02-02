"""Platform admin schemas for request/response validation."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.db.models.organization import PlanType


class PlatformOverviewResponse(BaseModel):
    """Platform overview statistics."""
    total_organizations: int
    total_users: int
    active_campaigns: int
    total_leads: int
    conversion_rate: float
    emails_sent: int
    meetings_scheduled: int


class PlatformOrganizationResponse(BaseModel):
    """Organization details for platform admin."""
    id: UUID
    name: str
    slug: str
    plan: str
    settings: dict
    user_count: int
    campaign_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlatformOrganizationCreate(BaseModel):
    """Request to create organization (platform admin)."""
    name: str = Field(..., max_length=255)
    plan: str = Field(default="trial", max_length=50)
    settings: Optional[dict] = None


class PlatformOrganizationUpdate(BaseModel):
    """Request to update organization (platform admin)."""
    name: Optional[str] = Field(None, max_length=255)
    plan: Optional[str] = None
    settings: Optional[dict] = None


class PlatformUserResponse(BaseModel):
    """User details for platform admin."""
    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    organization_id: Optional[UUID] = None
    organization_name: Optional[str] = None
    is_active: bool
    email_verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PlatformSystemMetricsResponse(BaseModel):
    """System metrics for platform admin."""
    api_requests_per_minute: float
    average_response_time_ms: float
    agent_latency_avg_ms: float
    error_rate: float
    active_users: int
