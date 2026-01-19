"""Integration tests for invitation API endpoints."""

import pytest
from datetime import datetime, timedelta, timezone
from app.db.models.invitation import Invitation
from app.db.models.user import User, UserRole
from app.core.security import get_password_hash


class TestAcceptInvitation:
    """Tests for POST /api/v1/auth/invite/accept."""

    def test_accept_invitation_success(self, client, db_session, test_owner_user, test_organization):
        """Should accept invitation and create user account."""
        # Create invitation
        invitation = Invitation(
            email="newuser@example.com",
            organization_id=test_organization.id,
            role="operator",
            invited_by=test_owner_user.id,
            otp="123456",
            otp_expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            first_name="New",
            last_name="User",
        )
        db_session.add(invitation)
        db_session.commit()

        payload = {
            "email": "newuser@example.com",
            "otp": "123456",
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
        }

        response = client.post("/api/v1/auth/invite/accept", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["role"] == "operator"
        
        # Verify user was created
        user = db_session.query(User).filter(User.email == "newuser@example.com").first()
        assert user is not None
        assert user.organization_id == test_organization.id
        
        # Verify invitation was deleted
        invitation_check = db_session.query(Invitation).filter(
            Invitation.email == "newuser@example.com"
        ).first()
        assert invitation_check is None

    def test_accept_invitation_invalid_otp(self, client, db_session, test_owner_user, test_organization):
        """Should return 401 for invalid OTP."""
        # Create invitation
        invitation = Invitation(
            email="test@example.com",
            organization_id=test_organization.id,
            role="operator",
            invited_by=test_owner_user.id,
            otp="123456",
            otp_expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        db_session.add(invitation)
        db_session.commit()

        payload = {
            "email": "test@example.com",
            "otp": "000000",  # Wrong OTP
            "password": "password123",
        }

        response = client.post("/api/v1/auth/invite/accept", json=payload)

        assert response.status_code == 401

    def test_accept_invitation_expired_otp(self, client, db_session, test_owner_user, test_organization):
        """Should return 401 for expired OTP."""
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

        payload = {
            "email": "expired@example.com",
            "otp": "123456",
            "password": "password123",
        }

        response = client.post("/api/v1/auth/invite/accept", json=payload)

        assert response.status_code == 401


class TestCreateUserDirectly:
    """Tests for POST /api/v1/user/organizations/me/users/create."""

    def test_create_user_directly_success(self, client, auth_headers, test_owner_user, test_organization):
        """Should create user directly (Owner/Admin only)."""
        payload = {
            "email": "directuser@example.com",
            "role": "operator",
            "password": "password123",
            "first_name": "Direct",
            "last_name": "User",
        }

        # Need to use owner token
        from app.core.security import create_access_token
        owner_token = create_access_token({
            "sub": str(test_owner_user.id),
            "org": str(test_owner_user.organization_id),
            "role": test_owner_user.role.value,
        })
        owner_headers = {"Authorization": f"Bearer {owner_token}"}

        response = client.post(
            "/api/v1/user/organizations/me/users/create",
            json=payload,
            headers=owner_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "directuser@example.com"
        assert data["role"] == "operator"

    def test_create_user_directly_requires_owner_admin(self, client, auth_headers):
        """Should require Owner/Admin role."""
        payload = {
            "email": "test@example.com",
            "role": "operator",
            "password": "password123",
        }

        # Using operator token (not owner/admin)
        response = client.post(
            "/api/v1/user/organizations/me/users/create",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 403
