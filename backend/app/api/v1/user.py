"""User and organization API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import (
    get_db,
    get_current_user,
    get_organization_user,
    require_role,
)
from app.schemas.auth import UserResponse, MessageResponse
from app.schemas.organization import (
    OrganizationResponse,
    OrganizationUpdate,
    OrganizationUserResponse,
    InviteUserRequest,
    UpdateUserRoleRequest,
    CreateUserRequest,
)
from app.schemas.notification import SendNotificationRequest, NotificationResponse
from app.db.models.user import User, UserRole
from app.services.organization import OrganizationService
from app.services.invitation import InvitationService
from app.services.notification import NotificationService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user profile.
    
    Works for all users (platform admin and organization users).
    """
    return current_user


@router.get("/organizations/me", response_model=OrganizationResponse)
def get_my_organization(
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Get current user's organization details.
    """
    service = OrganizationService(db)
    org = service.get_my_organization(current_user)
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        plan=org.plan.value,
        settings=org.settings,
        created_at=org.created_at,
        updated_at=org.updated_at,
    )


@router.patch("/organizations/me", response_model=OrganizationResponse)
def update_my_organization(
    request: OrganizationUpdate,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Update current user's organization.
    
    Only Owner/Admin can update organization.
    """
    service = OrganizationService(db)
    org = service.update_my_organization(
        user=current_user,
        name=request.name,
        settings=request.settings,
    )
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        plan=org.plan.value,
        settings=org.settings,
        created_at=org.created_at,
        updated_at=org.updated_at,
    )


@router.get("/organizations/me/users", response_model=List[OrganizationUserResponse])
def list_organization_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    List users in current user's organization.
    
    Only Owner/Admin/Manager can list users.
    """
    if current_user.role not in [UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    
    service = OrganizationService(db)
    users = service.list_users(user=current_user, skip=skip, limit=limit)
    
    return [
        OrganizationUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.value,
            is_active=user.is_active,
            email_verified_at=user.email_verified_at,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
        )
        for user in users
    ]


@router.post("/organizations/me/users/invite", response_model=MessageResponse)
def invite_user(
    request: InviteUserRequest,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Invite a user to the organization.
    
    Only Owner/Admin can invite users.
    """
    if current_user.role not in [UserRole.OWNER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner/Admin can invite users",
        )
    
    service = InvitationService(db)
    token = service.invite_user(
        inviter=current_user,
        email=request.email,
        role=request.role,
        first_name=request.first_name,
        last_name=request.last_name,
    )
    
    return MessageResponse(message=f"Invitation sent to {request.email}")


@router.post("/organizations/me/users/create", response_model=OrganizationUserResponse, status_code=201)
def create_user_directly(
    request: CreateUserRequest,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Create user directly in organization (no invitation email).
    
    Only Owner/Admin can create users directly.
    If password is not provided, a temporary password will be generated.
    """
    if current_user.role not in [UserRole.OWNER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner/Admin can create users directly",
        )
    
    service = OrganizationService(db)
    user = service.create_user_directly(
        inviter=current_user,
        email=request.email,
        role=request.role,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
        send_welcome_email=request.send_welcome_email,
    )
    
    return OrganizationUserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role.value,
        is_active=user.is_active,
        email_verified_at=user.email_verified_at,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
    )


@router.patch("/organizations/me/users/{user_id}/role", response_model=OrganizationUserResponse)
def update_user_role(
    user_id: UUID,
    request: UpdateUserRoleRequest,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Update user role in organization.
    
    Only Owner/Admin can update roles.
    """
    service = OrganizationService(db)
    user = service.update_user_role(
        user=current_user,
        target_user_id=user_id,
        new_role=request.role,
    )
    
    return OrganizationUserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role.value,
        is_active=user.is_active,
        email_verified_at=user.email_verified_at,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
    )


@router.delete("/organizations/me/users/{user_id}", status_code=204)
def remove_user(
    user_id: UUID,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Remove user from organization.
    
    Only Owner/Admin can remove users.
    """
    service = OrganizationService(db)
    service.remove_user(user=current_user, target_user_id=user_id)
    return None


@router.post("/notifications/send", response_model=NotificationResponse)
def send_notification(
    request: SendNotificationRequest,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db),
):
    """
    Send notification (organization user).
    
    Supported types:
    - org_to_prospects: Send to list of prospects (emails)
    - org_owner_to_members: Send to organization members
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
