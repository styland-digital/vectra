"""Campaign schemas for request/response validation."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any


class CampaignResponse(BaseModel):
    """Campaign response with details."""
    id: UUID
    organization_id: UUID
    created_by: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    status: str
    target_criteria: Dict[str, Any]
    email_template: Optional[Dict[str, Any]] = None
    bant_threshold: int
    daily_limit: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CampaignCreate(BaseModel):
    """Request to create a campaign."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    target_criteria: Optional[Dict[str, Any]] = Field(default_factory=dict)
    email_template: Optional[Dict[str, Any]] = None
    bant_threshold: int = Field(default=60, ge=0, le=100)
    daily_limit: int = Field(default=50, ge=1)


class CampaignUpdate(BaseModel):
    """Request to update a campaign."""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    target_criteria: Optional[Dict[str, Any]] = None
    email_template: Optional[Dict[str, Any]] = None
    bant_threshold: Optional[int] = Field(None, ge=0, le=100)
    daily_limit: Optional[int] = Field(None, ge=1)


class CampaignStatsResponse(BaseModel):
    """Campaign statistics response."""
    campaign_id: str
    status: str
    leads: Dict[str, int]
    emails: Dict[str, int]
    bant: Dict[str, float]
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
