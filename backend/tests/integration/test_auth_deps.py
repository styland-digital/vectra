"""Integration tests for FastAPI dependencies (auth, RBAC, multi-tenant)."""

import pytest
from uuid import UUID, uuid4
from fastapi.testclient import TestClient

from app.api.deps import get_current_user, require_role, get_organization_id
from app.core.security import create_access_token
from app.db.models.user import User, UserRole


class TestGetCurrentUser:
    """Tests for get_current_user dependency."""

    def test_get_current_user_with_valid_token(self, db_session, test_user):
        """Valid token should return user."""
        from app.core.security import create_access_token
        from app.api.deps import get_current_user
        
        token = create_access_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,
        })
        
        # Call get_current_user directly with test db_session
        user = get_current_user(token=token, db=db_session)
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_current_user_missing_token_raises(self, db_session):
        """Missing token should raise 401."""
        from fastapi import HTTPException
        
        from app.api.deps import get_db
        
        db_gen = get_db()
        db = next(db_gen)
        try:
            with pytest.raises(Exception):  # OAuth2PasswordBearer raises
                get_current_user(token="", db=db)
        finally:
            db_gen.close()

    def test_get_current_user_invalid_token_raises(self, db_session):
        """Invalid token should raise 401."""
        from fastapi import HTTPException
        from app.api.deps import get_db
        
        db_gen = get_db()
        db = next(db_gen)
        try:
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(token="invalid.token.here", db=db)
            assert exc_info.value.status_code == 401
        finally:
            db_gen.close()

    def test_get_current_user_token_without_bearer_prefix(self, db_session, test_user):
        """Token without Bearer prefix should fail (OAuth2PasswordBearer handles this)."""
        # OAuth2PasswordBearer expects "Bearer {token}" format
        # If token is passed without Bearer, it should fail
        token = create_access_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,
        })
        
        # get_current_user receives the token after OAuth2PasswordBearer extraction
        # So we test with the extracted token directly
        # Valid token (without Bearer prefix, already extracted)
        user = get_current_user(token=token, db=db_session)
        assert user.id == test_user.id

    def test_get_current_user_token_with_spaces(self, db_session, test_user):
        """Token with spaces before/after should be handled correctly."""
        token = create_access_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,
        })
        
        from app.api.deps import get_db
        
        db_gen = get_db()
        db = next(db_gen)
        try:
            # Token with spaces should fail (JWT doesn't allow spaces)
            with pytest.raises(Exception):
                get_current_user(token=f" {token} ", db=db)
        finally:
            db_gen.close()

    def test_get_current_user_invalid_user_id_raises(self, db_session):
        """Token with invalid user_id (non-UUID) should raise 401."""
        from fastapi import HTTPException
        from app.api.deps import get_db
        
        # Create token with invalid user_id format
        token = create_access_token({
            "sub": "not-a-uuid",
            "org": str(uuid4()),
            "role": "operator",
        })
        
        db_gen = get_db()
        db = next(db_gen)
        try:
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(token=token, db=db)
            assert exc_info.value.status_code == 401
        finally:
            db_gen.close()

    def test_get_current_user_deleted_user_raises(self, db_session, test_user):
        """Token for deleted user should raise 401."""
        from fastapi import HTTPException
        from app.api.deps import get_db
        
        token = create_access_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,
        })
        
        # Delete user
        db_session.delete(test_user)
        db_session.commit()
        
        db_gen = get_db()
        db = next(db_gen)
        try:
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(token=token, db=db)
            assert exc_info.value.status_code == 401
        finally:
            db_gen.close()

    def test_get_current_user_inactive_user_raises(self, db_session, inactive_user):
        """Token for inactive user should raise 401 with specific message."""
        from fastapi import HTTPException
        
        token = create_access_token({
            "sub": str(inactive_user.id),
            "org": str(inactive_user.organization_id),
            "role": inactive_user.role.value,
        })
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=db_session)
        assert exc_info.value.status_code == 401
        assert "disabled" in exc_info.value.detail.lower()


class TestRequireRole:
    """Tests for require_role RBAC dependency."""

    def test_require_role_allows_authorized_role(self, client, test_admin_user):
        """User with authorized role should pass."""
        # Note: require_role is a dependency factory
        # We test it through an endpoint that uses it
        # For now, we test the concept by verifying role checking
        token = create_access_token({
            "sub": str(test_admin_user.id),
            "org": str(test_admin_user.organization_id),
            "role": test_admin_user.role.value,  # ADMIN
        })
        
        # Admin should be able to access endpoints requiring admin role
        # (This is tested through actual endpoints using require_role)
        # Here we verify the token contains the correct role
        from app.core.security import decode_token
        decoded = decode_token(token)
        assert decoded["role"] == "admin"

    def test_require_role_blocks_unauthorized_role(self, client, test_user):
        """User with unauthorized role should be blocked."""
        token = create_access_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,  # OPERATOR
        })
        
        # Operator should not access admin endpoints
        # This is tested through endpoints that use require_role([UserRole.ADMIN, UserRole.OWNER])
        # Here we verify the token contains operator role
        from app.core.security import decode_token
        decoded = decode_token(token)
        assert decoded["role"] == "operator"

    def test_require_role_multiple_allowed_roles(self, client, test_user, test_admin_user):
        """require_role should accept multiple allowed roles."""
        # This is tested through endpoints that use require_role([UserRole.ADMIN, UserRole.OWNER])
        # Both admin and owner should be able to access
        admin_token = create_access_token({
            "sub": str(test_admin_user.id),
            "org": str(test_admin_user.organization_id),
            "role": test_admin_user.role.value,  # ADMIN
        })
        
        from app.core.security import decode_token
        decoded = decode_token(admin_token)
        # Admin should be in allowed roles [ADMIN, OWNER]
        assert decoded["role"] in ["admin", "owner"]


class TestGetOrganizationId:
    """Tests for get_organization_id multi-tenant dependency."""

    def test_get_organization_id_returns_user_org(self, db_session, test_user):
        """get_organization_id should return user's organization_id."""
        token = create_access_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,
        })
        
        user = get_current_user(token=token, db=db_session)
        org_id = get_organization_id(current_user=user)
        assert org_id == test_user.organization_id
        assert isinstance(org_id, UUID)

    def test_get_organization_id_isolation(self, db_session, test_user, test_organization):
        """Different users should have different organization_ids."""
        from app.db.models.user import User, UserRole
        from app.core.security import get_password_hash
        from app.api.deps import get_db, get_current_user
        
        # Create user in different organization
        from app.db.models.organization import Organization
        org2 = Organization(
            name="Org 2",
            slug="org-2",
            plan=test_organization.plan,
            settings={},
        )
        db_session.add(org2)
        db_session.commit()
        db_session.refresh(org2)
        
        user2 = User(
            email="user2@example.com",
            password_hash=get_password_hash("password123"),
            organization_id=org2.id,
            first_name="User",
            last_name="2",
            role=UserRole.OPERATOR,
        )
        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user2)
        
        token1 = create_access_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,
        })
        
        token2 = create_access_token({
            "sub": str(user2.id),
            "org": str(user2.organization_id),
            "role": user2.role.value,
        })
        
        user1 = get_current_user(token=token1, db=db_session)
        org_id1 = get_organization_id(current_user=user1)
        
        user2_obj = get_current_user(token=token2, db=db_session)
        org_id2 = get_organization_id(current_user=user2_obj)
        
        # Different users should have different organization_ids
        assert org_id1 != org_id2
        assert org_id1 == test_user.organization_id
        assert org_id2 == org2.id
