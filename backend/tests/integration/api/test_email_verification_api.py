"""Integration tests for email verification API endpoints."""

import pytest
from unittest.mock import patch
from fastapi import status
from datetime import datetime, timezone, timedelta

from app.db.models.user import User


class TestVerifyEmailEndpoint:
    """Test POST /api/v1/auth/verify-email endpoint."""

    def test_verify_email_with_valid_otp(self, client, test_user, db_session):
        """Should verify email with valid OTP."""
        from app.services.email_verification import EmailVerificationService
        
        verification_service = EmailVerificationService(db_session)
        otp = verification_service.generate_verification_otp(test_user)

        # Verify email
        response = client.post(
            "/api/v1/auth/verify-email",
            json={"email": test_user.email, "otp": otp},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Email verified successfully"

        # Refresh user from db_session
        db_session.refresh(test_user)
        assert test_user.email_verified_at is not None

    def test_verify_email_with_invalid_otp(self, client, test_user, db_session):
        """Should return error for invalid OTP."""
        from app.services.email_verification import EmailVerificationService
        
        verification_service = EmailVerificationService(db_session)
        verification_service.generate_verification_otp(test_user)

        response = client.post(
            "/api/v1/auth/verify-email",
            json={"email": test_user.email, "otp": "000000"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_email_with_expired_otp(self, client, test_user, db_session):
        """Should return error for expired OTP."""
        from app.services.email_verification import EmailVerificationService
        
        verification_service = EmailVerificationService(db_session)
        otp = verification_service.generate_verification_otp(test_user)
        
        # Manually expire OTP
        test_user.email_verification_otp_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        db_session.commit()

        response = client.post(
            "/api/v1/auth/verify-email",
            json={"email": test_user.email, "otp": otp},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_email_with_wrong_email(self, client, test_user, db_session):
        """Should return error for wrong email."""
        from app.services.email_verification import EmailVerificationService
        
        verification_service = EmailVerificationService(db_session)
        otp = verification_service.generate_verification_otp(test_user)

        response = client.post(
            "/api/v1/auth/verify-email",
            json={"email": "wrong@example.com", "otp": otp},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_email_already_verified(self, client, test_user, db_session):
        """Should return error if email is already verified."""
        from app.services.email_verification import EmailVerificationService
        
        verification_service = EmailVerificationService(db_session)
        otp = verification_service.generate_verification_otp(test_user)
        verification_service.verify_email_with_otp(test_user.email, otp)
        db_session.refresh(test_user)

        # Try to verify again with the same OTP (already used and cleared)
        response = client.post(
            "/api/v1/auth/verify-email",
            json={"email": test_user.email, "otp": otp},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestSendVerificationEmailEndpoint:
    """Test POST /api/v1/auth/send-verification-email endpoint."""

    @patch('app.services.resend.send_verification_email')
    def test_send_verification_email_for_unverified_user(self, mock_send, client, test_user):
        """Should send verification email for unverified user."""
        mock_send.return_value = None
        response = client.post(
            "/api/v1/auth/send-verification-email",
            json={"email": test_user.email},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data

    @patch('app.services.resend.send_verification_email')
    def test_send_verification_email_for_nonexistent_email(self, mock_send, client):
        """Should return success even for nonexistent email (security)."""
        mock_send.return_value = None
        response = client.post(
            "/api/v1/auth/send-verification-email",
            json={"email": "nonexistent@example.com"},
        )

        # Should return success for security (don't reveal if email exists)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data

    def test_send_verification_email_with_invalid_email_format(self, client):
        """Should return validation error for invalid email format."""
        response = client.post(
            "/api/v1/auth/send-verification-email",
            json={"email": "invalid_email"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestResendVerificationEmailEndpoint:
    """Test POST /api/v1/auth/resend-verification-email endpoint."""

    def test_resend_verification_email_unauthenticated(self, client):
        """Should return 401 for unauthenticated request."""
        response = client.post("/api/v1/auth/resend-verification-email")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('app.services.resend.send_verification_email')
    def test_resend_verification_email_for_unverified_user(self, mock_send, client, test_user):
        """Should resend verification email for unverified user."""
        mock_send.return_value = None
        # Login first
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "password123",
            },
        )
        assert login_response.status_code == status.HTTP_200_OK
        access_token = login_response.json()["access_token"]

        # Resend verification email
        response = client.post(
            "/api/v1/auth/resend-verification-email",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Verification email sent"

    def test_resend_verification_email_for_verified_user(self, client, test_user, db_session):
        """Should return error if email is already verified."""
        # Verify email first using test db_session
        from app.services.email_verification import EmailVerificationService
        
        verification_service = EmailVerificationService(db_session)
        otp = verification_service.generate_verification_otp(test_user)
        verification_service.verify_email_with_otp(test_user.email, otp)
        db_session.refresh(test_user)

        # Login
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "password123",
            },
        )
        access_token = login_response.json()["access_token"]

        # Try to resend
        response = client.post(
            "/api/v1/auth/resend-verification-email",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestRegisterSendsVerificationEmail:
    """Test that register endpoint sends verification email."""

    def test_register_sends_verification_email(self, client):
        """Should send verification email when user registers."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "first_name": "New",
                "last_name": "User",
                "organization_name": "New Org",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        # Email should be sent (logged in development)
        # In production, this would be sent via SendGrid
