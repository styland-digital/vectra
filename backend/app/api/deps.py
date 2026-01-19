"""API dependencies (auth, database, etc.)."""

from typing import Generator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.db.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Get current authenticated user with database validation.

    - Decodes JWT token
    - Validates token type is 'access'
    - Looks up user in database
    - Verifies user is active

    Raises:
        HTTPException 401: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if not payload:
        raise credentials_exception

    # Verify token type
    if payload.get("type") != "access":
        raise credentials_exception

    # Get user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception

    # Look up user in database
    try:
        user = db.query(User).filter(User.id == UUID(user_id)).first()
    except ValueError:
        raise credentials_exception

    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure user is active (redundant but explicit)."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


def require_role(allowed_roles: list[UserRole]):
    """
    Dependency factory for role-based access control.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.OWNER]))])
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user
    return role_checker


def get_current_verified_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user and verify email is verified."""
    if not current_user.email_verified_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required. Please verify your email before performing this action.",
        )
    return current_user


def get_platform_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user and verify they are platform admin."""
    if current_user.role != UserRole.PLATFORM_ADMIN or current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform admin access required",
        )
    return current_user


def get_organization_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user and verify they belong to an organization (not platform admin)."""
    if current_user.role == UserRole.PLATFORM_ADMIN or not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization user access required",
        )
    return current_user


def get_organization_id(current_user: User = Depends(get_current_user)) -> UUID:
    """Get current user's organization ID for multi-tenant queries."""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not belong to an organization",
        )
    return current_user.organization_id
