"""End-to-end tests for complete authentication flows."""

import pytest
from datetime import timedelta
from fastapi.testclient import TestClient

from app.core.security import create_access_token, decode_token
from app.db.models.user import UserRole


class TestCompleteAuthFlow:
    """End-to-end tests for complete authentication scenarios."""

    def test_register_login_refresh_logout_flow(self, client, db_session):
        """Test complete flow: register -> login -> refresh -> logout."""
        # 1. Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "flow1@example.com",
                "password": "password123",
                "first_name": "Flow",
                "last_name": "One",
                "organization_name": "Flow Org 1",
            },
        )
        assert register_response.status_code == 201
        register_data = register_response.json()
        assert "access_token" in register_data
        assert "refresh_token" in register_data
        initial_access_token = register_data["access_token"]
        refresh_token = register_data["refresh_token"]
        
        # 2. Access protected endpoint with initial token
        me_response1 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {initial_access_token}"},
        )
        assert me_response1.status_code == 200
        assert me_response1.json()["email"] == "flow1@example.com"
        
        # 3. Refresh token
        import time
        time.sleep(1.1)  # Ensure different expiration time
        
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_response.status_code == 200
        refresh_data = refresh_response.json()
        new_access_token = refresh_data["access_token"]
        assert new_access_token != initial_access_token  # Should be different
        
        # 4. Use new access token
        me_response2 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {new_access_token}"},
        )
        assert me_response2.status_code == 200
        assert me_response2.json()["email"] == "flow1@example.com"
        
        # 5. Logout
        logout_response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {new_access_token}"},
        )
        assert logout_response.status_code == 204
        
        # 6. After logout, token should still work (stateless - client discards)
        # In stateless auth, logout is client-side, so token remains valid
        # This is expected behavior for stateless JWT
        me_response3 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {new_access_token}"},
        )
        # Token should still work (stateless auth)
        assert me_response3.status_code == 200

    def test_login_change_password_relogin_flow(self, client, test_user):
        """Test login -> change password -> re-login with new password."""
        # 1. Login
        login_response1 = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        assert login_response1.status_code == 200
        access_token = login_response1.json()["access_token"]
        
        # 2. Change password
        change_response = client.post(
            "/api/v1/auth/change-password",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "current_password": "password123",
                "new_password": "newpassword456",
            },
        )
        assert change_response.status_code == 204
        
        # 3. Login with new password
        login_response2 = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "newpassword456",
            },
        )
        assert login_response2.status_code == 200
        new_access_token = login_response2.json()["access_token"]
        assert new_access_token is not None
        
        # 4. Old password should not work
        login_response3 = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",  # Old password
            },
        )
        assert login_response3.status_code == 401

    def test_login_token_expire_refresh_continuation_flow(self, client, test_user):
        """Test login -> token expires -> refresh -> continue using new token."""
        # 1. Login
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        assert login_response.status_code == 200
        tokens = login_response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        
        # 2. Use access token
        me_response1 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_response1.status_code == 200
        
        # 3. Simulate token expiration (create expired token)
        expired_token = create_access_token(
            {"sub": str(test_user.id), "org": str(test_user.organization_id), "role": test_user.role.value},
            expires_delta=timedelta(hours=-1)
        )
        
        # 4. Expired token should fail
        me_response2 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert me_response2.status_code == 401
        
        # 5. Refresh token to get new access token
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_response.status_code == 200
        new_tokens = refresh_response.json()
        new_access_token = new_tokens["access_token"]
        
        # 6. Use new access token
        me_response3 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {new_access_token}"},
        )
        assert me_response3.status_code == 200
        assert me_response3.json()["email"] == "test@example.com"

    def test_user_deactivated_during_session_flow(self, client, db_session, test_user):
        """Test user deactivated during active session."""
        # 1. Login
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]
        
        # 2. Access protected endpoint
        me_response1 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_response1.status_code == 200
        
        # 3. Deactivate user (simulating admin action)
        test_user.is_active = False
        db_session.commit()
        
        # 4. Token should now fail (user is inactive)
        me_response2 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_response2.status_code == 401
        assert "disabled" in me_response2.json()["detail"].lower()
        
        # 5. Refresh token should also fail (user is inactive)
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_response.status_code == 401
        
        # 6. Login should fail (user is inactive)
        login_response2 = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        assert login_response2.status_code == 401
        assert "disabled" in login_response2.json()["detail"].lower()

    def test_multiple_refresh_flow(self, client, test_user, refresh_token):
        """Test multiple refresh calls with same refresh token (idempotency)."""
        import time
        
        # 1. First refresh
        refresh_response1 = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_response1.status_code == 200
        token1 = refresh_response1.json()["access_token"]
        
        # Small delay to ensure different expiration times
        time.sleep(1.1)  # Wait slightly more than 1 second to ensure different exp
        
        # 2. Second refresh with same refresh token
        refresh_response2 = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_response2.status_code == 200
        token2 = refresh_response2.json()["access_token"]
        
        # 3. Both access tokens should work (different tokens each time)
        assert token1 != token2  # New token each time
        
        me_response1 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert me_response1.status_code == 200
        
        me_response2 = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert me_response2.status_code == 200

    def test_concurrent_authentication_flow(self, client, db_session, test_user):
        """Test multiple sequential authentication requests (simulating concurrent usage)."""
        # Note: Using sequential requests instead of true concurrency
        # because SQLAlchemy sessions are not thread-safe.
        # This still validates that multiple login requests work correctly.
        
        def login_request():
            return client.post(
                "/api/v1/auth/login",
                data={
                    "username": "test@example.com",
                    "password": "password123",
                },
            )
        
        # Make multiple sequential login requests (simulating concurrent usage)
        results = [login_request() for _ in range(5)]
        
        # All should succeed
        for response in results:
            assert response.status_code == 200
            assert "access_token" in response.json()
            assert "refresh_token" in response.json()

    def test_register_multiple_users_same_organization_not_allowed(self, client, db_session):
        """Test that register always creates new organization (users can't join existing)."""
        # 1. Register first user
        register_response1 = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user1@example.com",
                "password": "password123",
                "first_name": "User",
                "last_name": "1",
                "organization_name": "Same Org Name",
            },
        )
        assert register_response1.status_code == 201
        org1_id = register_response1.json()["user"]["organization"]["id"]
        
        # 2. Register second user with same org name (should create new org)
        register_response2 = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user2@example.com",
                "password": "password123",
                "first_name": "User",
                "last_name": "2",
                "organization_name": "Same Org Name",  # Same name
            },
        )
        assert register_response2.status_code == 201
        org2_id = register_response2.json()["user"]["organization"]["id"]
        
        # 3. Should be different organizations (register creates new org each time)
        assert org1_id != org2_id
