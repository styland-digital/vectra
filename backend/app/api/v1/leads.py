"""Lead API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.api.deps import get_db, get_organization_user
from app.schemas.lead import (
    LeadResponse,
    LeadDetailResponse,
    LeadUpdate,
    InteractionResponse,
    LeadListResponse,
    InteractionListResponse,
)
from app.db.models.user import User
from app.db.models.lead import Lead, LeadStatus
from app.services.lead import LeadService

router = APIRouter()


@router.get("", response_model=LeadListResponse)
def list_leads(
    campaign_id: Optional[UUID] = Query(None, description="Filter by campaign ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    intent: Optional[str] = Query(None, description="Filter by intent"),
    bant_score_min: Optional[int] = Query(None, ge=0, le=100, description="Minimum BANT score"),
    bant_score_max: Optional[int] = Query(None, ge=0, le=100, description="Maximum BANT score"),
    search: Optional[str] = Query(None, description="Search by name, email, company"),
    created_after: Optional[datetime] = Query(None, description="Filter by creation date (after)"),
    created_before: Optional[datetime] = Query(None, description="Filter by creation date (before)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    List leads for current user's organization.
    
    Supports filtering by campaign, status, intent, BANT score, and search.
    """
    service = LeadService(db)
    leads, total = service.list_leads(
        user=current_user,
        campaign_id=campaign_id,
        status_filter=status,
        intent_filter=intent,
        bant_score_min=bant_score_min,
        bant_score_max=bant_score_max,
        search=search,
        created_after=created_after,
        created_before=created_before,
        skip=skip,
        limit=limit,
    )
    
    # Convert to response format
    lead_responses = []
    for lead in leads:
        # Extract company info from enrichment_data
        company_info = None
        if lead.enrichment_data:
            company_info = {
                "name": lead.company_name or lead.enrichment_data.get("company_name"),
                "domain": lead.enrichment_data.get("domain"),
                "size": lead.company_size or lead.enrichment_data.get("company_size"),
                "industry": lead.enrichment_data.get("industry"),
                "location": lead.enrichment_data.get("location"),
            }
            # Remove None values
            company_info = {k: v for k, v in company_info.items() if v is not None} or None
        
        # Extract BANT info
        bant_info = None
        if lead.bant_score is not None:
            bant_info = {
                "score": lead.bant_score,
                "budget": lead.bant_breakdown.get("budget") if lead.bant_breakdown else None,
                "authority": lead.bant_breakdown.get("authority") if lead.bant_breakdown else None,
                "need": lead.bant_breakdown.get("need") if lead.bant_breakdown else None,
                "timeline": lead.bant_breakdown.get("timeline") if lead.bant_breakdown else None,
                "notes": lead.enrichment_data.get("notes") if lead.enrichment_data else None,
            }
            bant_info = {k: v for k, v in bant_info.items() if v is not None} or None
        
        # Get latest email status
        email_status = None
        email_sent_at = None
        email_opened_at = None
        if lead.emails:
            latest_email = max(lead.emails, key=lambda e: e.created_at)
            email_status = latest_email.status.value
            email_sent_at = latest_email.sent_at
            email_opened_at = latest_email.opened_at
        
        lead_responses.append(LeadResponse(
            id=lead.id,
            campaign_id=lead.campaign_id,
            email=lead.email,
            first_name=lead.first_name,
            last_name=lead.last_name,
            phone=lead.phone,
            linkedin_url=lead.linkedin_url,
            company=company_info,
            job={"title": lead.job_title} if lead.job_title else None,
            bant=bant_info,
            intent=lead.intent.value if lead.intent else None,
            intent_confidence=None,  # TODO: Store intent confidence
            status=lead.status.value,
            email_status=email_status,
            email_sent_at=email_sent_at,
            email_opened_at=email_opened_at,
            enriched_at=None,  # TODO: Track enrichment timestamp
            qualified_at=None,  # TODO: Track qualification timestamp
            created_at=lead.created_at,
        ))
    
    return LeadListResponse(
        data=lead_responses,
        pagination={
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total,
        }
    )


@router.get("/{lead_id}", response_model=LeadDetailResponse)
def get_lead(
    lead_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Get detailed lead information with interactions, emails, and meetings.
    """
    service = LeadService(db)
    lead = service.get_lead(user=current_user, lead_id=lead_id)
    
    # Get interactions
    interactions, _ = service.get_lead_interactions(
        user=current_user,
        lead_id=lead_id,
        skip=0,
        limit=100,
    )
    
    # Get emails summary
    emails_summary = []
    for email in lead.emails:
        emails_summary.append({
            "id": str(email.id),
            "subject": email.subject,
            "status": email.status.value,
            "sent_at": email.sent_at.isoformat() if email.sent_at else None,
            "opened_count": email.open_count,
        })
    
    # Get meetings summary
    meetings_summary = []
    for meeting in lead.meetings:
        meetings_summary.append({
            "id": str(meeting.id),
            "scheduled_at": meeting.scheduled_at.isoformat() if meeting.scheduled_at else None,
            "status": meeting.status.value,
        })
    
    # Build lead response (similar to list)
    company_info = None
    if lead.enrichment_data:
        company_info = {
            "name": lead.company_name or lead.enrichment_data.get("company_name"),
            "domain": lead.enrichment_data.get("domain"),
            "size": lead.company_size or lead.enrichment_data.get("company_size"),
            "industry": lead.enrichment_data.get("industry"),
            "location": lead.enrichment_data.get("location"),
        }
        company_info = {k: v for k, v in company_info.items() if v is not None} or None
    
    bant_info = None
    if lead.bant_score is not None:
        bant_info = {
            "score": lead.bant_score,
            "budget": lead.bant_breakdown.get("budget") if lead.bant_breakdown else None,
            "authority": lead.bant_breakdown.get("authority") if lead.bant_breakdown else None,
            "need": lead.bant_breakdown.get("need") if lead.bant_breakdown else None,
            "timeline": lead.bant_breakdown.get("timeline") if lead.bant_breakdown else None,
            "notes": lead.enrichment_data.get("notes") if lead.enrichment_data else None,
        }
        bant_info = {k: v for k, v in bant_info.items() if v is not None} or None
    
    email_status = None
    email_sent_at = None
    email_opened_at = None
    if lead.emails:
        latest_email = max(lead.emails, key=lambda e: e.created_at)
        email_status = latest_email.status.value
        email_sent_at = latest_email.sent_at
        email_opened_at = latest_email.opened_at
    
    return LeadDetailResponse(
        id=lead.id,
        campaign_id=lead.campaign_id,
        email=lead.email,
        first_name=lead.first_name,
        last_name=lead.last_name,
        phone=lead.phone,
        linkedin_url=lead.linkedin_url,
        company=company_info,
        job={"title": lead.job_title} if lead.job_title else None,
        bant=bant_info,
        intent=lead.intent.value if lead.intent else None,
        intent_confidence=None,
        status=lead.status.value,
        email_status=email_status,
        email_sent_at=email_sent_at,
        email_opened_at=email_opened_at,
        enriched_at=None,
        qualified_at=None,
        created_at=lead.created_at,
        interactions=interactions,
        emails=emails_summary,
        meetings=meetings_summary,
    )


@router.get("/{lead_id}/interactions", response_model=InteractionListResponse)
def get_lead_interactions(
    lead_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Get interaction history for a lead.
    """
    service = LeadService(db)
    interactions, total = service.get_lead_interactions(
        user=current_user,
        lead_id=lead_id,
        skip=skip,
        limit=limit,
    )
    
    interaction_responses = [
        InteractionResponse(
            id=UUID(i["id"]),
            type=i["type"],
            agent_type=i.get("agent_type"),
            data=i["data"],
            created_at=i["created_at"],
        )
        for i in interactions
    ]
    
    return InteractionListResponse(
        data=interaction_responses,
        pagination={
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total,
        }
    )


@router.patch("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: UUID,
    request: LeadUpdate,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Update a lead manually.
    """
    service = LeadService(db)
    lead = service.update_lead(
        user=current_user,
        lead_id=lead_id,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        company_name=request.company_name,
        job_title=request.job_title,
        status=request.status,
        notes=request.notes,
    )
    
    # Build response (similar to list)
    company_info = None
    if lead.enrichment_data:
        company_info = {
            "name": lead.company_name or lead.enrichment_data.get("company_name"),
            "domain": lead.enrichment_data.get("domain"),
            "size": lead.company_size or lead.enrichment_data.get("company_size"),
            "industry": lead.enrichment_data.get("industry"),
            "location": lead.enrichment_data.get("location"),
        }
        company_info = {k: v for k, v in company_info.items() if v is not None} or None
    
    bant_info = None
    if lead.bant_score is not None:
        bant_info = {
            "score": lead.bant_score,
            "budget": lead.bant_breakdown.get("budget") if lead.bant_breakdown else None,
            "authority": lead.bant_breakdown.get("authority") if lead.bant_breakdown else None,
            "need": lead.bant_breakdown.get("need") if lead.bant_breakdown else None,
            "timeline": lead.bant_breakdown.get("timeline") if lead.bant_breakdown else None,
            "notes": lead.enrichment_data.get("notes") if lead.enrichment_data else None,
        }
        bant_info = {k: v for k, v in bant_info.items() if v is not None} or None
    
    email_status = None
    email_sent_at = None
    email_opened_at = None
    if lead.emails:
        latest_email = max(lead.emails, key=lambda e: e.created_at)
        email_status = latest_email.status.value
        email_sent_at = latest_email.sent_at
        email_opened_at = latest_email.opened_at
    
    return LeadResponse(
        id=lead.id,
        campaign_id=lead.campaign_id,
        email=lead.email,
        first_name=lead.first_name,
        last_name=lead.last_name,
        phone=lead.phone,
        linkedin_url=lead.linkedin_url,
        company=company_info,
        job={"title": lead.job_title} if lead.job_title else None,
        bant=bant_info,
        intent=lead.intent.value if lead.intent else None,
        intent_confidence=None,
        status=lead.status.value,
        email_status=email_status,
        email_sent_at=email_sent_at,
        email_opened_at=email_opened_at,
        enriched_at=None,
        qualified_at=None,
        created_at=lead.created_at,
    )
