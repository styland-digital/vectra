"""Unit tests for NotificationService."""

import pytest
from unittest.mock import patch, MagicMock
from app.services.notification import NotificationService
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.db.models.user import User, UserRole
from app.db.models.organization import Organization, PlanType


class TestSendNotification:
    """Tests for NotificationService.send_notification method."""

    @patch('app.services.notification.send_notification_email')
    def test_send_notification_vectra_to_users(self, mock_send_email, db_session, test_organization):
        """Platform admin should be able to send to all users."""
        mock_send_email.return_value = {"id": "email-id", "success": True}

        # Create platform admin
        platform_admin = User(
            email="admin@vectra.io",
            password_hash="hash",
            organization_id=None,
            role=UserRole.PLATFORM_ADMIN,
            is_active=True,
        )
        db_session.add(platform_admin)

        # Create regular users
        user1 = User(
            email="user1@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        user2 = User(
            email="user2@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add_all([platform_admin, user1, user2])
        db_session.commit()

        service = NotificationService(db_session)
        result = service.send_notification(
            notification_type="vectra_to_users",
            recipients=["all"],
            subject="Test Subject",
            body="Test Body",
            sender=platform_admin,
        )

        assert result["success"] is True
        assert result["sent_count"] == 2

    @patch('app.services.notification.send_notification_email')
    def test_send_notification_org_to_prospects(self, mock_send_email, db_session, test_owner_user):
        """Owner should be able to send to prospects."""
        mock_send_email.return_value = {"id": "email-id", "success": True}

        service = NotificationService(db_session)
        result = service.send_notification(
            notification_type="org_to_prospects",
            recipients=["prospect1@example.com", "prospect2@example.com"],
            subject="Test Subject",
            body="Test Body",
            sender=test_owner_user,
        )

        assert result["success"] is True
        assert result["sent_count"] == 2

    def test_send_notification_org_to_prospects_as_operator_raises(self, db_session, test_user):
        """Operator should not be able to send to prospects."""
        service = NotificationService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            service.send_notification(
                notification_type="org_to_prospects",
                recipients=["prospect@example.com"],
                subject="Test Subject",
                body="Test Body",
                sender=test_user,
            )

        assert "Only Owner/Admin" in str(exc_info.value.detail)

    def test_send_notification_invalid_type_raises(self, db_session, test_owner_user):
        """Invalid notification type should raise BadRequestError."""
        service = NotificationService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.send_notification(
                notification_type="invalid_type",
                recipients=["user@example.com"],
                subject="Test Subject",
                body="Test Body",
                sender=test_owner_user,
            )

        assert "Invalid notification type" in str(exc_info.value.detail)

    def test_send_notification_vectra_to_users_as_non_admin_raises(self, db_session, test_owner_user):
        """Non-platform admin should not be able to send vectra notifications."""
        service = NotificationService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            service.send_notification(
                notification_type="vectra_to_users",
                recipients=["all"],
                subject="Test Subject",
                body="Test Body",
                sender=test_owner_user,
            )

        assert "Platform admin access required" in str(exc_info.value.detail)
