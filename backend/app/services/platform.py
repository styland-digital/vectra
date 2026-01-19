"""Platform admin service for business logic."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.core.exceptions import NotFoundError, BadRequestError
from app.db.repositories.organization import OrganizationRepository
from app.db.repositories.user import UserRepository
from app.db.models.organization import Organization, PlanType
from app.db.models.user import User


class PlatformService:
    """Service for platform admin operations."""

    def __init__(self, db: Session):
        self.db = db
        self.org_repo = OrganizationRepository(db)
        self.user_repo = UserRepository(db)

    def get_overview(self) -> dict:
        """
        Get platform overview statistics.
        
        Returns:
            Dictionary with statistics
        """
        # Count organizations
        total_orgs = self.db.query(func.count(Organization.id)).scalar() or 0
        
        # Count users (exclude platform admins)
        total_users = (
            self.db.query(func.count(User.id))
            .filter(User.organization_id.isnot(None))
            .scalar() or 0
        )
        
        # Count active campaigns
        from app.db.models.campaign import Campaign, CampaignStatus
        active_campaigns = (
            self.db.query(func.count(Campaign.id))
            .filter(Campaign.status == CampaignStatus.ACTIVE)
            .scalar() or 0
        )
        
        # Count total leads
        from app.db.models.lead import Lead
        total_leads = self.db.query(func.count(Lead.id)).scalar() or 0
        
        # Calculate conversion rate
        from app.db.models.lead import LeadStatus
        qualified_leads = (
            self.db.query(func.count(Lead.id))
            .filter(Lead.status.in_([
                LeadStatus.QUALIFIED,
                LeadStatus.CONTACTED,
                LeadStatus.MEETING_SCHEDULED,
                LeadStatus.COMPLETED,
            ]))
            .scalar() or 0
        )
        conversion_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0.0
        
        # Count emails sent
        from app.db.models.email import Email, EmailStatus
        emails_sent = (
            self.db.query(func.count(Email.id))
            .filter(Email.status.in_([EmailStatus.SENT, EmailStatus.DELIVERED]))
            .scalar() or 0
        )
        
        # Count meetings scheduled
        from app.db.models.meeting import Meeting, MeetingStatus
        meetings_scheduled = (
            self.db.query(func.count(Meeting.id))
            .filter(Meeting.status.in_([MeetingStatus.SCHEDULED, MeetingStatus.CONFIRMED]))
            .scalar() or 0
        )
        
        return {
            "total_organizations": total_orgs,
            "total_users": total_users,
            "active_campaigns": active_campaigns,
            "total_leads": total_leads,
            "conversion_rate": round(conversion_rate, 2),
            "emails_sent": emails_sent,
            "meetings_scheduled": meetings_scheduled,
        }

    def list_organizations(
        self,
        skip: int = 0,
        limit: int = 100,
        plan: Optional[str] = None,
    ) -> List[Organization]:
        """
        List all organizations with filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            plan: Filter by plan type
            
        Returns:
            List of organizations
        """
        query = self.db.query(Organization)
        
        if plan:
            try:
                plan_enum = PlanType(plan.lower())
                query = query.filter(Organization.plan == plan_enum)
            except ValueError:
                raise BadRequestError(f"Invalid plan type: {plan}")
        
        return query.offset(skip).limit(limit).all()

    def get_organization(self, org_id: UUID) -> Organization:
        """
        Get organization by ID.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Organization
            
        Raises:
            NotFoundError: If organization not found
        """
        org = self.org_repo.get_by_id(org_id)
        if not org:
            raise NotFoundError("Organization not found")
        return org

    def create_organization(
        self,
        name: str,
        plan: Optional[str] = None,
        settings: Optional[dict] = None,
    ) -> Organization:
        """
        Create a new organization.
        
        Args:
            name: Organization name
            plan: Plan type (default: trial)
            settings: Optional settings dictionary
            
        Returns:
            Created organization
        """
        plan_enum = PlanType.TRIAL
        if plan:
            try:
                plan_enum = PlanType(plan.lower())
            except ValueError:
                raise BadRequestError(f"Invalid plan type: {plan}")
        
        org = self.org_repo.create(
            name=name,
            plan=plan_enum,
        )
        
        if settings:
            org = self.org_repo.update(org, settings=settings)
        
        return org

    def update_organization(
        self,
        org_id: UUID,
        name: Optional[str] = None,
        plan: Optional[str] = None,
        settings: Optional[dict] = None,
    ) -> Organization:
        """
        Update organization.
        
        Args:
            org_id: Organization ID
            name: New name
            plan: New plan type
            settings: New settings
            
        Returns:
            Updated organization
            
        Raises:
            NotFoundError: If organization not found
        """
        org = self.get_organization(org_id)
        
        if name:
            org = self.org_repo.update(org, name=name)
        
        if plan:
            try:
                plan_enum = PlanType(plan.lower())
                org = self.org_repo.upgrade_plan(org, plan_enum)
            except ValueError:
                raise BadRequestError(f"Invalid plan type: {plan}")
        
        if settings is not None:
            org = self.org_repo.update(org, settings=settings)
        
        return org

    def delete_organization(self, org_id: UUID) -> None:
        """
        Delete organization (hard delete).
        
        Args:
            org_id: Organization ID
            
        Raises:
            NotFoundError: If organization not found
        """
        org = self.get_organization(org_id)
        self.db.delete(org)
        self.db.commit()

    def list_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        organization_id: Optional[UUID] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> List[User]:
        """
        List all users with filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            organization_id: Filter by organization
            role: Filter by role
            is_active: Filter by active status
            
        Returns:
            List of users
        """
        query = self.db.query(User).filter(User.organization_id.isnot(None))
        
        if organization_id:
            query = query.filter(User.organization_id == organization_id)
        
        if role:
            from app.db.models.user import UserRole
            try:
                role_enum = UserRole(role.lower())
                query = query.filter(User.role == role_enum)
            except ValueError:
                raise BadRequestError(f"Invalid role: {role}")
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()

    def get_system_metrics(self) -> dict:
        """
        Get system metrics.
        
        Returns:
            Dictionary with system metrics
        """
        # For now, return placeholder metrics
        # In production, these would be collected from monitoring system
        return {
            "api_requests_per_minute": 0.0,
            "average_response_time_ms": 0.0,
            "agent_latency_avg_ms": 0.0,
            "error_rate": 0.0,
            "active_users": (
                self.db.query(func.count(User.id))
                .filter(User.is_active == True)
                .filter(User.organization_id.isnot(None))
                .scalar() or 0
            ),
        }
