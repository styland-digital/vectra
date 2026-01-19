"""Email API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db, get_organization_user
from app.schemas.email import (
    EmailResponse,
    EmailDetailResponse,
    EmailListResponse,
    ApproveEmailRequest,
    RejectEmailRequest,
    EmailApproveResponse,
    LeadSummary,
    TrackingInfo,
)
from app.db.models.user import User
from app.db.models.email import Email
from app.services.email import EmailService

router = APIRouter()


@router.get("", response_model=EmailListResponse)
def list_emails(
    campaign_id: Optional[UUID] = Query(None, description="Filter by campaign ID"),
    lead_id: Optional[UUID] = Query(None, description="Filter by lead ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    List emails for current user's organization.
    
    Supports filtering by campaign, lead, and status.
    """
    service = EmailService(db)
    emails, total = service.list_emails(
        user=current_user,
        campaign_id=campaign_id,
        lead_id=lead_id,
        status_filter=status,
        skip=skip,
        limit=limit,
    )
    
    email_responses = []
    for email in emails:
        lead_summary = None
        if email.lead:
            lead_summary = LeadSummary(
                email=email.lead.email,
                name=email.lead.full_name if hasattr(email.lead, 'full_name') else email.lead.email,
                company=email.lead.company_name,
            )
        
        body_preview = email.body[:200] + "..." if email.body and len(email.body) > 200 else email.body
        
        email_responses.append(EmailResponse(
            id=email.id,
            lead_id=email.lead_id,
            campaign_id=email.campaign_id,
            lead=lead_summary,
            subject=email.subject,
            body_preview=body_preview,
            status=email.status.value,
            generated_by="scheduler",  # TODO: Store actual generator
            created_at=email.created_at,
        ))
    
    return EmailListResponse(
        data=email_responses,
        pagination={
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total,
        }
    )


@router.get("/{email_id}", response_model=EmailDetailResponse)
def get_email(
    email_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Get detailed email information.
    """
    service = EmailService(db)
    email = service.get_email(user=current_user, email_id=email_id)
    
    # Extract body as HTML and text
    body_html = email.body if email.body else None
    body_text = email.body if email.body else None  # TODO: Convert HTML to text if needed
    
    # Build approved_by info
    approved_by_info = None
    if email.approved_by_user:
        approved_by_info = {
            "id": str(email.approved_by_user.id),
            "name": email.approved_by_user.full_name if hasattr(email.approved_by_user, 'full_name') else email.approved_by_user.email,
        }
    
    # Build tracking info
    tracking_info = TrackingInfo(
        opened_count=email.open_count,
        first_opened_at=email.opened_at,
        last_opened_at=email.opened_at,  # TODO: Track last opened separately
        clicked_count=email.click_count,
        first_clicked_at=email.clicked_at,
    )
    
    return EmailDetailResponse(
        id=email.id,
        lead_id=email.lead_id,
        campaign_id=email.campaign_id,
        subject=email.subject,
        body_html=body_html,
        body_text=body_text,
        from_email=None,  # TODO: Store from_email
        from_name=None,  # TODO: Store from_name
        to_email=email.lead.email if email.lead else None,
        status=email.status.value,
        generated_by="scheduler",
        generation_model=None,  # TODO: Store generation model
        approved_by=approved_by_info,
        approved_at=email.approved_at,
        sent_at=email.sent_at,
        tracking=tracking_info,
        created_at=email.created_at,
    )


@router.post("/{email_id}/approve", response_model=EmailApproveResponse)
def approve_email(
    email_id: UUID,
    request: ApproveEmailRequest,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Approve an email for sending.
    
    Optionally modify subject or body before approval.
    """
    service = EmailService(db)
    email = service.approve_email(
        user=current_user,
        email_id=email_id,
        subject=request.modifications.get("subject") if request.modifications else None,
        body_html=request.modifications.get("body_html") if request.modifications else None,
    )
    
    # TODO: Schedule email sending (add to queue)
    scheduled_send_at = None
    
    return EmailApproveResponse(
        id=email.id,
        status=email.status.value,
        approved_at=email.approved_at,
        scheduled_send_at=scheduled_send_at,
    )


@router.post("/{email_id}/reject", response_model=EmailDetailResponse)
def reject_email(
    email_id: UUID,
    request: RejectEmailRequest,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Reject an email.
    
    Provide a reason for rejection.
    """
    service = EmailService(db)
    email = service.reject_email(
        user=current_user,
        email_id=email_id,
        reason=request.reason,
    )
    
    # Build response (similar to get_email)
    body_html = email.body if email.body else None
    body_text = email.body if email.body else None
    
    approved_by_info = None
    if email.approved_by_user:
        approved_by_info = {
            "id": str(email.approved_by_user.id),
            "name": email.approved_by_user.full_name if hasattr(email.approved_by_user, 'full_name') else email.approved_by_user.email,
        }
    
    tracking_info = TrackingInfo(
        opened_count=email.open_count,
        first_opened_at=email.opened_at,
        last_opened_at=email.opened_at,
        clicked_count=email.click_count,
        first_clicked_at=email.clicked_at,
    )
    
    return EmailDetailResponse(
        id=email.id,
        lead_id=email.lead_id,
        campaign_id=email.campaign_id,
        subject=email.subject,
        body_html=body_html,
        body_text=body_text,
        from_email=None,
        from_name=None,
        to_email=email.lead.email if email.lead else None,
        status=email.status.value,
        generated_by="scheduler",
        generation_model=None,
        approved_by=approved_by_info,
        approved_at=email.approved_at,
        sent_at=email.sent_at,
        tracking=tracking_info,
        created_at=email.created_at,
    )
