"""Resend email service for sending transactional emails."""

from typing import Optional, Dict, Any
from pathlib import Path
import os

import resend
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import BadRequestError

logger = get_logger(__name__)

# Initialize Resend API key
_resend_initialized = False

def initialize_resend():
    """Initialize Resend with API key."""
    global _resend_initialized
    if not _resend_initialized:
        api_key = settings.RESEND_API_KEY
        if not api_key:
            logger.warning("RESEND_API_KEY not configured - emails will not be sent")
        else:
            resend.api_key = api_key
            _resend_initialized = True
            logger.info("Resend initialized successfully")


def load_email_template(template_name: str, context: Dict[str, Any]) -> tuple[str, str]:
    """
    Load and render email template.
    
    Args:
        template_name: Name of template file (e.g., 'verify-email')
        context: Template context variables
    
    Returns:
        Tuple of (html_content, text_content)
    """
    # Templates directory
    templates_dir = Path(__file__).parent.parent / "templates" / "emails"
    
    if not templates_dir.exists():
        # Fallback to simple HTML if templates dir doesn't exist
        logger.warning(f"Templates directory not found: {templates_dir}")
        return _generate_simple_html(template_name, context), _generate_simple_text(context)
    
    # Load logo if not provided
    logo_url = context.get("logo_url")
    if not logo_url:
        logo_path = templates_dir / "assets" / "logo.svg"
        if logo_path.exists():
            try:
                import base64
                with open(logo_path, "rb") as f:
                    logo_content = f.read()
                    logo_base64 = base64.b64encode(logo_content).decode("utf-8")
                    logo_url = f"data:image/svg+xml;base64,{logo_base64}"
            except Exception as e:
                logger.warning(f"Failed to load logo: {e}")
    
    # Add default context variables
    default_context = {
        "app_url": settings.APP_URL,
        "recipient_email": context.get("to", ""),
        "logo_url": logo_url,
    }
    context = {**default_context, **context}
    
    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Load HTML template
    try:
        html_template = env.get_template(f"{template_name}.html")
        html_content = html_template.render(**context)
    except Exception as e:
        logger.error(f"Failed to load template {template_name}: {e}", exc_info=True)
        # Fallback to simple HTML
        return _generate_simple_html(template_name, context), _generate_simple_text(context)
    
    # Generate text version (simplified)
    text_content = _generate_simple_text(template_name, context)
    
    return html_content, text_content


def _generate_simple_html(template_name: str, context: Dict[str, Any]) -> str:
    """Generate simple HTML email as fallback."""
    verification_url = context.get("verification_url", "")
    user_name = context.get("user_name", "utilisateur")
    
    if template_name == "verify-email":
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vérification de votre email</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #2E5BFF;">Bienvenue sur Vectra !</h1>
    <p>Bonjour {user_name},</p>
    <p>Merci de vous être inscrit sur Vectra. Pour compléter votre inscription, veuillez vérifier votre adresse email en cliquant sur le bouton ci-dessous :</p>
    <p style="text-align: center; margin: 30px 0;">
        <a href="{verification_url}" style="background-color: #2E5BFF; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Vérifier mon email</a>
    </p>
    <p>Ou copiez-collez ce lien dans votre navigateur :</p>
    <p style="word-break: break-all; color: #666;">{verification_url}</p>
    <p>Ce lien expire dans 24 heures.</p>
    <p>Si vous n'avez pas créé de compte sur Vectra, vous pouvez ignorer cet email.</p>
    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
    <p style="font-size: 12px; color: #999;">© 2026 Vectra. Tous droits réservés.</p>
</body>
</html>
"""
    return f"<html><body><p>{context}</p></body></html>"


def _generate_simple_text(template_name: str, context: Dict[str, Any]) -> str:
    """Generate simple text email version."""
    user_name = context.get("user_name", "utilisateur")
    app_url = context.get("app_url", settings.APP_URL)
    
    if template_name == "verify-email":
        otp = context.get("otp", "")
        email = context.get("to", "")
        return f"""
Verify your email

We need to verify your email address {email} before you can access your account. Enter the code below in your open browser window:

{otp}

This code expires in 10 minutes.

If you didn't sign up for Vectra, you can safely ignore this email. Someone else might have typed your email address by mistake.

© 2026 Vectra. All rights reserved.
{app_url}
"""
    elif template_name == "password-reset":
        reset_url = context.get("reset_url", "")
        return f"""
Réinitialisation de votre mot de passe - Vectra

Bonjour {user_name},

Vous avez demandé à réinitialiser votre mot de passe pour votre compte Vectra. Cliquez sur le lien ci-dessous pour créer un nouveau mot de passe :

{reset_url}

Ce lien expire dans 1 heure. Si vous n'avez pas demandé cette réinitialisation, vous pouvez ignorer cet email.

Pour des raisons de sécurité, ne partagez jamais ce lien avec qui que ce soit.

© 2026 Vectra. Tous droits réservés.
{app_url}
"""
    elif template_name == "notification":
        title = context.get("title", "Notification Vectra")
        body = context.get("body", "Vous avez reçu une nouvelle notification de Vectra.")
        action_url = context.get("action_url", "")
        return f"""
{title} - Vectra

Bonjour {user_name},

{body}

{f'Pour en savoir plus, visitez : {action_url}' if action_url else ''}

© 2026 Vectra. Tous droits réservés.
{app_url}
"""
    else:
        return f"""
Notification Vectra

Bonjour {user_name},

Vous avez reçu une nouvelle notification de Vectra.

© 2026 Vectra. Tous droits réservés.
{app_url}
"""


def send_email(
    to: str,
    subject: str,
    html_content: Optional[str] = None,
    text_content: Optional[str] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send email via Resend API.
    
    Args:
        to: Recipient email address
        subject: Email subject
        html_content: HTML content (required if text_content not provided)
        text_content: Plain text content (optional)
        from_email: Sender email (defaults to settings.RESEND_FROM_EMAIL)
        from_name: Sender name (optional)
    
    Returns:
        Dict with 'id' (email ID) and 'success' (bool)
    
    Raises:
        BadRequestError: If sending fails
    """
    # Initialize Resend
    initialize_resend()
    
    # Use default from email if not provided
    if not from_email:
        from_email = settings.RESEND_FROM_EMAIL
    
    # In development, use test email if no domain is verified
    if settings.ENVIRONMENT == "development" or settings.DEBUG:
        if not from_email or "@vectra.io" in from_email:
            from_email = "onboarding@resend.dev"
            logger.warning("Using Resend test email (onboarding@resend.dev) in development mode")
    
    if not from_email:
        raise BadRequestError("RESEND_FROM_EMAIL not configured")
    
    # In development without API key, log instead of sending
    if not settings.RESEND_API_KEY:
        logger.info(
            "Email would be sent via Resend",
            extra={
                "to": to,
                "subject": subject,
                "from": from_email,
                "mode": "development_log",
            }
        )
        return {"id": "dev-log", "success": True}
    
    try:
        # Build params
        params = {
            "from": f"{from_name} <{from_email}>" if from_name else from_email,
            "to": [to],  # Resend expects a list
            "subject": subject,
        }
        
        if html_content:
            params["html"] = html_content
        if text_content:
            params["text"] = text_content
        
        # Send email (Emails is a class, we need to instantiate it)
        emails = resend.Emails()
        response = emails.send(params)
        
        logger.info(
            "Email sent via Resend",
            extra={
                "to": to,
                "subject": subject,
                "email_id": response.get("id"),
            }
        )
        
        return {
            "id": response.get("id"),
            "success": True,
        }
        
    except Exception as e:
        logger.error(
            "Failed to send email via Resend",
            extra={
                "to": to,
                "subject": subject,
                "error": str(e),
            },
            exc_info=True,
        )
        raise BadRequestError(f"Failed to send email: {str(e)}")


def send_verification_email(
    to: str,
    otp: str,
    user_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send email verification email with OTP.
    
    Args:
        to: Recipient email address
        otp: 6-digit OTP code
        user_name: User's name (optional)
    
    Returns:
        Dict with 'id' and 'success'
    """
    # Load template
    context = {
        "to": to,
        "otp": otp,
        "user_name": user_name or "utilisateur",
        "subject": "Verify your email",
    }
    
    html_content, text_content = load_email_template("verify-email", context)
    
    # Send email
    return send_email(
        to=to,
        subject="Verify your email",
        html_content=html_content,
        text_content=text_content,
        from_name="Vectra",
    )


def send_password_reset_email(
    to: str,
    reset_url: str,
    user_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send password reset email.
    
    Args:
        to: Recipient email address
        reset_url: URL for password reset
        user_name: User's name (optional)
    
    Returns:
        Dict with 'id' and 'success'
    """
    context = {
        "to": to,
        "reset_url": reset_url,
        "user_name": user_name or "utilisateur",
        "subject": "Réinitialisation de votre mot de passe - Vectra",
    }
    
    html_content, text_content = load_email_template("password-reset", context)
    
    return send_email(
        to=to,
        subject="Réinitialisation de votre mot de passe - Vectra",
        html_content=html_content,
        text_content=text_content,
        from_name="Vectra",
    )


def send_notification_email(
    to: str,
    title: str,
    body: Optional[str] = None,
    body_html: Optional[str] = None,
    action_url: Optional[str] = None,
    action_text: Optional[str] = None,
    user_name: Optional[str] = None,
    alert_type: Optional[str] = None,
    alert_message: Optional[str] = None,
    unsubscribe_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send notification email.
    
    Args:
        to: Recipient email address
        title: Email title
        body: Plain text body (optional, ignored if body_html provided)
        body_html: HTML body content (optional)
        action_url: URL for CTA button (optional)
        action_text: Text for CTA button (optional)
        user_name: User's name (optional)
        alert_type: Type of alert ('success', 'warning', 'info') (optional)
        alert_message: Alert message (optional)
        unsubscribe_url: Unsubscribe link (optional)
    
    Returns:
        Dict with 'id' and 'success'
    """
    context = {
        "to": to,
        "title": title,
        "body": body,
        "body_html": body_html,
        "action_url": action_url,
        "action_text": action_text,
        "user_name": user_name or "utilisateur",
        "alert_type": alert_type,
        "alert_message": alert_message,
        "unsubscribe_url": unsubscribe_url,
        "subject": title,
    }
    
    html_content, text_content = load_email_template("notification", context)
    
    return send_email(
        to=to,
        subject=title,
        html_content=html_content,
        text_content=text_content,
        from_name="Vectra",
    )


def send_invitation_email(
    to: str,
    inviter_name: str,
    organization_name: str,
    invitation_url: str,
    role: str,
    otp: Optional[str] = None,
    user_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send user invitation email with OTP.
    
    Args:
        to: Recipient email address
        inviter_name: Name of user sending invitation
        organization_name: Organization name
        invitation_url: URL to accept invitation
        role: Role being assigned
        otp: 6-digit OTP code (required for OTP-based invitations)
        user_name: Recipient name (optional)
    
    Returns:
        Dict with 'id' and 'success'
    """
    context = {
        "to": to,
        "inviter_name": inviter_name,
        "organization_name": organization_name,
        "invitation_url": invitation_url,
        "role": role,
        "otp": otp,
        "user_name": user_name or "utilisateur",
        "subject": f"Invitation à rejoindre {organization_name} sur Vectra",
    }
    
    html_content, text_content = load_email_template("invite-user", context)
    
    return send_email(
        to=to,
        subject=f"Invitation à rejoindre {organization_name} sur Vectra",
        html_content=html_content,
        text_content=text_content,
        from_name="Vectra",
    )


# Wrapper class for convenience
class ResendService:
    """Wrapper class for Resend email service."""
    
    def __init__(self):
        pass
    
    def send_invitation_email(
        self,
        to: str,
        inviter_name: str,
        organization_name: str,
        invitation_url: str,
        role: str,
        user_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send invitation email."""
        return send_invitation_email(
            to=to,
            inviter_name=inviter_name,
            organization_name=organization_name,
            invitation_url=invitation_url,
            role=role,
            user_name=user_name,
        )
