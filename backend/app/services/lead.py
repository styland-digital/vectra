"""Lead service for business logic."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func, desc

from fastapi import HTTPException, status
from app.core.exceptions import NotFoundError, BadRequestError
from app.db.models.lead import Lead, LeadStatus, LeadIntent
from app.db.models.email import Email
from app.db.models.meeting import Meeting
from app.db.models.agent_run import AgentRun, AgentType
from app.db.models.user import User


class LeadService:
    """Service for lead operations."""

    def __init__(self, db: Session):
        self.db = db

    def list_leads(
        self,
        user: User,
        campaign_id: Optional[UUID] = None,
        status_filter: Optional[str] = None,
        intent_filter: Optional[str] = None,
        bant_score_min: Optional[int] = None,
        bant_score_max: Optional[int] = None,
        search: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Lead], int]:
        """
        List leads for user's organization.
        
        Args:
            user: Current user
            campaign_id: Optional campaign filter
            status_filter: Optional status filter
            intent_filter: Optional intent filter
            bant_score_min: Minimum BANT score
            bant_score_max: Maximum BANT score
            search: Search query (name, email, company)
            created_after: Filter by creation date (after)
            created_before: Filter by creation date (before)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (leads list, total count)
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        query = self.db.query(Lead).filter(
            Lead.organization_id == user.organization_id
        )
        
        if campaign_id:
            query = query.filter(Lead.campaign_id == campaign_id)
        
        if status_filter:
            try:
                status_enum = LeadStatus(status_filter.lower())
                query = query.filter(Lead.status == status_enum)
            except ValueError:
                raise BadRequestError(f"Invalid status: {status_filter}")
        
        if intent_filter:
            try:
                intent_enum = LeadIntent(intent_filter.lower())
                query = query.filter(Lead.intent == intent_enum)
            except ValueError:
                raise BadRequestError(f"Invalid intent: {intent_filter}")
        
        if bant_score_min is not None:
            query = query.filter(Lead.bant_score >= bant_score_min)
        
        if bant_score_max is not None:
            query = query.filter(Lead.bant_score <= bant_score_max)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Lead.first_name.ilike(search_pattern),
                    Lead.last_name.ilike(search_pattern),
                    Lead.email.ilike(search_pattern),
                    Lead.company_name.ilike(search_pattern),
                )
            )
        
        if created_after:
            query = query.filter(Lead.created_at >= created_after)
        
        if created_before:
            query = query.filter(Lead.created_at <= created_before)
        
        total = query.count()
        leads = query.order_by(desc(Lead.created_at)).offset(skip).limit(limit).all()
        
        return leads, total

    def get_lead(
        self,
        user: User,
        lead_id: UUID,
    ) -> Lead:
        """
        Get lead by ID with all relationships.
        
        Args:
            user: Current user
            lead_id: Lead ID
            
        Returns:
            Lead with relationships loaded
            
        Raises:
            NotFoundError: If lead not found or not in user's org
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        lead = (
            self.db.query(Lead)
            .options(
                joinedload(Lead.emails),
                joinedload(Lead.meetings),
                joinedload(Lead.campaign),
            )
            .filter(
                Lead.id == lead_id,
                Lead.organization_id == user.organization_id
            )
            .first()
        )
        
        if not lead:
            raise NotFoundError("Lead not found")
        
        return lead

    def get_lead_interactions(
        self,
        user: User,
        lead_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        Get interactions for a lead.
        
        Interactions are generated from:
        - Agent runs (prospector_found, bant_scored, email_generated)
        - Emails (email_sent, email_opened, email_clicked, email_replied)
        - Meetings (meeting_scheduled, meeting_completed)
        
        Args:
            user: Current user
            lead_id: Lead ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (interactions list, total count)
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        # Verify lead exists and belongs to org
        lead = self.get_lead(user, lead_id)
        
        interactions = []
        
        # Get emails as interactions
        emails = (
            self.db.query(Email)
            .filter(Email.lead_id == lead_id)
            .order_by(desc(Email.created_at))
            .all()
        )
        
        for email in emails:
            interactions.append({
                "id": email.id,
                "type": f"email_{email.status.value}",
                "agent_type": "scheduler",
                "data": {
                    "subject": email.subject,
                    "body_preview": email.body[:100] if email.body else None,
                    "status": email.status.value,
                },
                "created_at": email.created_at,
            })
        
        # Get meetings as interactions
        meetings = (
            self.db.query(Meeting)
            .filter(Meeting.lead_id == lead_id)
            .order_by(desc(Meeting.created_at))
            .all()
        )
        
        for meeting in meetings:
            interactions.append({
                "id": meeting.id,
                "type": f"meeting_{meeting.status.value}",
                "agent_type": "scheduler",
                "data": {
                    "scheduled_at": meeting.scheduled_at.isoformat() if meeting.scheduled_at else None,
                    "status": meeting.status.value,
                    "meeting_url": meeting.meeting_url,
                },
                "created_at": meeting.created_at,
            })
        
        # Get agent runs for the campaign as interactions
        agent_runs = (
            self.db.query(AgentRun)
            .filter(AgentRun.campaign_id == lead.campaign_id)
            .order_by(desc(AgentRun.created_at))
            .limit(50)  # Limit to recent runs
            .all()
        )
        
        for run in agent_runs:
            # Map agent type to interaction type
            interaction_type_map = {
                AgentType.PROSPECTOR: "prospector_found",
                AgentType.BANT_QUALIFIER: "bant_scored",
                AgentType.SCHEDULER: "email_generated",
                AgentType.INTENT_CLASSIFIER: "intent_classified",
            }
            
            interaction_type = interaction_type_map.get(run.agent_type, "agent_run")
            
            interactions.append({
                "id": run.id,
                "type": interaction_type,
                "agent_type": run.agent_type.value,
                "data": {
                    "status": run.status.value,
                    "output_data": run.output_data,
                },
                "created_at": run.created_at,
            })
        
        # Sort all interactions by created_at desc
        interactions.sort(key=lambda x: x["created_at"], reverse=True)
        
        total = len(interactions)
        paginated_interactions = interactions[skip:skip + limit]
        
        return paginated_interactions, total

    def update_lead(
        self,
        user: User,
        lead_id: UUID,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company_name: Optional[str] = None,
        job_title: Optional[str] = None,
        status: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Lead:
        """
        Update lead manually.
        
        Args:
            user: Current user
            lead_id: Lead ID
            first_name: First name
            last_name: Last name
            phone: Phone number
            company_name: Company name
            job_title: Job title
            status: Lead status
            notes: Notes (stored in enrichment_data for now)
            
        Returns:
            Updated lead
            
        Raises:
            NotFoundError: If lead not found or not in user's org
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        lead = self.get_lead(user, lead_id)
        
        if first_name is not None:
            lead.first_name = first_name
        if last_name is not None:
            lead.last_name = last_name
        if phone is not None:
            lead.phone = phone
        if company_name is not None:
            lead.company_name = company_name
        if job_title is not None:
            lead.job_title = job_title
        if status is not None:
            try:
                lead.status = LeadStatus(status.lower())
            except ValueError:
                raise BadRequestError(f"Invalid status: {status}")
        if notes is not None:
            # Store notes in enrichment_data for now
            if lead.enrichment_data is None:
                lead.enrichment_data = {}
            lead.enrichment_data["notes"] = notes
        
        self.db.commit()
        self.db.refresh(lead)
        
        return lead
