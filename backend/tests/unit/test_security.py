"""Unit tests for security module (JWT tokens and password hashing)."""

import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings


class TestPasswordHashing:
    """Tests for password hashing functions."""

    def test_hash_password_returns_hash(self):
        """Password hash should be different from plain password."""
        password = "mysecretpassword"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt prefix

    def test_verify_password_correct(self):
        """Correct password should verify successfully."""
        password = "mysecretpassword"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Incorrect password should fail verification."""
        password = "mysecretpassword"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_hash_is_unique_each_time(self):
        """Same password should produce different hashes (salted)."""
        password = "mysecretpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        # Both should still verify
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_empty_password_still_hashes(self):
        """Empty password should still produce a hash."""
        hashed = get_password_hash("")
        assert len(hashed) > 0
        assert verify_password("", hashed) is True

    def test_long_password_hashes(self):
        """Very long password (>1000 chars) should hash successfully."""
        long_password = "a" * 2000
        hashed = get_password_hash(long_password)
        assert len(hashed) > 0
        assert verify_password(long_password, hashed) is True

    def test_unicode_password_hashes(self):
        """Password with Unicode characters should hash correctly."""
        unicode_passwords = [
            "pässwörd123",
            "密码123",
            "пароль123",
            "🎂🎁🎉",
            "émoji 😀😁😂",
        ]
        for password in unicode_passwords:
            hashed = get_password_hash(password)
            assert verify_password(password, hashed) is True
            # Unicode should not match similar ASCII
            assert verify_password(password.encode("ascii", "ignore").decode(), hashed) is False

    def test_password_with_spaces(self):
        """Passwords with spaces should be handled correctly (no automatic trimming)."""
        password_with_spaces = "  password123  "
        hashed = get_password_hash(password_with_spaces)
        # Spaces are part of the password - should verify with exact match
        assert verify_password(password_with_spaces, hashed) is True
        # Without spaces should fail
        assert verify_password("password123", hashed) is False

    def test_password_hashing_performance(self):
        """Password hashing should complete in reasonable time (< 500ms)."""
        import time
        password = "test_password_123"
        start = time.time()
        hashed = get_password_hash(password)
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        assert elapsed < 500, f"Password hashing took {elapsed}ms, should be < 500ms"
        assert verify_password(password, hashed) is True


class TestAccessToken:
    """Tests for access token creation and validation."""

    def test_create_access_token_with_data(self):
        """Access token should contain the provided data."""
        data = {"sub": "user123", "role": "admin"}
        token = create_access_token(data)

        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        assert decoded["sub"] == "user123"
        assert decoded["role"] == "admin"

    def test_access_token_contains_type_access(self):
        """Access token should have type='access' claim."""
        data = {"sub": "user123"}
        token = create_access_token(data)

        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        assert decoded["type"] == "access"

    def test_access_token_has_expiration(self):
        """Access token should have exp claim."""
        data = {"sub": "user123"}
        token = create_access_token(data)

        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        assert "exp" in decoded
        # Should expire in the future
        assert decoded["exp"] > datetime.now(timezone.utc).timestamp()

    def test_access_token_custom_expiration(self):
        """Access token should accept custom expiration."""
        data = {"sub": "user123"}
        expires_delta = timedelta(hours=1)
        token = create_access_token(data, expires_delta=expires_delta)

        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        expected_exp = datetime.now(timezone.utc) + expires_delta
        # Allow 5 second tolerance
        assert abs(decoded["exp"] - expected_exp.timestamp()) < 5

    def test_decode_valid_access_token(self):
        """Valid access token should decode successfully."""
        data = {"sub": "user123", "role": "admin"}
        token = create_access_token(data)

        decoded = decode_token(token)

        assert decoded is not None
        assert decoded["sub"] == "user123"
        assert decoded["type"] == "access"

    def test_decode_expired_token_returns_none(self):
        """Expired token should return None."""
        data = {"sub": "user123"}
        # Create token that expired 1 hour ago
        expires_delta = timedelta(hours=-1)
        token = create_access_token(data, expires_delta=expires_delta)

        decoded = decode_token(token)

        assert decoded is None

    def test_decode_invalid_token_returns_none(self):
        """Invalid token should return None."""
        invalid_token = "invalid.token.here"

        decoded = decode_token(invalid_token)

        assert decoded is None

    def test_decode_token_wrong_secret_returns_none(self):
        """Token signed with different secret should return None."""
        data = {"sub": "user123"}
        # Create token with different secret
        token = jwt.encode(
            {**data, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
            "different-secret",
            algorithm=settings.JWT_ALGORITHM,
        )

        decoded = decode_token(token)

        assert decoded is None

    def test_decode_token_without_signature_returns_none(self):
        """Token without signature should return None."""
        # Attempt to create unsigned token (jwt.encode always signs, so we create malformed)
        malformed_token = "eyJhbGciOiJub25lIn0.eyJzdWIiOiJ1c2VyMTIzIn0."
        decoded = decode_token(malformed_token)
        assert decoded is None

    def test_decode_token_none_algorithm_attack_returns_none(self):
        """Token with algorithm 'none' should be rejected (algorithm attack prevention)."""
        # Create token with algorithm 'none' (attack vector)
        payload = {
            "sub": "user123",
            "type": "access",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        # jwt.encode doesn't allow 'none' algorithm by default, so we create manually
        # The decode_token function only accepts algorithms from settings, so 'none' should fail
        try:
            token = jwt.encode(payload, "", algorithm="none")
        except Exception:
            # If jwt.encode doesn't allow none, that's fine - our decode should also reject it
            token = "eyJhbGciOiJub25lIn0.eyJzdWIiOiJ1c2VyMTIzIn0."
        decoded = decode_token(token)
        assert decoded is None

    def test_decode_token_manipulated_returns_none(self):
        """Manipulated token (middle bytes changed) should return None."""
        data = {"sub": "user123"}
        token = create_access_token(data)
        # Manipulate token by changing middle bytes
        token_parts = token.split(".")
        if len(token_parts) == 3:
            # Change middle part (payload)
            manipulated_token = f"{token_parts[0]}.{token_parts[1][:-5]}XXXX.{token_parts[2]}"
            decoded = decode_token(manipulated_token)
            assert decoded is None

    def test_decode_token_expired_but_valid_structure_returns_none(self):
        """Expired token should return None even if structure is valid."""
        data = {"sub": "user123"}
        expires_delta = timedelta(hours=-1)  # Expired 1 hour ago
        token = create_access_token(data, expires_delta=expires_delta)
        # Token structure is valid but expired
        decoded = decode_token(token)
        assert decoded is None

    def test_decode_token_without_type_claim(self):
        """Token without type claim should decode but type check should fail in deps."""
        # Create token without type claim (manual creation)
        payload = {
            "sub": "user123",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        decoded = decode_token(token)
        # decode_token should return payload, but type will be missing
        assert decoded is not None
        assert "type" not in decoded

    def test_decode_token_with_invalid_type_claim(self):
        """Token with invalid type claim ('hacked') should decode but fail validation in deps."""
        payload = {
            "sub": "user123",
            "type": "hacked",  # Invalid type
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        decoded = decode_token(token)
        # decode_token returns payload, validation happens in deps.get_current_user
        assert decoded is not None
        assert decoded["type"] == "hacked"
        assert decoded["type"] != "access"

    def test_access_token_contains_all_required_claims(self):
        """Access token should contain all required claims: sub, org, role, type, exp."""
        data = {"sub": "user123", "org": "org456", "role": "admin"}
        token = create_access_token(data)
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        assert "sub" in decoded
        assert "org" in decoded
        assert "role" in decoded
        assert "type" in decoded
        assert decoded["type"] == "access"
        assert "exp" in decoded
        # iat might not be explicitly set, but exp should be there

    def test_access_token_expiration_matches_config(self):
        """Access token expiration should match JWT_ACCESS_TOKEN_EXPIRE_MINUTES setting."""
        data = {"sub": "user123"}
        token = create_access_token(data)
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        now = datetime.now(timezone.utc)
        exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        expected_exp = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        # Allow 60 second tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 60

    def test_access_token_custom_expiration_minute(self):
        """Access token should accept custom expiration of 1 minute."""
        data = {"sub": "user123"}
        custom_exp = timedelta(minutes=1)
        token = create_access_token(data, expires_delta=custom_exp)
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        now = datetime.now(timezone.utc)
        exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        expected_exp = now + custom_exp
        # Allow 5 second tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 5

    def test_access_token_custom_expiration_hour(self):
        """Access token should accept custom expiration of 1 hour."""
        data = {"sub": "user123"}
        custom_exp = timedelta(hours=1)
        token = create_access_token(data, expires_delta=custom_exp)
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        now = datetime.now(timezone.utc)
        exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        expected_exp = now + custom_exp
        # Allow 5 second tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 5


class TestRefreshToken:
    """Tests for refresh token creation and validation."""

    def test_create_refresh_token_with_data(self):
        """Refresh token should contain the provided data."""
        data = {"sub": "user123", "role": "admin"}
        token = create_refresh_token(data)

        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        assert decoded["sub"] == "user123"
        assert decoded["role"] == "admin"

    def test_refresh_token_contains_type_refresh(self):
        """Refresh token should have type='refresh' claim."""
        data = {"sub": "user123"}
        token = create_refresh_token(data)

        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        assert decoded["type"] == "refresh"

    def test_refresh_token_expires_in_7_days(self):
        """Refresh token should expire in approximately 7 days."""
        data = {"sub": "user123"}
        token = create_refresh_token(data)

        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        expected_exp = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        # Allow 60 second tolerance
        assert abs(decoded["exp"] - expected_exp.timestamp()) < 60

    def test_decode_valid_refresh_token(self):
        """Valid refresh token should decode successfully."""
        data = {"sub": "user123", "org": "org456"}
        token = create_refresh_token(data)

        decoded = decode_token(token)

        assert decoded is not None
        assert decoded["sub"] == "user123"
        assert decoded["org"] == "org456"
        assert decoded["type"] == "refresh"

    def test_access_and_refresh_tokens_are_different(self):
        """Access and refresh tokens for same data should be different."""
        data = {"sub": "user123"}
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)

        assert access_token != refresh_token

        access_decoded = decode_token(access_token)
        refresh_decoded = decode_token(refresh_token)

        assert access_decoded["type"] == "access"
        assert refresh_decoded["type"] == "refresh"

    def test_refresh_token_expired_returns_none(self):
        """Expired refresh token should return None."""
        data = {"sub": "user123"}
        # Create refresh token that expired 1 day ago
        # Since refresh token creation doesn't accept custom expiration,
        # we need to create it manually
        payload = {
            **data,
            "type": "refresh",
            "exp": datetime.now(timezone.utc) - timedelta(days=1),
        }
        expired_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        decoded = decode_token(expired_token)
        assert decoded is None

    def test_refresh_token_idempotency(self):
        """Refresh token can be used multiple times (idempotency - no single-use restriction)."""
        data = {"sub": "user123", "org": "org456", "role": "admin"}
        refresh_token = create_refresh_token(data)
        # Decode multiple times should work
        decoded1 = decode_token(refresh_token)
        decoded2 = decode_token(refresh_token)
        decoded3 = decode_token(refresh_token)
        assert decoded1 == decoded2 == decoded3
        assert decoded1["type"] == "refresh"

    def test_refresh_token_with_invalid_user_id_in_payload(self):
        """Refresh token with invalid user_id should decode but fail in AuthService."""
        # Create token with non-existent user_id
        payload = {
            "sub": "00000000-0000-0000-0000-000000000000",  # Invalid UUID
            "org": "org456",
            "role": "admin",
            "type": "refresh",
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        decoded = decode_token(token)
        # decode_token should return payload, but AuthService should reject invalid user_id
        assert decoded is not None
        assert decoded["sub"] == "00000000-0000-0000-0000-000000000000"
