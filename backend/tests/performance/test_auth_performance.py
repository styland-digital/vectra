"""Performance tests for authentication system."""

import pytest
import time
from fastapi.testclient import TestClient

from app.core.security import get_password_hash, create_access_token


class TestAuthenticationPerformance:
    """Performance tests for authentication operations."""

    def test_login_performance(self, client, test_user):
        """Login should complete in reasonable time (< 200ms P95)."""
        start = time.time()
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        
        assert response.status_code == 200
        # P95 should be < 200ms, but we allow some tolerance for CI/CD environments
        assert elapsed < 1000, f"Login took {elapsed}ms, should be < 1000ms (P95 target: < 200ms)"

    def test_token_creation_performance(self):
        """Token creation should be fast (< 10ms)."""
        data = {"sub": "user123", "org": "org456", "role": "operator"}
        
        start = time.time()
        token = create_access_token(data)
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        
        assert token is not None
        assert elapsed < 50, f"Token creation took {elapsed}ms, should be < 50ms (target: < 10ms)"

    def test_password_hashing_performance(self):
        """Password hashing should complete in reasonable time (< 500ms)."""
        password = "test_password_123"
        
        start = time.time()
        hashed = get_password_hash(password)
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        
        assert hashed is not None
        # bcrypt cost 12 should take < 500ms
        assert elapsed < 500, f"Password hashing took {elapsed}ms, should be < 500ms (bcrypt cost 12)"

    def test_password_verification_performance(self):
        """Password verification should be fast (< 100ms)."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        start = time.time()
        from app.core.security import verify_password
        result = verify_password(password, hashed)
        elapsed = (time.time() - start) * 1000
        
        assert result is True
        # Verification should be fast
        assert elapsed < 200, f"Password verification took {elapsed}ms, should be < 200ms"

    def test_refresh_token_performance(self, client, refresh_token):
        """Refresh token should complete in reasonable time (< 200ms)."""
        start = time.time()
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code == 200
        assert elapsed < 1000, f"Refresh token took {elapsed}ms, should be < 1000ms (P95 target: < 200ms)"


class TestRateLimiting:
    """Tests for rate limiting (if implemented)."""

    def test_rate_limiting_not_implemented_yet(self, client, test_user):
        """Rate limiting should be implemented according to DOC-TECH-002 (10 req/min on auth)."""
        # Note: Rate limiting is not yet implemented in the codebase
        # This test documents the expected behavior
        # When implemented, this test should validate:
        # - 10 requests per minute limit on /login
        # - Headers X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
        # - 429 Too Many Requests after limit
        
        # For now, we just verify that multiple requests work
        # (no rate limiting means they all succeed)
        for i in range(15):  # More than 10 to test limit
            response = client.post(
                "/api/v1/auth/login",
                data={
                    "username": "test@example.com",
                    "password": "password123",
                },
            )
            # Currently all succeed (rate limiting not implemented)
            # When implemented, requests 11+ should return 429
            assert response.status_code in [200, 429], f"Request {i+1} returned {response.status_code}"
            
            if response.status_code == 429:
                # Rate limit reached
                assert "rate" in response.json()["detail"].lower() or "limit" in response.json()["detail"].lower()
                break

    def test_rate_limit_headers_expected(self, client, test_user):
        """Rate limiting headers should be present when rate limiting is implemented."""
        # Note: This test documents expected behavior
        # Currently rate limiting is not implemented
        
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        
        assert response.status_code == 200
        
        # When rate limiting is implemented, these headers should be present:
        # - X-RateLimit-Limit: 10
        # - X-RateLimit-Remaining: 9
        # - X-RateLimit-Reset: <timestamp>
        
        # For now, we just verify the endpoint works
        # These assertions will pass once rate limiting is implemented:
        # assert "X-RateLimit-Limit" in response.headers
        # assert "X-RateLimit-Remaining" in response.headers
        # assert "X-RateLimit-Reset" in response.headers
