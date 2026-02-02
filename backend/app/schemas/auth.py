"""Authentication schemas for request/response validation."""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class LoginRequest(BaseModel):
    """Login request with email and password."""
    email: EmailStr
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    """Token response after successful authentication."""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900  # 15 minutes in seconds


class RefreshRequest(BaseModel):
    """Request to refresh access token."""
    refresh_token: str = Field(min_length=1)


class RegisterRequest(BaseModel):
    """Request to register a new user with organization."""
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    organization_name: str = Field(max_length=255)


class OrganizationResponse(BaseModel):
    """Organization info in responses."""
    id: UUID
    name: str
    slug: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response for API."""
    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    organization_id: Optional[UUID] = None  # Nullable for platform admins
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserWithOrgResponse(BaseModel):
    """User response with organization details."""
    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    organization: Optional[OrganizationResponse] = None  # None for platform admins

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Full login response with tokens and user info."""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900
    user: UserWithOrgResponse


class VerifyEmailRequest(BaseModel):
    """Request to verify email with OTP."""
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6, pattern="^[0-9]{6}$")


class SendVerificationEmailRequest(BaseModel):
    """Request to send verification email."""
    email: EmailStr


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class ForgotPasswordRequest(BaseModel):
    """Request to send password reset email."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Request to reset password with token."""
    token: str = Field(min_length=1)
    password: str = Field(min_length=8)
    password_confirmation: str = Field(min_length=8)


class AcceptInvitationRequest(BaseModel):
    """Request to accept invitation with OTP."""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]{6}$")
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class RequestPasswordChangeRequest(BaseModel):
    """Request to send password change OTP."""
    pass  # No fields needed, uses authenticated user


class ChangePasswordWithOtpRequest(BaseModel):
    """Request to change password with OTP verification."""
    otp: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]{6}$")
    new_password: str = Field(..., min_length=8)
