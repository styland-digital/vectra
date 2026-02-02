"""Organization schemas for request/response validation."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.db.models.organization import PlanType


class OrganizationResponse(BaseModel):
    """Organization response with details."""
    id: UUID
    name: str
    slug: str
    plan: str
    settings: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationUpdate(BaseModel):
    """Request to update organization."""
    name: Optional[str] = Field(None, max_length=255)
    plan: Optional[str] = None
    settings: Optional[dict] = None


class OrganizationUserResponse(BaseModel):
    """User in organization response."""
    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    is_active: bool
    email_verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InviteUserRequest(BaseModel):
    """Request to invite a user to organization."""
    email: str = Field(..., max_length=255)
    role: str = Field(default="operator", max_length=50)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UpdateUserRoleRequest(BaseModel):
    """Request to update user role in organization."""
    role: str = Field(..., max_length=50)


class CreateUserRequest(BaseModel):
    """Request to create user directly in organization."""
    email: str = Field(..., max_length=255)
    role: str = Field(..., max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    send_welcome_email: bool = Field(default=True)
