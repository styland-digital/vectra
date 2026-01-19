"""Notification service for sending notifications."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, UnauthorizedError
from app.db.models.user import User, UserRole
from app.services.resend import send_notification_email


class NotificationService:
    """Service for sending notifications."""

    def __init__(self, db: Session):
        self.db = db

    def send_notification(
        self,
        notification_type: str,
        recipients: List[str],
        subject: str,
        body: str,
        body_html: Optional[str] = None,
        action_url: Optional[str] = None,
        action_text: Optional[str] = None,
        sender: Optional[User] = None,
    ) -> dict:
        """
        Send notification based on type.
        
        Args:
            notification_type: Type of notification
            recipients: List of recipient identifiers (emails, org_id, or "all")
            subject: Email subject
            body: Plain text body
            body_html: HTML body (optional)
            action_url: Action button URL (optional)
            action_text: Action button text (optional)
            sender: User sending the notification
            
        Returns:
            Dictionary with success, message, sent_count, failed_count
            
        Raises:
            BadRequestError: If invalid notification type or recipients
            UnauthorizedError: If sender doesn't have permission
        """
        from app.db.repositories.user import UserRepository
        from app.db.repositories.organization import OrganizationRepository
        
        user_repo = UserRepository(self.db)
        org_repo = OrganizationRepository(self.db)
        
        # Platform admin notifications
        if notification_type in ["vectra_to_users", "vectra_to_org_owner", "system_alerts"]:
            if not sender or not sender.is_platform_admin():
                raise UnauthorizedError("Platform admin access required")
            
            recipient_emails = []
            
            if notification_type == "vectra_to_users":
                # Send to all users
                if "all" in recipients:
                    users = self.db.query(User).filter(
                        User.organization_id.isnot(None),
                        User.is_active == True
                    ).all()
                    recipient_emails = [user.email for user in users]
                else:
                    recipient_emails = recipients
            
            elif notification_type == "vectra_to_org_owner":
                # Send to organization owners
                if "all" in recipients:
                    users = self.db.query(User).filter(
                        User.role == UserRole.OWNER,
                        User.organization_id.isnot(None),
                        User.is_active == True
                    ).all()
                    recipient_emails = [user.email for user in users]
                else:
                    # Filter to only owners
                    users = self.db.query(User).filter(
                        User.email.in_(recipients),
                        User.role == UserRole.OWNER
                    ).all()
                    recipient_emails = [user.email for user in users]
            
            elif notification_type == "system_alerts":
                # Send to platform admin or all users (depending on recipients)
                if "all" in recipients:
                    users = self.db.query(User).filter(
                        User.is_active == True
                    ).all()
                    recipient_emails = [user.email for user in users]
                else:
                    recipient_emails = recipients
        
        # Organization notifications
        elif notification_type in ["org_to_prospects", "org_owner_to_members"]:
            if not sender or not sender.organization_id:
                raise UnauthorizedError("Organization user access required")
            
            org = org_repo.get_by_id(sender.organization_id)
            if not org:
                raise BadRequestError("Organization not found")
            
            if notification_type == "org_to_prospects":
                # Send to prospects (email list)
                if sender.role not in [UserRole.OWNER, UserRole.ADMIN]:
                    raise UnauthorizedError("Only Owner/Admin can send to prospects")
                recipient_emails = recipients
            
            elif notification_type == "org_owner_to_members":
                # Send to organization members
                if sender.role not in [UserRole.OWNER, UserRole.ADMIN]:
                    raise UnauthorizedError("Only Owner/Admin can send to members")
                
                if "all" in recipients:
                    users = self.db.query(User).filter(
                        User.organization_id == sender.organization_id,
                        User.is_active == True
                    ).all()
                    recipient_emails = [user.email for user in users]
                else:
                    # Validate emails belong to organization
                    users = self.db.query(User).filter(
                        User.email.in_(recipients),
                        User.organization_id == sender.organization_id
                    ).all()
                    recipient_emails = [user.email for user in users]
        else:
            raise BadRequestError(f"Invalid notification type: {notification_type}")
        
        # Send emails
        sent_count = 0
        failed_count = 0
        
        for email in recipient_emails:
            try:
                send_notification_email(
                    to=email,
                    title=subject,
                    body=body,
                    body_html=body_html,
                    action_url=action_url,
                    action_text=action_text,
                )
                sent_count += 1
            except Exception:
                failed_count += 1
        
        return {
            "success": failed_count == 0,
            "message": f"Notification sent to {sent_count} recipient(s)",
            "sent_count": sent_count,
            "failed_count": failed_count,
        }
