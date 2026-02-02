"""Campaign service for business logic."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from fastapi import HTTPException, status
from app.core.exceptions import NotFoundError, BadRequestError
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead, LeadStatus
from app.db.models.email import Email
from app.db.models.user import User
from app.orchestrator.campaign_runner import CampaignRunner


class CampaignService:
    """Service for campaign operations."""

    def __init__(self, db: Session):
        self.db = db

    def list_campaigns(
        self,
        user: User,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[str] = None,
    ) -> List[Campaign]:
        """
        List campaigns for user's organization.
        
        Args:
            user: Current user
            skip: Number of records to skip
            limit: Maximum number of records to return
            status_filter: Optional status filter
            
        Returns:
            List of campaigns
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        query = self.db.query(Campaign).filter(
            Campaign.organization_id == user.organization_id
        )
        
        if status_filter:
            try:
                status_enum = CampaignStatus(status_filter.lower())
                query = query.filter(Campaign.status == status_enum)
            except ValueError:
                raise BadRequestError(f"Invalid status: {status_filter}")
        
        return query.order_by(Campaign.created_at.desc()).offset(skip).limit(limit).all()

    def get_campaign(
        self,
        user: User,
        campaign_id: UUID,
    ) -> Campaign:
        """
        Get campaign by ID.
        
        Args:
            user: Current user
            campaign_id: Campaign ID
            
        Returns:
            Campaign
            
        Raises:
            NotFoundError: If campaign not found or not in user's org
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        campaign = self.db.query(Campaign).filter(
            Campaign.id == campaign_id,
            Campaign.organization_id == user.organization_id
        ).first()
        
        if not campaign:
            raise NotFoundError("Campaign not found")
        
        return campaign

    def create_campaign(
        self,
        user: User,
        name: str,
        description: Optional[str] = None,
        target_criteria: Optional[Dict[str, Any]] = None,
        email_template: Optional[Dict[str, Any]] = None,
        bant_threshold: int = 60,
        daily_limit: int = 50,
    ) -> Campaign:
        """
        Create a new campaign.
        
        Args:
            user: Current user (creator)
            name: Campaign name
            description: Campaign description
            target_criteria: Targeting criteria for Prospector
            email_template: Email template for Scheduler
            bant_threshold: BANT qualification threshold (0-100)
            daily_limit: Daily email sending limit
            
        Returns:
            Created campaign
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        campaign = Campaign(
            organization_id=user.organization_id,
            created_by=user.id,
            name=name,
            description=description,
            target_criteria=target_criteria or {},
            email_template=email_template,
            bant_threshold=bant_threshold,
            daily_limit=daily_limit,
            status=CampaignStatus.DRAFT,
        )
        
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        
        return campaign

    def update_campaign(
        self,
        user: User,
        campaign_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        target_criteria: Optional[Dict[str, Any]] = None,
        email_template: Optional[Dict[str, Any]] = None,
        bant_threshold: Optional[int] = None,
        daily_limit: Optional[int] = None,
    ) -> Campaign:
        """
        Update campaign.
        
        Can only update DRAFT campaigns.
        
        Args:
            user: Current user
            campaign_id: Campaign ID
            name: New name
            description: New description
            target_criteria: New target criteria
            email_template: New email template
            bant_threshold: New BANT threshold
            daily_limit: New daily limit
            
        Returns:
            Updated campaign
        """
        campaign = self.get_campaign(user, campaign_id)
        
        # Only allow updates to DRAFT campaigns
        if campaign.status != CampaignStatus.DRAFT:
            raise BadRequestError("Can only update DRAFT campaigns")
        
        if name is not None:
            campaign.name = name
        if description is not None:
            campaign.description = description
        if target_criteria is not None:
            campaign.target_criteria = target_criteria
        if email_template is not None:
            campaign.email_template = email_template
        if bant_threshold is not None:
            if not 0 <= bant_threshold <= 100:
                raise BadRequestError("BANT threshold must be between 0 and 100")
            campaign.bant_threshold = bant_threshold
        if daily_limit is not None:
            if daily_limit < 1:
                raise BadRequestError("Daily limit must be at least 1")
            campaign.daily_limit = daily_limit
        
        self.db.commit()
        self.db.refresh(campaign)
        
        return campaign

    def launch_campaign(
        self,
        user: User,
        campaign_id: UUID,
    ) -> Campaign:
        """
        Launch a campaign (change status to ACTIVE and start execution).
        
        Args:
            user: Current user
            campaign_id: Campaign ID
            
        Returns:
            Updated campaign
        """
        campaign = self.get_campaign(user, campaign_id)
        
        # Only allow launching DRAFT campaigns
        if campaign.status != CampaignStatus.DRAFT:
            raise BadRequestError("Can only launch DRAFT campaigns")
        
        # Validate required fields
        if not campaign.target_criteria:
            raise BadRequestError("Target criteria required to launch campaign")
        
        # Update status
        campaign.status = CampaignStatus.ACTIVE
        if not campaign.started_at:
            campaign.started_at = datetime.now(timezone.utc)
        
        self.db.commit()
        self.db.refresh(campaign)
        
        # Start campaign execution asynchronously (via Celery task)
        # For now, we'll just update the status
        # TODO: Trigger Celery task to run campaign
        
        return campaign

    def pause_campaign(
        self,
        user: User,
        campaign_id: UUID,
    ) -> Campaign:
        """
        Pause an active campaign.
        
        Args:
            user: Current user
            campaign_id: Campaign ID
            
        Returns:
            Updated campaign
        """
        campaign = self.get_campaign(user, campaign_id)
        
        # Only allow pausing ACTIVE campaigns
        if campaign.status != CampaignStatus.ACTIVE:
            raise BadRequestError("Can only pause ACTIVE campaigns")
        
        campaign.status = CampaignStatus.PAUSED
        self.db.commit()
        self.db.refresh(campaign)
        
        return campaign

    def resume_campaign(
        self,
        user: User,
        campaign_id: UUID,
    ) -> Campaign:
        """
        Resume a paused campaign.
        
        Args:
            user: Current user
            campaign_id: Campaign ID
            
        Returns:
            Updated campaign
        """
        campaign = self.get_campaign(user, campaign_id)
        
        # Only allow resuming PAUSED campaigns
        if campaign.status != CampaignStatus.PAUSED:
            raise BadRequestError("Can only resume PAUSED campaigns")
        
        campaign.status = CampaignStatus.ACTIVE
        self.db.commit()
        self.db.refresh(campaign)
        
        return campaign

    def delete_campaign(
        self,
        user: User,
        campaign_id: UUID,
    ) -> None:
        """
        Delete a campaign (soft delete - archive).
        
        Args:
            user: Current user
            campaign_id: Campaign ID
        """
        campaign = self.get_campaign(user, campaign_id)
        
        # Soft delete: archive instead of hard delete
        campaign.status = CampaignStatus.ARCHIVED
        self.db.commit()

    def get_campaign_stats(
        self,
        user: User,
        campaign_id: UUID,
    ) -> Dict[str, Any]:
        """
        Get campaign statistics.
        
        Args:
            user: Current user
            campaign_id: Campaign ID
            
        Returns:
            Dictionary with campaign statistics
        """
        campaign = self.get_campaign(user, campaign_id)
        
        # Count leads by status
        leads_total = self.db.query(Lead).filter(Lead.campaign_id == campaign_id).count()
        leads_qualified = self.db.query(Lead).filter(
            Lead.campaign_id == campaign_id,
            Lead.status.in_([LeadStatus.QUALIFIED, LeadStatus.CONTACTED, LeadStatus.MEETING_SCHEDULED, LeadStatus.COMPLETED])
        ).count()
        leads_rejected = self.db.query(Lead).filter(
            Lead.campaign_id == campaign_id,
            Lead.status == LeadStatus.REJECTED
        ).count()
        
        # Count emails
        emails_sent = self.db.query(Email).filter(Email.campaign_id == campaign_id).count()
        
        # Calculate average BANT score
        avg_bant = self.db.query(
            func.avg(Lead.bant_score)
        ).filter(Lead.campaign_id == campaign_id).scalar() or 0
        
        return {
            "campaign_id": str(campaign_id),
            "status": campaign.status.value,
            "leads": {
                "total": leads_total,
                "qualified": leads_qualified,
                "rejected": leads_rejected,
            },
            "emails": {
                "sent": emails_sent,
            },
            "bant": {
                "average_score": float(avg_bant),
                "threshold": campaign.bant_threshold,
            },
            "started_at": campaign.started_at.isoformat() if campaign.started_at else None,
            "completed_at": campaign.completed_at.isoformat() if campaign.completed_at else None,
        }
