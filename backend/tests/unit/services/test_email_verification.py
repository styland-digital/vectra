"""Unit tests for email verification service."""

import pytest
from unittest.mock import patch
from datetime import datetime, timezone
from uuid import uuid4

from app.services.email_verification import EmailVerificationService
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.db.models.user import User, UserRole
from app.db.models.organization import Organization, PlanType


@pytest.fixture
def verification_service(db_session):
    """Create email verification service."""
    return EmailVerificationService(db_session)


@pytest.fixture
def unverified_user(db_session):
    """Create an unverified user."""
    org = Organization(
        id=uuid4(),
        name="Test Org",
        slug="test-org",
        plan=PlanType.TRIAL.value,
        settings={},
    )
    db_session.add(org)
    db_session.commit()

    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        organization_id=org.id,
        first_name="Test",
        last_name="User",
        role=UserRole.OWNER,
        email_verified_at=None,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def verified_user(db_session, unverified_user):
    """Create a verified user."""
    unverified_user.email_verified_at = datetime.now(timezone.utc)
    db_session.commit()
    db_session.refresh(unverified_user)
    return unverified_user


class TestGenerateVerificationOtp:
    """Test verification OTP generation."""

    def test_generate_otp_for_unverified_user(self, verification_service, unverified_user):
        """Should generate OTP for unverified user."""
        otp = verification_service.generate_verification_otp(unverified_user)
        assert otp is not None
        assert isinstance(otp, str)
        assert len(otp) == 6
        assert otp.isdigit()

    def test_generate_otp_fails_for_verified_user(self, verification_service, verified_user):
        """Should raise error if user is already verified."""
        with pytest.raises(BadRequestError, match="already verified"):
            verification_service.generate_verification_otp(verified_user)

    def test_generate_otp_invalidates_old_otp(self, verification_service, unverified_user):
        """Should invalidate old OTP when new one is generated."""
        # Generate first OTP
        first_otp = verification_service.generate_verification_otp(unverified_user)
        assert unverified_user.email_verification_otp == first_otp

        # Generate second OTP
        second_otp = verification_service.generate_verification_otp(unverified_user)
        assert second_otp != first_otp
        assert unverified_user.email_verification_otp == second_otp

        # Old OTP should be invalid
        with pytest.raises(UnauthorizedError, match="Invalid OTP"):
            verification_service.verify_email_with_otp(unverified_user.email, first_otp)

        # New OTP should work
        verified_user = verification_service.verify_email_with_otp(unverified_user.email, second_otp)
        assert verified_user.email_verified_at is not None


class TestVerifyEmailWithOtp:
    """Test email verification with OTP."""

    def test_verify_email_with_valid_otp(self, verification_service, unverified_user):
        """Should verify email with valid OTP."""
        otp = verification_service.generate_verification_otp(unverified_user)
        
        # Verify email
        verified_user = verification_service.verify_email_with_otp(unverified_user.email, otp)
        
        assert verified_user.email_verified_at is not None
        assert verified_user.id == unverified_user.id

    def test_verify_email_with_invalid_otp(self, verification_service, unverified_user):
        """Should raise error for invalid OTP."""
        verification_service.generate_verification_otp(unverified_user)
        with pytest.raises(UnauthorizedError, match="Invalid OTP"):
            verification_service.verify_email_with_otp(unverified_user.email, "000000")

    def test_verify_email_with_nonexistent_email(self, verification_service):
        """Should raise error if email doesn't exist."""
        with pytest.raises(UnauthorizedError, match="Invalid OTP"):
            verification_service.verify_email_with_otp("nonexistent@example.com", "123456")

    def test_verify_email_already_verified(self, verification_service, verified_user):
        """Should raise error if email is already verified."""
        # Try to generate OTP for already verified user
        with pytest.raises(BadRequestError, match="already verified"):
            verification_service.generate_verification_otp(verified_user)

    def test_verify_email_with_expired_otp(self, verification_service, unverified_user, db_session):
        """Should raise error for expired OTP."""
        from datetime import timedelta
        otp = verification_service.generate_verification_otp(unverified_user)
        
        # Manually expire OTP
        unverified_user.email_verification_otp_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        db_session.commit()
        
        with pytest.raises(UnauthorizedError, match="expired"):
            verification_service.verify_email_with_otp(unverified_user.email, otp)


class TestSendVerificationEmail:
    """Test sending verification emails."""

    @patch('app.services.resend.send_verification_email')
    def test_send_email_for_unverified_user(self, mock_send, verification_service, unverified_user):
        """Should send email for unverified user."""
        mock_send.return_value = None
        # Should not raise
        verification_service.send_verification_email(unverified_user.email)

    def test_send_email_for_verified_user(self, verification_service, verified_user):
        """Should raise error if email is already verified."""
        with pytest.raises(BadRequestError, match="already verified"):
            verification_service.send_verification_email(verified_user.email)

    @patch('app.services.resend.send_verification_email')
    def test_send_email_for_nonexistent_email(self, mock_send, verification_service):
        """Should not raise for nonexistent email (security)."""
        mock_send.return_value = None
        # Should not raise - don't reveal if email exists
        verification_service.send_verification_email("nonexistent@example.com")


class TestResendVerificationEmail:
    """Test resending verification emails."""

    @patch('app.services.resend.send_verification_email')
    def test_resend_email_for_unverified_user(self, mock_send, verification_service, unverified_user):
        """Should resend email for unverified user."""
        mock_send.return_value = None
        # Should not raise
        verification_service.resend_verification_email(unverified_user)

    def test_resend_email_for_verified_user(self, verification_service, verified_user):
        """Should raise error if email is already verified."""
        with pytest.raises(BadRequestError, match="already verified"):
            verification_service.resend_verification_email(verified_user)
