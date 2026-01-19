"""Email service for business logic."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from fastapi import HTTPException, status
from app.core.exceptions import NotFoundError, BadRequestError
from app.db.models.email import Email, EmailStatus
from app.db.models.lead import Lead
from app.db.models.user import User


class EmailService:
    """Service for email operations."""

    def __init__(self, db: Session):
        self.db = db

    def list_emails(
        self,
        user: User,
        campaign_id: Optional[UUID] = None,
        lead_id: Optional[UUID] = None,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Email], int]:
        """
        List emails for user's organization.
        
        Args:
            user: Current user
            campaign_id: Optional campaign filter
            lead_id: Optional lead filter
            status_filter: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (emails list, total count)
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        # Join with Lead to filter by organization
        query = (
            self.db.query(Email)
            .join(Lead, Email.lead_id == Lead.id)
            .filter(Lead.organization_id == user.organization_id)
        )
        
        if campaign_id:
            query = query.filter(Email.campaign_id == campaign_id)
        
        if lead_id:
            query = query.filter(Email.lead_id == lead_id)
        
        if status_filter:
            try:
                status_enum = EmailStatus(status_filter.lower())
                query = query.filter(Email.status == status_enum)
            except ValueError:
                raise BadRequestError(f"Invalid status: {status_filter}")
        
        total = query.count()
        emails = (
            query.options(joinedload(Email.lead))
            .order_by(desc(Email.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return emails, total

    def get_email(
        self,
        user: User,
        email_id: UUID,
    ) -> Email:
        """
        Get email by ID with all relationships.
        
        Args:
            user: Current user
            email_id: Email ID
            
        Returns:
            Email with relationships loaded
            
        Raises:
            NotFoundError: If email not found or not in user's org
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")
        
        email = (
            self.db.query(Email)
            .join(Lead, Email.lead_id == Lead.id)
            .options(
                joinedload(Email.lead),
                joinedload(Email.approved_by_user),
            )
            .filter(
                Email.id == email_id,
                Lead.organization_id == user.organization_id
            )
            .first()
        )
        
        if not email:
            raise NotFoundError("Email not found")
        
        return email

    def approve_email(
        self,
        user: User,
        email_id: UUID,
        subject: Optional[str] = None,
        body_html: Optional[str] = None,
    ) -> Email:
        """
        Approve an email for sending.
        
        Args:
            user: Current user (approver)
            email_id: Email ID
            subject: Optional subject modification
            body_html: Optional body modification
            
        Returns:
            Approved email
            
        Raises:
            NotFoundError: If email not found
            BadRequestError: If email cannot be approved
        """
        email = self.get_email(user, email_id)
        
        if email.status != EmailStatus.PENDING:
            raise BadRequestError(f"Cannot approve email with status: {email.status.value}")
        
        if subject is not None:
            email.subject = subject
        
        if body_html is not None:
            email.body = body_html
        
        email.status = EmailStatus.APPROVED
        email.approved_by = user.id
        email.approved_at = datetime.now(timezone.utc)
        
        self.db.commit()
        self.db.refresh(email)
        
        return email

    def reject_email(
        self,
        user: User,
        email_id: UUID,
        reason: str,
    ) -> Email:
        """
        Reject an email.
        
        Args:
            user: Current user (rejector)
            email_id: Email ID
            reason: Rejection reason
            
        Returns:
            Rejected email
            
        Raises:
            NotFoundError: If email not found
            BadRequestError: If email cannot be rejected
        """
        email = self.get_email(user, email_id)
        
        if email.status != EmailStatus.PENDING:
            raise BadRequestError(f"Cannot reject email with status: {email.status.value}")
        
        email.status = EmailStatus.REJECTED
        
        # Store rejection reason in a notes field if available
        # For now, we'll add it to the body or create a separate field
        
        self.db.commit()
        self.db.refresh(email)
        
        return email
