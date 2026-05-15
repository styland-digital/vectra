"""Meeting service for business logic."""

from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.core.exceptions import NotFoundError, BadRequestError
from app.core.logging import get_logger
from app.db.models.meeting import Meeting, MeetingStatus, MeetingOutcome
from app.db.models.user import User

logger = get_logger(__name__)


class MeetingService:
    """Service for meeting operations."""

    def __init__(self, db: Session):
        self.db = db

    def list_meetings(
        self,
        user: User,
        campaign_id: Optional[UUID] = None,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Meeting], int]:
        """
        List meetings for user's organization.

        Args:
            user: Current user
            campaign_id: Optional campaign filter
            status_filter: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (meetings list, total count)
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")

        query = self.db.query(Meeting).filter(
            Meeting.organization_id == user.organization_id
        )

        if campaign_id:
            query = query.filter(Meeting.campaign_id == campaign_id)

        if status_filter:
            try:
                status_enum = MeetingStatus(status_filter.lower())
                query = query.filter(Meeting.status == status_enum)
            except ValueError:
                raise BadRequestError(f"Invalid status: {status_filter}")

        total = query.count()
        meetings = (
            query
            .order_by(desc(Meeting.scheduled_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

        logger.info(
            f"list_meetings: total={total} org={user.organization_id} skip={skip} limit={limit}"
        )

        return meetings, total

    def get_meeting(
        self,
        user: User,
        meeting_id: UUID,
    ) -> Meeting:
        """
        Get meeting by ID for user's organization.

        Args:
            user: Current user
            meeting_id: Meeting ID

        Returns:
            Meeting instance

        Raises:
            NotFoundError: If meeting not found or not in user's org
        """
        if not user.organization_id:
            raise BadRequestError("User does not belong to an organization")

        meeting = (
            self.db.query(Meeting)
            .filter(
                Meeting.id == meeting_id,
                Meeting.organization_id == user.organization_id,
            )
            .first()
        )

        if not meeting:
            raise NotFoundError("Meeting not found")

        return meeting

    def update_meeting(
        self,
        user: User,
        meeting_id: UUID,
        notes: Optional[str] = None,
        outcome: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Meeting:
        """
        Update allowed fields on a meeting.

        Args:
            user: Current user
            meeting_id: Meeting ID
            notes: Optional notes to set
            outcome: Optional outcome value (MeetingOutcome enum string)
            status: Optional status value (MeetingStatus enum string)

        Returns:
            Updated meeting instance

        Raises:
            NotFoundError: If meeting not found
            BadRequestError: If provided values are invalid
        """
        meeting = self.get_meeting(user, meeting_id)

        if notes is not None:
            meeting.notes = notes

        if outcome is not None:
            try:
                meeting.outcome = MeetingOutcome(outcome.lower())
            except ValueError:
                valid = [o.value for o in MeetingOutcome]
                raise BadRequestError(
                    f"Invalid outcome: {outcome}. Valid values: {valid}"
                )

        if status is not None:
            try:
                new_status = MeetingStatus(status.lower())
                meeting.status = new_status
                if new_status == MeetingStatus.COMPLETED and not meeting.completed_at:
                    meeting.completed_at = datetime.now(timezone.utc)
                if new_status == MeetingStatus.NO_SHOW:
                    meeting.no_show = True
            except ValueError:
                valid = [s.value for s in MeetingStatus]
                raise BadRequestError(
                    f"Invalid status: {status}. Valid values: {valid}"
                )

        self.db.commit()
        self.db.refresh(meeting)

        logger.info(f"update_meeting: meeting_id={meeting_id} org={user.organization_id}")

        return meeting
