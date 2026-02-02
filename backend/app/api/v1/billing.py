"""Billing and Stripe integration endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
import json

from app.core.logging import get_logger
from app.api.deps import get_db, get_organization_user
from app.db.models.user import User
from app.services.stripe_service import StripeService
from app.schemas.billing import (
    CheckoutSessionCreate,
    CheckoutSessionResponse,
    PortalSessionResponse,
    PlansResponse
)

logger = get_logger(__name__)
router = APIRouter()


@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionCreate,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe checkout session for subscription."""
    try:
        stripe_service = StripeService(db)

        result = await stripe_service.create_checkout_session(
            plan_type=request.plan_type,
            organization_id=current_user.organization_id,
            customer_id=request.customer_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        return CheckoutSessionResponse(
            session_id=result["session_id"],
            session_url=result["session_url"]
        )

    except Exception as e:
        logger.error(f"Checkout session creation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_checkout_session(
    session_id: str,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Retrieve a Stripe checkout session."""
    try:
        stripe_service = StripeService(db)

        result = await stripe_service.get_session(session_id)

        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["error"])

        return result["session"]

    except Exception as e:
        logger.error(f"Session retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-portal-session", response_model=PortalSessionResponse)
async def create_portal_session(
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe customer portal session."""
    try:
        # Get organization's subscription to find customer_id
        from app.db.models.subscription import Subscription
        subscription = db.query(Subscription).filter(
            Subscription.organization_id == current_user.organization_id
        ).first()

        if not subscription or not subscription.stripe_customer_id:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )

        stripe_service = StripeService(db)

        result = await stripe_service.create_portal_session(
            customer_id=subscription.stripe_customer_id
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        return PortalSessionResponse(
            session_url=result["session_url"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Portal session creation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plans", response_model=PlansResponse)
async def get_plans():
    """Get available subscription plans."""
    try:
        stripe_service = StripeService()
        plans = stripe_service.get_plans()

        return PlansResponse(plans=plans)

    except Exception as e:
        logger.error(f"Plans retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Stripe webhook events."""
    try:
        payload = await request.body()
        signature = request.headers.get("stripe-signature")

        if not signature:
            raise HTTPException(status_code=400, detail="Missing signature header")

        stripe_service = StripeService(db)

        # Validate webhook signature
        if not stripe_service.validate_webhook_signature(payload, signature):
            raise HTTPException(status_code=400, detail="Invalid signature")

        # Parse event
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")

        # Process event
        result = stripe_service.handle_webhook_event(event)

        if not result["success"]:
            logger.error(f"Webhook processing failed: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])

        return {"status": "success", "message": result.get("message", "Event processed")}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))