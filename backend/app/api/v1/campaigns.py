"""Campaign API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.api.deps import get_db, get_organization_user
from app.schemas.campaign import (
    CampaignResponse,
    CampaignCreate,
    CampaignUpdate,
    CampaignStatsResponse,
)
from app.schemas.auth import MessageResponse
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.user import User
from app.db.session import SessionLocal
from app.services.campaign import CampaignService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


async def _run_campaign_background(campaign_id: UUID) -> None:
    """Background task: creates its own DB session and runs the full campaign pipeline."""
    # Lazy import so the heavy agent/crewai chain doesn't load at router startup.
    from app.orchestrator.campaign_runner import CampaignRunner  # noqa: PLC0415

    db = SessionLocal()
    try:
        runner = CampaignRunner(db=db)
        await runner.run_campaign(campaign_id)
    except Exception as exc:
        logger.error(
            f"Unhandled error in campaign background task {campaign_id}: {exc}",
            exc_info=True,
        )
        try:
            c = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if c and c.status == CampaignStatus.ACTIVE:
                c.status = CampaignStatus.PAUSED
                db.commit()
        except Exception:
            pass
    finally:
        db.close()



@router.get("", response_model=List[CampaignResponse])
def list_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None, max_length=100),
    created_by: Optional[UUID] = Query(None),
    created_after: Optional[datetime] = Query(None),
    started_after: Optional[datetime] = Query(None),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """List campaigns for current user's organization with optional filters."""
    service = CampaignService(db)
    return service.list_campaigns(
        user=current_user,
        skip=skip,
        limit=limit,
        status_filter=status,
        search=search,
        created_by_filter=created_by,
        created_after=created_after,
        started_after=started_after,
    )


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Get campaign details by ID.
    """
    service = CampaignService(db)
    campaign = service.get_campaign(user=current_user, campaign_id=campaign_id)
    
    return campaign


@router.post("", response_model=CampaignResponse, status_code=201)
def create_campaign(
    request: CampaignCreate,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Create a new campaign.
    """
    service = CampaignService(db)
    campaign = service.create_campaign(
        user=current_user,
        name=request.name,
        description=request.description,
        target_criteria=request.target_criteria,
        email_template=request.email_template,
        bant_threshold=request.bant_threshold,
        daily_limit=request.daily_limit,
    )
    
    return campaign


@router.patch("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: UUID,
    request: CampaignUpdate,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Update a campaign.
    
    Can only update DRAFT campaigns.
    """
    service = CampaignService(db)
    campaign = service.update_campaign(
        user=current_user,
        campaign_id=campaign_id,
        name=request.name,
        description=request.description,
        target_criteria=request.target_criteria,
        email_template=request.email_template,
        bant_threshold=request.bant_threshold,
        daily_limit=request.daily_limit,
    )
    
    return campaign


@router.post("/{campaign_id}/launch", response_model=CampaignResponse)
def launch_campaign(
    campaign_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Launch a campaign (change status to ACTIVE and start execution).
    """
    service = CampaignService(db)
    campaign = service.launch_campaign(user=current_user, campaign_id=campaign_id)
    background_tasks.add_task(_run_campaign_background, campaign.id)
    return campaign


@router.post("/{campaign_id}/pause", response_model=CampaignResponse)
def pause_campaign(
    campaign_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Pause an active campaign.
    """
    service = CampaignService(db)
    campaign = service.pause_campaign(user=current_user, campaign_id=campaign_id)
    
    return campaign


@router.post("/{campaign_id}/resume", response_model=CampaignResponse)
def resume_campaign(
    campaign_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Resume a paused campaign.
    """
    service = CampaignService(db)
    campaign = service.resume_campaign(user=current_user, campaign_id=campaign_id)
    background_tasks.add_task(_run_campaign_background, campaign.id)
    return campaign


@router.delete("/{campaign_id}", status_code=204)
def delete_campaign(
    campaign_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Delete a campaign (soft delete - archive).
    """
    service = CampaignService(db)
    service.delete_campaign(user=current_user, campaign_id=campaign_id)
    
    return None


@router.get("/{campaign_id}/stats", response_model=CampaignStatsResponse)
def get_campaign_stats(
    campaign_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Get campaign statistics.
    """
    service = CampaignService(db)
    stats = service.get_campaign_stats(user=current_user, campaign_id=campaign_id)
    
    return stats
