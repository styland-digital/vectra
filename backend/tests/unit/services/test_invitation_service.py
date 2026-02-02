"""Unit tests for InvitationService."""

import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from app.services.invitation import InvitationService
from app.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError
from app.db.models.user import User, UserRole
from app.db.models.organization import Organization, PlanType
from app.db.models.invitation import Invitation


class TestInviteUser:
    """Tests for InvitationService.invite_user method."""

    @patch('app.services.invitation.ResendService')
    def test_invite_user_success(self, mock_resend_service, db_session, test_owner_user, test_organization):
        """Should send invitation email and return OTP."""
        # Mock email service
        mock_service = MagicMock()
        mock_resend_service.return_value = mock_service
        mock_service.send_invitation_email.return_value = {"id": "email-id", "success": True}

        service = InvitationService(db_session)
        otp = service.invite_user(
            inviter=test_owner_user,
            email="newuser@example.com",
            role="operator",
            first_name="New",
            last_name="User",
        )

        assert otp is not None
        assert len(otp) == 6
        assert otp.isdigit()
        
        # Verify invitation was created in DB
        invitation = db_session.query(Invitation).filter(
            Invitation.email == "newuser@example.com"
        ).first()
        assert invitation is not None
        assert invitation.otp == otp
        assert invitation.organization_id == test_owner_user.organization_id

    def test_invite_user_duplicate_email_raises(self, db_session, test_owner_user, test_user):
        """Should raise BadRequestError if email already exists in organization."""
        service = InvitationService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.invite_user(
                inviter=test_owner_user,
                email=test_user.email,  # Already exists
                role="operator",
            )

        assert "already belongs" in str(exc_info.value.detail).lower()

    def test_invite_user_invalid_role_raises(self, db_session, test_owner_user):
        """Should raise BadRequestError for invalid role."""
        service = InvitationService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.invite_user(
                inviter=test_owner_user,
                email="newuser@example.com",
                role="invalid_role",
            )

        assert "Invalid role" in str(exc_info.value.detail)


class TestAcceptInvitation:
    """Tests for InvitationService.accept_invitation method."""

    def test_accept_invitation_success(self, db_session, test_owner_user, test_organization):
        """Should create user from invitation OTP."""
        # Create invitation
        invitation = Invitation(
            email="invited@example.com",
            organization_id=test_organization.id,
            role="operator",
            invited_by=test_owner_user.id,
            otp="123456",
            otp_expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        db_session.add(invitation)
        db_session.commit()

        service = InvitationService(db_session)
        access_token, refresh_token, user = service.accept_invitation(
            email="invited@example.com",
            otp="123456",
            password="password123",
        )

        assert user.email == "invited@example.com"
        assert user.organization_id == test_organization.id
        assert user.role == UserRole.OPERATOR
        assert access_token is not None
        assert refresh_token is not None
        
        # Verify invitation was deleted
        invitation_check = db_session.query(Invitation).filter(
            Invitation.email == "invited@example.com"
        ).first()
        assert invitation_check is None

    def test_accept_invitation_invalid_otp_raises(self, db_session, test_owner_user, test_organization):
        """Should raise UnauthorizedError for invalid OTP."""
        service = InvitationService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            service.accept_invitation(
                email="test@example.com",
                otp="000000",
                password="password123",
            )

        detail_str = str(exc_info.value.detail).lower()
        assert "invalid" in detail_str or "expired" in detail_str

    def test_accept_invitation_expired_otp_raises(self, db_session, test_owner_user, test_organization):
        """Should raise UnauthorizedError for expired OTP."""
        # Create expired invitation
        invitation = Invitation(
            email="expired@example.com",
            organization_id=test_organization.id,
            role="operator",
            invited_by=test_owner_user.id,
            otp="123456",
            otp_expires_at=datetime.now(timezone.utc) - timedelta(days=1),  # Expired
        )
        db_session.add(invitation)
        db_session.commit()

        service = InvitationService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            service.accept_invitation(
                email="expired@example.com",
                otp="123456",
                password="password123",
            )

        detail_str = str(exc_info.value.detail).lower()
        assert "invalid" in detail_str or "expired" in detail_str

    def test_accept_invitation_duplicate_email_raises(self, db_session, test_user, test_owner_user, test_organization):
        """Should raise BadRequestError if user already exists."""
        # Create invitation with existing email
        invitation = Invitation(
            email=test_user.email,
            organization_id=test_organization.id,
            role="operator",
            invited_by=test_owner_user.id,
            otp="123456",
            otp_expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        db_session.add(invitation)
        db_session.commit()

        service = InvitationService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.accept_invitation(
                email=test_user.email,
                otp="123456",
                password="password123",
            )

        assert "already exists" in str(exc_info.value.detail).lower()
        
        # Verify invitation was deleted
        invitation_check = db_session.query(Invitation).filter(
            Invitation.email == test_user.email
        ).first()
        assert invitation_check is None
