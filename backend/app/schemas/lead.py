"""Lead schemas for request/response validation."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List


class CompanyInfo(BaseModel):
    """Company information."""
    name: Optional[str] = None
    domain: Optional[str] = None
    size: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None


class JobInfo(BaseModel):
    """Job information."""
    title: Optional[str] = None
    department: Optional[str] = None
    seniority: Optional[str] = None


class BANTInfo(BaseModel):
    """BANT qualification information."""
    score: Optional[int] = None
    budget: Optional[int] = None
    authority: Optional[int] = None
    need: Optional[int] = None
    timeline: Optional[int] = None
    notes: Optional[str] = None


class LeadResponse(BaseModel):
    """Lead response with details."""
    id: UUID
    campaign_id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    company: Optional[CompanyInfo] = None
    job: Optional[JobInfo] = None
    bant: Optional[BANTInfo] = None
    intent: Optional[str] = None
    intent_confidence: Optional[float] = None
    status: str
    email_status: Optional[str] = None
    email_sent_at: Optional[datetime] = None
    email_opened_at: Optional[datetime] = None
    enriched_at: Optional[datetime] = None
    qualified_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LeadDetailResponse(LeadResponse):
    """Detailed lead response with interactions, emails, meetings."""
    interactions: List[Dict[str, Any]] = Field(default_factory=list)
    emails: List[Dict[str, Any]] = Field(default_factory=list)
    meetings: List[Dict[str, Any]] = Field(default_factory=list)


class LeadUpdate(BaseModel):
    """Request to update a lead."""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    company_name: Optional[str] = Field(None, max_length=255)
    job_title: Optional[str] = Field(None, max_length=200)
    status: Optional[str] = None
    notes: Optional[str] = None


class InteractionResponse(BaseModel):
    """Interaction response."""
    id: UUID
    type: str
    agent_type: Optional[str] = None
    data: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Paginated list of leads."""
    data: List[LeadResponse]
    pagination: Dict[str, Any]


class InteractionListResponse(BaseModel):
    """Paginated list of interactions."""
    data: List[InteractionResponse]
    pagination: Dict[str, Any]
