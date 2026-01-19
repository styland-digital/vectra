"""Platform admin API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db, get_platform_admin
from app.schemas.platform import (
    PlatformOverviewResponse,
    PlatformOrganizationResponse,
    PlatformOrganizationCreate,
    PlatformOrganizationUpdate,
    PlatformUserResponse,
    PlatformSystemMetricsResponse,
)
from app.schemas.notification import SendNotificationRequest, NotificationResponse
from app.services.platform import PlatformService
from app.services.notification import NotificationService
from app.db.models.user import User

router = APIRouter()


@router.get("/overview", response_model=PlatformOverviewResponse)
def get_overview(
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    Get platform overview statistics.
    
    Returns total organizations, users, campaigns, leads, and metrics.
    """
    service = PlatformService(db)
    overview = service.get_overview()
    return PlatformOverviewResponse(**overview)


@router.get("/organizations", response_model=List[PlatformOrganizationResponse])
def list_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    plan: Optional[str] = Query(None),
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    List all organizations with filters.
    
    Supports pagination and filtering by plan type.
    """
    service = PlatformService(db)
    orgs = service.list_organizations(skip=skip, limit=limit, plan=plan)
    
    # Convert to response with counts
    result = []
    for org in orgs:
        user_count = (
            db.query(User).filter(User.organization_id == org.id).count()
        )
        from app.db.models.campaign import Campaign
        campaign_count = (
            db.query(Campaign).filter(Campaign.organization_id == org.id).count()
        )
        result.append(PlatformOrganizationResponse(
            id=org.id,
            name=org.name,
            slug=org.slug,
            plan=org.plan.value,
            settings=org.settings,
            user_count=user_count,
            campaign_count=campaign_count,
            created_at=org.created_at,
            updated_at=org.updated_at,
        ))
    return result


@router.get("/organizations/{org_id}", response_model=PlatformOrganizationResponse)
def get_organization(
    org_id: UUID,
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    Get organization details by ID.
    """
    service = PlatformService(db)
    org = service.get_organization(org_id)
    
    # Get counts
    user_count = (
        db.query(User).filter(User.organization_id == org.id).count()
    )
    from app.db.models.campaign import Campaign
    campaign_count = (
        db.query(Campaign).filter(Campaign.organization_id == org.id).count()
    )
    
    return PlatformOrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        plan=org.plan.value,
        settings=org.settings,
        user_count=user_count,
        campaign_count=campaign_count,
        created_at=org.created_at,
        updated_at=org.updated_at,
    )


@router.post("/organizations", response_model=PlatformOrganizationResponse, status_code=201)
def create_organization(
    request: PlatformOrganizationCreate,
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    Create a new organization (platform admin only).
    """
    service = PlatformService(db)
    org = service.create_organization(
        name=request.name,
        plan=request.plan,
        settings=request.settings,
    )
    
    return PlatformOrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        plan=org.plan.value,
        settings=org.settings,
        user_count=0,
        campaign_count=0,
        created_at=org.created_at,
        updated_at=org.updated_at,
    )


@router.patch("/organizations/{org_id}", response_model=PlatformOrganizationResponse)
def update_organization(
    org_id: UUID,
    request: PlatformOrganizationUpdate,
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    Update organization details (plan, settings, etc.).
    """
    service = PlatformService(db)
    org = service.update_organization(
        org_id=org_id,
        name=request.name,
        plan=request.plan,
        settings=request.settings,
    )
    
    # Get counts
    user_count = (
        db.query(User).filter(User.organization_id == org.id).count()
    )
    from app.db.models.campaign import Campaign
    campaign_count = (
        db.query(Campaign).filter(Campaign.organization_id == org.id).count()
    )
    
    return PlatformOrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        plan=org.plan.value,
        settings=org.settings,
        user_count=user_count,
        campaign_count=campaign_count,
        created_at=org.created_at,
        updated_at=org.updated_at,
    )


@router.delete("/organizations/{org_id}", status_code=204)
def delete_organization(
    org_id: UUID,
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    Delete an organization (hard delete).
    """
    service = PlatformService(db)
    service.delete_organization(org_id)
    return None


@router.get("/users", response_model=List[PlatformUserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    organization_id: Optional[UUID] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    List all users with filters.
    
    Supports filtering by organization, role, and active status.
    """
    service = PlatformService(db)
    users = service.list_all_users(
        skip=skip,
        limit=limit,
        organization_id=organization_id,
        role=role,
        is_active=is_active,
    )
    
    # Convert to response
    result = []
    for user in users:
        org_name = None
        if user.organization_id and user.organization:
            org_name = user.organization.name
        
        result.append(PlatformUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.value,
            organization_id=user.organization_id,
            organization_name=org_name,
            is_active=user.is_active,
            email_verified_at=user.email_verified_at,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
        ))
    return result


@router.get("/system/metrics", response_model=PlatformSystemMetricsResponse)
def get_system_metrics(
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    Get system metrics (performance, latency, errors, etc.).
    """
    service = PlatformService(db)
    metrics = service.get_system_metrics()
    return PlatformSystemMetricsResponse(**metrics)


@router.post("/notifications/send", response_model=NotificationResponse)
def send_notification(
    request: SendNotificationRequest,
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    """
    Send notification (platform admin only).
    
    Supported types:
    - vectra_to_users: Send to all platform users
    - vectra_to_org_owner: Send to organization owners
    - system_alerts: System alerts
    """
    service = NotificationService(db)
    result = service.send_notification(
        notification_type=request.type,
        recipients=request.recipients,
        subject=request.subject,
        body=request.body,
        body_html=request.body_html,
        action_url=request.action_url,
        action_text=request.action_text,
        sender=current_user,
    )
    return NotificationResponse(**result)
