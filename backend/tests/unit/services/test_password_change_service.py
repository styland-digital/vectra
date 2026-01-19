"""Unit tests for PasswordChangeService."""

import pytest
from datetime import datetime, timedelta, timezone
from app.services.password_change import PasswordChangeService
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.db.models.user import User, UserRole


class TestRequestPasswordChange:
    """Tests for PasswordChangeService.request_password_change method."""

    def test_request_password_change_success(self, db_session, test_user, test_organization):
        """Should generate OTP and send email."""
        # Set email as verified
        test_user.email_verified_at = datetime.now(timezone.utc)
        db_session.commit()

        service = PasswordChangeService(db_session)
        service.request_password_change(test_user)

        # Verify OTP was generated
        db_session.refresh(test_user)
        assert test_user.password_change_otp is not None
        assert len(test_user.password_change_otp) == 6
        assert test_user.password_change_otp_expires_at is not None

    def test_request_password_change_email_not_verified_raises(self, db_session, test_user):
        """Should raise BadRequestError if email not verified."""
        test_user.email_verified_at = None
        db_session.commit()

        service = PasswordChangeService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.request_password_change(test_user)

        assert "Email must be verified" in str(exc_info.value.detail)


class TestChangePasswordWithOtp:
    """Tests for PasswordChangeService.change_password_with_otp method."""

    def test_change_password_with_otp_success(self, db_session, test_user):
        """Should change password after OTP verification."""
        # Set up OTP
        test_user.password_change_otp = "123456"
        test_user.password_change_otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        old_password_hash = test_user.password_hash
        db_session.commit()

        service = PasswordChangeService(db_session)
        service.change_password_with_otp(
            user=test_user,
            otp="123456",
            new_password="newpassword123",
        )

        # Verify password changed
        db_session.refresh(test_user)
        assert test_user.password_hash != old_password_hash
        assert test_user.password_change_otp is None
        assert test_user.password_change_otp_expires_at is None

    def test_change_password_with_otp_invalid_raises(self, db_session, test_user):
        """Should raise UnauthorizedError if OTP is invalid."""
        test_user.password_change_otp = "123456"
        test_user.password_change_otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        db_session.commit()

        service = PasswordChangeService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            service.change_password_with_otp(
                user=test_user,
                otp="000000",
                new_password="newpassword123",
            )

        assert "Invalid password change OTP" in str(exc_info.value.detail)

    def test_change_password_with_otp_expired_raises(self, db_session, test_user):
        """Should raise UnauthorizedError if OTP is expired."""
        test_user.password_change_otp = "123456"
        test_user.password_change_otp_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        db_session.commit()

        service = PasswordChangeService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            service.change_password_with_otp(
                user=test_user,
                otp="123456",
                new_password="newpassword123",
            )

        assert "expired" in str(exc_info.value.detail).lower()

    def test_change_password_with_otp_not_requested_raises(self, db_session, test_user):
        """Should raise UnauthorizedError if OTP was not requested."""
        test_user.password_change_otp = None
        db_session.commit()

        service = PasswordChangeService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            service.change_password_with_otp(
                user=test_user,
                otp="123456",
                new_password="newpassword123",
            )

        assert "not requested" in str(exc_info.value.detail).lower()
