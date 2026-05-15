"""Meetings API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db, get_organization_user
from app.schemas.meeting import MeetingResponse, MeetingListResponse, MeetingUpdate
from app.db.models.user import User
from app.services.meeting import MeetingService

router = APIRouter()


@router.get("", response_model=MeetingListResponse)
def list_meetings(
    campaign_id: Optional[UUID] = Query(None, description="Filter by campaign ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    List meetings for current user's organization.

    Supports filtering by campaign and status.
    """
    service = MeetingService(db)
    meetings, total = service.list_meetings(
        user=current_user,
        campaign_id=campaign_id,
        status_filter=status,
        skip=skip,
        limit=limit,
    )

    data = [
        MeetingResponse(
            id=m.id,
            lead_id=m.lead_id,
            campaign_id=m.campaign_id,
            organization_id=m.organization_id,
            scheduled_at=m.scheduled_at,
            duration_minutes=m.duration_minutes,
            meeting_url=m.meeting_url,
            calendly_event_id=m.calendly_event_id,
            status=m.status.value,
            completed_at=m.completed_at,
            no_show=m.no_show,
            notes=m.notes,
            outcome=m.outcome.value if m.outcome else None,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
        for m in meetings
    ]

    return MeetingListResponse(
        data=data,
        pagination={
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total,
        },
    )


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Get meeting details by ID.
    """
    service = MeetingService(db)
    m = service.get_meeting(user=current_user, meeting_id=meeting_id)

    return MeetingResponse(
        id=m.id,
        lead_id=m.lead_id,
        campaign_id=m.campaign_id,
        organization_id=m.organization_id,
        scheduled_at=m.scheduled_at,
        duration_minutes=m.duration_minutes,
        meeting_url=m.meeting_url,
        calendly_event_id=m.calendly_event_id,
        status=m.status.value,
        completed_at=m.completed_at,
        no_show=m.no_show,
        notes=m.notes,
        outcome=m.outcome.value if m.outcome else None,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


@router.patch("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(
    meeting_id: UUID,
    body: MeetingUpdate,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Update a meeting's notes, outcome, or status.
    """
    service = MeetingService(db)
    m = service.update_meeting(
        user=current_user,
        meeting_id=meeting_id,
        notes=body.notes,
        outcome=body.outcome,
        status=body.status,
    )

    return MeetingResponse(
        id=m.id,
        lead_id=m.lead_id,
        campaign_id=m.campaign_id,
        organization_id=m.organization_id,
        scheduled_at=m.scheduled_at,
        duration_minutes=m.duration_minutes,
        meeting_url=m.meeting_url,
        calendly_event_id=m.calendly_event_id,
        status=m.status.value,
        completed_at=m.completed_at,
        no_show=m.no_show,
        notes=m.notes,
        outcome=m.outcome.value if m.outcome else None,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )
