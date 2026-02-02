"""Organization service for business logic."""

import secrets
import string
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from app.core.exceptions import NotFoundError, BadRequestError
from app.core.security import get_password_hash
from app.core.config import settings
from app.db.repositories.organization import OrganizationRepository
from app.db.repositories.user import UserRepository
from app.db.models.organization import Organization, PlanType
from app.db.models.user import User, UserRole
from app.services.resend import ResendService


class OrganizationService:
    """Service for organization operations."""

    def __init__(self, db: Session):
        self.db = db
        self.org_repo = OrganizationRepository(db)
        self.user_repo = UserRepository(db)

    def get_my_organization(self, user: User) -> Organization:
        """
        Get current user's organization.
        
        Args:
            user: Current user
            
        Returns:
            Organization
            
        Raises:
            NotFoundError: If user has no organization
        """
        if not user.organization_id:
            raise NotFoundError("User does not belong to an organization")
        
        org = self.org_repo.get_by_id(user.organization_id)
        if not org:
            raise NotFoundError("Organization not found")
        return org

    def update_my_organization(
        self,
        user: User,
        name: Optional[str] = None,
        settings: Optional[dict] = None,
    ) -> Organization:
        """
        Update current user's organization.
        
        Only Owner/Admin can update organization.
        
        Args:
            user: Current user
            name: New name
            settings: New settings
            
        Returns:
            Updated organization
            
        Raises:
            UnauthorizedError: If user is not Owner/Admin
        """
        if user.role not in [UserRole.OWNER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Owner/Admin can update organization",
            )
        
        org = self.get_my_organization(user)
        
        if name:
            org = self.org_repo.update(org, name=name)
        
        if settings is not None:
            org = self.org_repo.update(org, settings=settings)
        
        return org

    def list_users(
        self,
        user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        """
        List users in current user's organization.
        
        Only Owner/Admin/Manager can list users.
        
        Args:
            user: Current user
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of users
            
        Raises:
            UnauthorizedError: If user is not Owner/Admin/Manager
        """
        if user.role not in [UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to list users",
            )
        
        org = self.get_my_organization(user)
        
        return (
            self.db.query(User)
            .filter(User.organization_id == org.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_user_role(
        self,
        user: User,
        target_user_id: UUID,
        new_role: str,
    ) -> User:
        """
        Update user role in organization.
        
        Only Owner/Admin can update roles.
        
        Args:
            user: Current user (Owner/Admin)
            target_user_id: User ID to update
            new_role: New role
            
        Returns:
            Updated user
            
        Raises:
            UnauthorizedError: If user is not Owner/Admin
            NotFoundError: If target user not found
            BadRequestError: If invalid role
        """
        if user.role not in [UserRole.OWNER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Owner/Admin can update user roles",
            )
        
        org = self.get_my_organization(user)
        
        target_user = self.user_repo.get_by_id(target_user_id)
        if not target_user or target_user.organization_id != org.id:
            raise NotFoundError("User not found in organization")
        
        try:
            role_enum = UserRole(new_role.lower())
        except ValueError:
            raise BadRequestError(f"Invalid role: {new_role}")
        
        # Don't allow changing Owner role
        if target_user.role == UserRole.OWNER and role_enum != UserRole.OWNER:
            raise BadRequestError("Cannot change Owner role")
        
        # Don't allow non-Owners to assign Owner role
        if user.role != UserRole.OWNER and role_enum == UserRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Owner can assign Owner role",
            )
        
        target_user.role = role_enum
        self.db.commit()
        self.db.refresh(target_user)
        
        return target_user

    def remove_user(
        self,
        user: User,
        target_user_id: UUID,
    ) -> None:
        """
        Remove user from organization.
        
        Only Owner/Admin can remove users.
        
        Args:
            user: Current user (Owner/Admin)
            target_user_id: User ID to remove
            
        Raises:
            UnauthorizedError: If user is not Owner/Admin
            NotFoundError: If target user not found
            BadRequestError: If trying to remove Owner
        """
        if user.role not in [UserRole.OWNER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Owner/Admin can remove users",
            )
        
        org = self.get_my_organization(user)
        
        target_user = self.user_repo.get_by_id(target_user_id)
        if not target_user or target_user.organization_id != org.id:
            raise NotFoundError("User not found in organization")
        
        # Don't allow removing Owner
        if target_user.role == UserRole.OWNER:
            raise BadRequestError("Cannot remove Owner from organization")
        
        # Soft delete: deactivate user
        target_user.is_active = False
        # Or hard delete: remove from organization
        target_user.organization_id = None
        self.db.commit()

    def create_user_directly(
        self,
        inviter: User,
        email: str,
        role: str,
        password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        send_welcome_email: bool = True,
    ) -> User:
        """
        Create user directly in organization without invitation flow.
        
        Only Owner/Admin can create users directly.
        If password is not provided, generates a temporary password.
        
        Args:
            inviter: User creating the account (Owner/Admin)
            email: Email address
            role: Role to assign
            password: Password (optional, will be generated if not provided)
            first_name: First name (optional)
            last_name: Last name (optional)
            send_welcome_email: Whether to send welcome email with password
            
        Returns:
            Created user
            
        Raises:
            HTTPException: If user is not Owner/Admin
            BadRequestError: If email already exists or invalid role
        """
        if inviter.role not in [UserRole.OWNER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Owner/Admin can create users directly",
            )
        
        org = self.get_my_organization(inviter)
        
        # Check if user already exists
        if self.user_repo.email_exists(email):
            existing_user = self.user_repo.get_by_email(email)
            if existing_user.organization_id == org.id:
                raise BadRequestError("User already belongs to this organization")
            raise BadRequestError("User with this email already exists")
        
        # Validate role
        try:
            role_enum = UserRole(role.lower())
        except ValueError:
            raise BadRequestError(f"Invalid role: {role}")
        
        # Generate password if not provided
        if not password:
            # Generate secure random password
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(alphabet) for _ in range(16))
        
        # Create user
        password_hash = get_password_hash(password)
        user = self.user_repo.create(
            email=email,
            password_hash=password_hash,
            organization_id=org.id,
            first_name=first_name or "",
            last_name=last_name or "",
            role=role_enum,
        )
        
        # Send welcome email if requested
        if send_welcome_email:
            try:
                email_service = ResendService()
                # TODO: Create welcome email template
                # For now, we'll just log that email should be sent
                from app.core.logging import get_logger
                logger = get_logger(__name__)
                logger.info(f"Welcome email should be sent to {email} with temporary password")
            except Exception:
                # Don't fail if email sending fails
                pass
        
        return user
