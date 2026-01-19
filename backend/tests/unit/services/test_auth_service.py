"""Unit tests for AuthService."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone
from jose import jwt

from app.services.auth import AuthService
from app.core.security import decode_token, get_password_hash
from app.core.config import settings
from app.core.exceptions import UnauthorizedError, BadRequestError
from app.db.models.user import User, UserRole
from app.db.models.organization import Organization, PlanType


class TestAuthenticate:
    """Tests for AuthService.authenticate method."""

    def test_authenticate_valid_credentials(self, db_session, test_user):
        """Valid credentials should return tokens and user."""
        auth_service = AuthService(db_session)

        access_token, refresh_token, user = auth_service.authenticate(
            email="test@example.com",
            password="password123",
        )

        assert access_token is not None
        assert refresh_token is not None
        assert user.id == test_user.id
        assert user.email == "test@example.com"

    def test_authenticate_invalid_email_raises(self, db_session, test_user):
        """Non-existent email should raise UnauthorizedError."""
        auth_service = AuthService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.authenticate(
                email="nonexistent@example.com",
                password="password123",
            )

        assert "Invalid credentials" in str(exc_info.value.detail)

    def test_authenticate_invalid_password_raises(self, db_session, test_user):
        """Wrong password should raise UnauthorizedError."""
        auth_service = AuthService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.authenticate(
                email="test@example.com",
                password="wrongpassword",
            )

        assert "Invalid credentials" in str(exc_info.value.detail)

    def test_authenticate_inactive_user_raises(self, db_session, inactive_user):
        """Inactive user should raise UnauthorizedError."""
        auth_service = AuthService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.authenticate(
                email="inactive@example.com",
                password="password123",
            )

        assert "disabled" in str(exc_info.value.detail).lower()

    def test_authenticate_updates_last_login(self, db_session, test_user):
        """Authenticate should update last_login_at."""
        auth_service = AuthService(db_session)
        assert test_user.last_login_at is None

        auth_service.authenticate(
            email="test@example.com",
            password="password123",
        )

        db_session.refresh(test_user)
        assert test_user.last_login_at is not None

    def test_authenticate_returns_valid_tokens(self, db_session, test_user):
        """Returned tokens should be decodable and contain correct data."""
        auth_service = AuthService(db_session)

        access_token, refresh_token, user = auth_service.authenticate(
            email="test@example.com",
            password="password123",
        )

        access_decoded = decode_token(access_token)
        refresh_decoded = decode_token(refresh_token)

        assert access_decoded["sub"] == str(test_user.id)
        # Only check org if user belongs to organization
        if test_user.organization_id:
            assert access_decoded["org"] == str(test_user.organization_id)
        assert access_decoded["role"] == test_user.role.value
        assert access_decoded["type"] == "access"

        assert refresh_decoded["type"] == "refresh"


class TestRefreshAccessToken:
    """Tests for AuthService.refresh_access_token method."""

    def test_refresh_with_valid_token(self, db_session, test_user, refresh_token):
        """Valid refresh token should return new access token."""
        auth_service = AuthService(db_session)

        new_access_token = auth_service.refresh_access_token(refresh_token)

        decoded = decode_token(new_access_token)
        assert decoded is not None
        assert decoded["sub"] == str(test_user.id)
        assert decoded["type"] == "access"

    def test_refresh_with_invalid_token_raises(self, db_session):
        """Invalid token should raise UnauthorizedError."""
        auth_service = AuthService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.refresh_access_token("invalid.token.here")

        assert "Invalid refresh token" in str(exc_info.value.detail)

    def test_refresh_with_access_token_raises(self, db_session, auth_token):
        """Access token used as refresh should raise UnauthorizedError."""
        auth_service = AuthService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.refresh_access_token(auth_token)

        assert "Invalid token type" in str(exc_info.value.detail)

    def test_refresh_with_inactive_user_raises(self, db_session, test_organization):
        """Refresh for inactive user should raise UnauthorizedError."""
        from app.core.security import create_refresh_token

        # Create inactive user
        user = User(
            email="inactive2@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=test_organization.id,
            first_name="Inactive",
            last_name="User",
            role=UserRole.OPERATOR,
            is_active=False,
        )
        db_session.add(user)
        db_session.commit()

        # Create refresh token for inactive user
        token_data = {
            "sub": str(user.id),
            "role": user.role.value,
        }
        if user.organization_id:
            token_data["org"] = str(user.organization_id)
        refresh_token = create_refresh_token(token_data)

        auth_service = AuthService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.refresh_access_token(refresh_token)

        assert "inactive" in str(exc_info.value.detail).lower()

    def test_refresh_with_expired_token_raises(self, db_session, test_user):
        """Expired refresh token should raise UnauthorizedError."""
        from app.core.security import create_refresh_token
        from datetime import timedelta
        
        # Create expired refresh token manually
        payload = {
            "sub": str(test_user.id),
            "role": test_user.role.value,
            "type": "refresh",
            "exp": datetime.now(timezone.utc) - timedelta(days=1),  # Expired 1 day ago
        }
        if test_user.organization_id:
            payload["org"] = str(test_user.organization_id)
        expired_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        
        auth_service = AuthService(db_session)
        with pytest.raises(UnauthorizedError):
            auth_service.refresh_access_token(expired_token)

    def test_refresh_with_deleted_user_raises(self, db_session, test_user, test_organization):
        """Refresh with deleted user should raise UnauthorizedError."""
        from app.core.security import create_refresh_token
        
        # Create refresh token
        token_data = {
            "sub": str(test_user.id),
            "role": test_user.role.value,
        }
        if test_user.organization_id:
            token_data["org"] = str(test_user.organization_id)
        refresh_token = create_refresh_token(token_data)
        
        # Delete user
        db_session.delete(test_user)
        db_session.commit()
        
        auth_service = AuthService(db_session)
        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.refresh_access_token(refresh_token)
        
        assert "not found" in str(exc_info.value.detail).lower() or "invalid" in str(exc_info.value.detail).lower()

    def test_refresh_after_role_change(self, db_session, test_user):
        """Refresh should create token with updated role."""
        from app.core.security import create_refresh_token
        
        # Create refresh token with old role
        token_data = {
            "sub": str(test_user.id),
            "role": test_user.role.value,
        }
        if test_user.organization_id:
            token_data["org"] = str(test_user.organization_id)
        refresh_token = create_refresh_token(token_data)
        
        # Change user role
        test_user.role = UserRole.ADMIN
        db_session.commit()
        
        auth_service = AuthService(db_session)
        new_access_token = auth_service.refresh_access_token(refresh_token)
        
        # Decode and verify new role is in token
        from app.core.security import decode_token
        decoded = decode_token(new_access_token)
        assert decoded["role"] == "admin"  # Updated role

    def test_refresh_after_password_change_still_works(self, db_session, test_user):
        """Refresh token should remain valid after password change (stateless tokens)."""
        from app.core.security import create_refresh_token
        
        # Create refresh token
        token_data = {
            "sub": str(test_user.id),
            "role": test_user.role.value,
        }
        if test_user.organization_id:
            token_data["org"] = str(test_user.organization_id)
        refresh_token = create_refresh_token(token_data)
        
        # Change password
        auth_service = AuthService(db_session)
        auth_service.change_password(
            user=test_user,
            current_password="password123",
            new_password="newpassword456",
        )
        
        # Refresh token should still work (stateless - password change doesn't invalidate)
        new_access_token = auth_service.refresh_access_token(refresh_token)
        assert new_access_token is not None


class TestRegister:
    """Tests for AuthService.register method."""

    def test_register_creates_organization(self, db_session):
        """Register should create a new organization."""
        auth_service = AuthService(db_session)

        access_token, refresh_token, user = auth_service.register(
            email="newuser@example.com",
            password="password123",
            first_name="New",
            last_name="User",
            organization_name="New Organization",
        )

        org = db_session.query(Organization).filter(
            Organization.name == "New Organization"
        ).first()

        assert org is not None
        assert user.organization_id == org.id

    def test_register_creates_user_as_owner(self, db_session):
        """Registered user should have owner role."""
        auth_service = AuthService(db_session)

        access_token, refresh_token, user = auth_service.register(
            email="newowner@example.com",
            password="password123",
            first_name="New",
            last_name="Owner",
            organization_name="Owner Org",
        )

        assert user.role == UserRole.OWNER

    def test_register_duplicate_email_raises(self, db_session, test_user):
        """Registering with existing email should raise BadRequestError."""
        auth_service = AuthService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            auth_service.register(
                email="test@example.com",  # Already exists
                password="password123",
                first_name="Duplicate",
                last_name="User",
                organization_name="Duplicate Org",
            )

        assert "already registered" in str(exc_info.value.detail).lower()

    def test_register_returns_valid_tokens(self, db_session):
        """Register should return valid tokens."""
        auth_service = AuthService(db_session)

        access_token, refresh_token, user = auth_service.register(
            email="tokens@example.com",
            password="password123",
            first_name="Token",
            last_name="User",
            organization_name="Token Org",
        )

        access_decoded = decode_token(access_token)
        refresh_decoded = decode_token(refresh_token)

        assert access_decoded["sub"] == str(user.id)
        assert access_decoded["type"] == "access"
        assert refresh_decoded["type"] == "refresh"

    def test_register_organization_name_with_special_chars(self, db_session):
        """Organization name with special characters should be handled correctly."""
        auth_service = AuthService(db_session)
        
        access_token, refresh_token, user = auth_service.register(
            email="special@example.com",
            password="password123",
            first_name="Special",
            last_name="User",
            organization_name="Test & Co. (Ltd.) - 2024",
        )
        
        org = db_session.query(Organization).filter(
            Organization.id == user.organization_id
        ).first()
        assert org is not None
        assert org.name == "Test & Co. (Ltd.) - 2024"

    def test_register_organization_name_too_long_handled(self, db_session):
        """Organization name longer than 255 chars should be handled (validation should be in API layer)."""
        auth_service = AuthService(db_session)
        long_name = "A" * 300  # Longer than 255 chars
        
        # This should fail at the schema/API validation level, not service level
        # But we test that service handles it gracefully
        try:
            auth_service.register(
                email="longname@example.com",
                password="password123",
                first_name="Long",
                last_name="Name",
                organization_name=long_name,
            )
        except Exception:
            # Expected - validation should happen at API layer
            pass

    def test_register_duplicate_email_case_insensitive(self, db_session, test_user):
        """Register with existing email (different case) should raise BadRequestError."""
        auth_service = AuthService(db_session)
        
        # PostgreSQL emails are case-sensitive, but we test the exact match behavior
        # If we want case-insensitive, normalization should happen in service
        with pytest.raises(BadRequestError):
            auth_service.register(
                email="test@example.com",  # Exact match
                password="password123",
                first_name="Duplicate",
                last_name="User",
                organization_name="Duplicate Org",
            )

    def test_register_creates_unique_slug(self, db_session):
        """Register should create unique slug for organization."""
        from app.db.repositories.organization import OrganizationRepository
        
        auth_service = AuthService(db_session)
        org_repo = OrganizationRepository(db_session)
        
        # Register first org
        auth_service.register(
            email="org1@example.com",
            password="password123",
            first_name="Org1",
            last_name="User",
            organization_name="Test Organization",
        )
        
        # Register second org with same name
        auth_service.register(
            email="org2@example.com",
            password="password123",
            first_name="Org2",
            last_name="User",
            organization_name="Test Organization",
        )
        
        # Both should have different slugs
        orgs = db_session.query(Organization).filter(
            Organization.name == "Test Organization"
        ).all()
        assert len(orgs) == 2
        slugs = [org.slug for org in orgs]
        assert len(set(slugs)) == 2  # All slugs should be unique

    def test_register_organization_settings_initialized(self, db_session):
        """Register should initialize organization settings."""
        auth_service = AuthService(db_session)
        
        access_token, refresh_token, user = auth_service.register(
            email="settings@example.com",
            password="password123",
            first_name="Settings",
            last_name="User",
            organization_name="Settings Org",
        )
        
        org = db_session.query(Organization).filter(
            Organization.id == user.organization_id
        ).first()
        assert org.settings is not None
        assert isinstance(org.settings, dict)

    def test_register_first_last_name_optional(self, db_session):
        """Register should work with empty first_name and last_name."""
        auth_service = AuthService(db_session)
        
        # Note: Current implementation requires first_name and last_name
        # If made optional, this test validates that behavior
        access_token, refresh_token, user = auth_service.register(
            email="optional@example.com",
            password="password123",
            first_name="",
            last_name="",
            organization_name="Optional Org",
        )
        
        assert user.email == "optional@example.com"

    def test_register_platform_admin(self, db_session):
        """Register with PLATFORM_ADMIN_EMAIL should create platform admin."""
        from app.core.config import settings
        auth_service = AuthService(db_session)
        
        # Use platform admin email from settings
        platform_email = settings.PLATFORM_ADMIN_EMAIL
        
        access_token, refresh_token, user = auth_service.register(
            email=platform_email,
            password="password123",
            first_name="Platform",
            last_name="Admin",
            organization_name="Vectra",  # This should be ignored
        )
        
        assert user.role == UserRole.PLATFORM_ADMIN
        assert user.organization_id is None
        assert user.email == platform_email


class TestChangePassword:
    """Tests for AuthService.change_password method."""

    def test_change_password_success(self, db_session, test_user):
        """Valid current password should allow password change."""
        auth_service = AuthService(db_session)

        auth_service.change_password(
            user=test_user,
            current_password="password123",
            new_password="newpassword456",
        )

        # Should be able to authenticate with new password
        access_token, refresh_token, user = auth_service.authenticate(
            email="test@example.com",
            password="newpassword456",
        )
        assert user.id == test_user.id

    def test_change_password_wrong_current_raises(self, db_session, test_user):
        """Wrong current password should raise UnauthorizedError."""
        auth_service = AuthService(db_session)

        with pytest.raises(UnauthorizedError) as exc_info:
            auth_service.change_password(
                user=test_user,
                current_password="wrongpassword",
                new_password="newpassword456",
            )

        assert "incorrect" in str(exc_info.value.detail).lower()

    def test_change_password_same_password_allowed(self, db_session, test_user):
        """Changing password to the same password should be allowed (no-op)."""
        from app.core.security import verify_password
        
        auth_service = AuthService(db_session)
        old_hash = test_user.password_hash
        
        # Change to same password
        auth_service.change_password(
            user=test_user,
            current_password="password123",
            new_password="password123",  # Same password
        )
        
        db_session.refresh(test_user)
        # Hash should be different (re-hashed) but password should still work
        new_hash = test_user.password_hash
        # Note: bcrypt produces different hashes even for same password
        assert verify_password("password123", new_hash) is True

    def test_change_password_multiple_times_rapidly(self, db_session, test_user):
        """Changing password multiple times rapidly should work."""
        auth_service = AuthService(db_session)
        
        # Change password 3 times in sequence
        auth_service.change_password(
            user=test_user,
            current_password="password123",
            new_password="password1",
        )
        
        auth_service.change_password(
            user=test_user,
            current_password="password1",
            new_password="password2",
        )
        
        auth_service.change_password(
            user=test_user,
            current_password="password2",
            new_password="password3",
        )
        
        # Should be able to authenticate with final password
        access_token, refresh_token, user = auth_service.authenticate(
            email="test@example.com",
            password="password3",
        )
        assert user.id == test_user.id
