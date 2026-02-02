"""Integration tests for password change API endpoints."""

import pytest
from datetime import datetime, timezone
from app.db.models.user import User


class TestRequestPasswordChange:
    """Tests for POST /api/v1/auth/change-password/request."""

    def test_request_password_change_success(self, client, auth_headers, db_session, test_user):
        """Should send OTP email."""
        # Set email as verified
        test_user.email_verified_at = datetime.now(timezone.utc)
        db_session.commit()

        response = client.post("/api/v1/auth/change-password/request", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "OTP sent" in data["message"]

    def test_request_password_change_email_not_verified(self, client, auth_headers, db_session, test_user):
        """Should return 400 if email not verified."""
        test_user.email_verified_at = None
        db_session.commit()

        response = client.post("/api/v1/auth/change-password/request", headers=auth_headers)

        assert response.status_code == 400

    def test_request_password_change_requires_auth(self, client):
        """Should require authentication."""
        response = client.post("/api/v1/auth/change-password/request")

        assert response.status_code == 401


class TestChangePasswordWithOtp:
    """Tests for POST /api/v1/auth/change-password/verify."""

    def test_change_password_with_otp_success(self, client, auth_headers, db_session, test_user):
        """Should change password after OTP verification."""
        from datetime import timedelta
        
        # Set up OTP
        test_user.password_change_otp = "123456"
        test_user.password_change_otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        db_session.commit()

        payload = {
            "otp": "123456",
            "new_password": "newpassword123"
        }

        response = client.post("/api/v1/auth/change-password/verify", json=payload, headers=auth_headers)

        assert response.status_code == 204

    def test_change_password_with_otp_invalid(self, client, auth_headers, db_session, test_user):
        """Should return 401 if OTP is invalid."""
        from datetime import timedelta
        
        test_user.password_change_otp = "123456"
        test_user.password_change_otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        db_session.commit()

        payload = {
            "otp": "000000",
            "new_password": "newpassword123"
        }

        response = client.post("/api/v1/auth/change-password/verify", json=payload, headers=auth_headers)

        assert response.status_code == 401

    def test_change_password_with_otp_requires_auth(self, client):
        """Should require authentication."""
        payload = {
            "otp": "123456",
            "new_password": "newpassword123"
        }

        response = client.post("/api/v1/auth/change-password/verify", json=payload)

        assert response.status_code == 401
