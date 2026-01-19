"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.auth import (
    TokenResponse,
    RefreshRequest,
    RegisterRequest,
    UserResponse,
    UserWithOrgResponse,
    OrganizationResponse,
    LoginResponse,
    VerifyEmailRequest,
    SendVerificationEmailRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    AcceptInvitationRequest,
    MessageResponse,
)
from app.schemas.user import ChangePasswordRequest
from app.services.auth import AuthService
from app.services.email_verification import EmailVerificationService
from app.services.password_reset import PasswordResetService
from app.services.invitation import InvitationService
from app.db.models.user import User

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login with email and password.

    Returns access token, refresh token, and user info.
    OAuth2 compatible (uses form data with username field for email).
    """
    # Validate required fields
    if not form_data.username or not form_data.password:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email and password are required",
        )
    
    auth_service = AuthService(db)
    access_token, refresh_token, user = auth_service.authenticate(
        email=form_data.username,  # OAuth2 uses 'username' field
        password=form_data.password,
    )

    # Build UserWithOrgResponse
    org_response = None
    if user.organization:
        org_response = OrganizationResponse(
            id=user.organization.id,
            name=user.organization.name,
            slug=user.organization.slug,
        )
    
    user_response = UserWithOrgResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at,
        organization=org_response,
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db),
):
    """
    Refresh access token using refresh token.

    Returns new access token (refresh token remains unchanged).
    """
    auth_service = AuthService(db)
    new_access_token = auth_service.refresh_access_token(request.refresh_token)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=request.refresh_token,
    )


@router.post("/logout", status_code=204)
def logout(
    current_user: User = Depends(get_current_user),
):
    """
    Logout current user.

    Client should discard tokens. Server-side token blacklisting
    can be implemented with Redis if needed.
    """
    # Stateless logout - client discards tokens
    # For stateful logout, implement token blacklist in Redis
    return Response(status_code=204)


@router.post("/register", response_model=LoginResponse, status_code=201)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user with a new organization.

    Creates organization and user as owner.
    Returns access token, refresh token, and user info.
    """
    auth_service = AuthService(db)
    access_token, refresh_token, user = auth_service.register(
        email=request.email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
        organization_name=request.organization_name,
    )

    # Build UserWithOrgResponse
    org_response = None
    if hasattr(user, 'organization') and user.organization:
        org_response = OrganizationResponse(
            id=user.organization.id,
            name=user.organization.name,
            slug=user.organization.slug,
        )
    
    user_response = UserWithOrgResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at,
        organization=org_response,
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response,
    )


@router.post("/change-password", status_code=204)
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Change current user's password.
    """
    auth_service = AuthService(db)
    auth_service.change_password(
        user=current_user,
        current_password=request.current_password,
        new_password=request.new_password,
    )
    return Response(status_code=204)


@router.post("/verify-email", response_model=MessageResponse, status_code=200)
def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db),
):
    """
    Verify user email with 6-digit OTP.
    """
    verification_service = EmailVerificationService(db)
    verification_service.verify_email_with_otp(request.email, request.otp)

    return MessageResponse(message="Email verified successfully")


@router.post("/send-verification-email", response_model=MessageResponse, status_code=200)
def send_verification_email(
    request: SendVerificationEmailRequest,
    db: Session = Depends(get_db),
):
    """
    Send verification email to user.
    
    Note: Always returns success for security (don't reveal if email exists).
    """
    verification_service = EmailVerificationService(db)
    try:
        verification_service.send_verification_email(request.email)
    except Exception:
        # Don't reveal if email exists or is already verified
        pass

    return MessageResponse(message="If the email exists and is not verified, a verification email will be sent")


@router.post("/resend-verification-email", response_model=MessageResponse, status_code=200)
def resend_verification_email(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Resend verification email to current user.
    """
    verification_service = EmailVerificationService(db)
    verification_service.resend_verification_email(current_user)

    return MessageResponse(message="Verification email sent")


@router.post("/forgot-password", response_model=MessageResponse, status_code=200)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Send password reset email to user.
    
    Note: Always returns success for security (don't reveal if email exists).
    """
    password_reset_service = PasswordResetService(db)
    try:
        password_reset_service.send_reset_email(request.email)
    except Exception:
        # Don't reveal if email exists
        pass

    return MessageResponse(message="If the email exists, a password reset email will be sent")


@router.post("/reset-password", response_model=MessageResponse, status_code=200)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Reset user password with reset token.
    
    Validates password confirmation and updates user password.
    """
    # Validate password confirmation
    if request.password != request.password_confirmation:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    password_reset_service = PasswordResetService(db)
    password_reset_service.reset_password_with_token(request.token, request.password)

    return MessageResponse(message="Password reset successful")


@router.post("/invite/accept", response_model=LoginResponse, status_code=200)
def accept_invitation(
    request: AcceptInvitationRequest,
    db: Session = Depends(get_db),
):
    """
    Accept invitation using OTP and create user account.
    
    User provides email, OTP, and sets password.
    Returns access token, refresh token, and user info.
    """
    invitation_service = InvitationService(db)
    access_token, refresh_token, user = invitation_service.accept_invitation(
        email=request.email,
        otp=request.otp,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
    )
    
    # Build UserWithOrgResponse
    org_response = None
    if user.organization:
        org_response = OrganizationResponse(
            id=user.organization.id,
            name=user.organization.name,
            slug=user.organization.slug,
        )
    
    user_response = UserWithOrgResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at,
        organization=org_response,
    )
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response,
    )
