"""Stripe service for payment processing and subscription management."""

import stripe
from typing import Dict, Any, Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models.organization import Organization
from app.db.models.subscription import Subscription, SubscriptionStatus, PlanType

logger = get_logger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Service for Stripe payment processing."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize Stripe service."""
        self.db = db
        self.logger = get_logger(self.__class__.__name__)

    # Plan configuration matching docs/specs/SPECIFICATION_TECHNIQUE_V2.md
    PLANS = {
        "starter": {
            "name": "Starter",
            "price": 99.00,
            "currency": "eur",
            "interval": "month",
            "features": {
                "leads_per_month": 500,
                "campaigns_active": 2,
                "users": 2,
                "emails_per_day": 50,
                "support": "Email"
            },
            "stripe_price_id": settings.STRIPE_PRICE_ID_STARTER
        },
        "growth": {
            "name": "Growth",
            "price": 299.00,
            "currency": "eur",
            "interval": "month",
            "features": {
                "leads_per_month": 2000,
                "campaigns_active": 5,
                "users": 5,
                "emails_per_day": 200,
                "support": "Email + Chat"
            },
            "stripe_price_id": settings.STRIPE_PRICE_ID_GROWTH
        },
        "scale": {
            "name": "Scale",
            "price": 799.00,
            "currency": "eur",
            "interval": "month",
            "features": {
                "leads_per_month": 10000,
                "campaigns_active": 999,
                "users": 15,
                "emails_per_day": 1000,
                "support": "Priority Support"
            },
            "stripe_price_id": settings.STRIPE_PRICE_ID_SCALE
        }
    }

    async def create_customer(
        self,
        organization: Organization,
        email: str,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a Stripe customer for an organization."""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name or organization.name,
                metadata={
                    "organization_id": str(organization.id),
                    "organization_name": organization.name
                }
            )

            self.logger.info(f"Created Stripe customer {customer.id} for org {organization.id}")
            return {
                "success": True,
                "customer_id": customer.id,
                "customer": customer
            }

        except stripe.StripeError as e:
            self.logger.error(f"Stripe customer creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_checkout_session(
        self,
        plan_type: str,
        organization_id: UUID,
        customer_id: Optional[str] = None,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a Stripe checkout session for subscription."""
        try:
            if plan_type not in self.PLANS:
                raise ValueError(f"Invalid plan type: {plan_type}")

            plan = self.PLANS[plan_type]

            # Default URLs
            if not success_url:
                success_url = f"{settings.FRONTEND_URL}/billing/success?session_id={{CHECKOUT_SESSION_ID}}"
            if not cancel_url:
                cancel_url = f"{settings.FRONTEND_URL}/pricing"

            session_config = {
                "payment_method_types": ["card"],
                "mode": "subscription",
                "line_items": [{
                    "price": plan["stripe_price_id"],
                    "quantity": 1,
                }],
                "success_url": success_url,
                "cancel_url": cancel_url,
                "metadata": {
                    "organization_id": str(organization_id),
                    "plan_type": plan_type
                },
                "subscription_data": {
                    "metadata": {
                        "organization_id": str(organization_id),
                        "plan_type": plan_type
                    }
                }
            }

            if customer_id:
                session_config["customer"] = customer_id
            else:
                session_config["customer_creation"] = "always"

            session = stripe.checkout.Session.create(**session_config)

            self.logger.info(f"Created checkout session {session.id} for org {organization_id}")
            return {
                "success": True,
                "session_id": session.id,
                "session_url": session.url,
                "session": session
            }

        except stripe.StripeError as e:
            self.logger.error(f"Checkout session creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_portal_session(
        self,
        customer_id: str,
        return_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a Stripe customer portal session."""
        try:
            if not return_url:
                return_url = f"{settings.FRONTEND_URL}/settings/billing"

            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )

            self.logger.info(f"Created portal session for customer {customer_id}")
            return {
                "success": True,
                "session_url": session.url,
                "session": session
            }

        except stripe.StripeError as e:
            self.logger.error(f"Portal session creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """Retrieve a Stripe checkout session."""
        try:
            session = stripe.checkout.Session.retrieve(
                session_id,
                expand=["subscription", "customer"]
            )

            return {
                "success": True,
                "session": session
            }

        except stripe.StripeError as e:
            self.logger.error(f"Session retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def handle_webhook_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Stripe webhook events."""
        try:
            event_type = event["type"]
            data_object = event["data"]["object"]

            self.logger.info(f"Processing webhook event: {event_type}")

            if event_type == "checkout.session.completed":
                return self._handle_checkout_completed(data_object)
            elif event_type == "invoice.payment_succeeded":
                return self._handle_payment_succeeded(data_object)
            elif event_type == "invoice.payment_failed":
                return self._handle_payment_failed(data_object)
            elif event_type == "customer.subscription.updated":
                return self._handle_subscription_updated(data_object)
            elif event_type == "customer.subscription.deleted":
                return self._handle_subscription_cancelled(data_object)
            else:
                self.logger.info(f"Unhandled webhook event: {event_type}")
                return {"success": True, "message": f"Event {event_type} ignored"}

        except Exception as e:
            self.logger.error(f"Webhook processing failed: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _handle_checkout_completed(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful checkout completion."""
        try:
            organization_id = session.get("metadata", {}).get("organization_id")
            plan_type = session.get("metadata", {}).get("plan_type")

            if not organization_id or not self.db:
                raise ValueError("Missing organization_id or database session")

            # Update or create subscription
            subscription = self.db.query(Subscription).filter(
                Subscription.organization_id == UUID(organization_id)
            ).first()

            if not subscription:
                subscription = Subscription(
                    organization_id=UUID(organization_id),
                    plan_type=PlanType(plan_type),
                    status=SubscriptionStatus.ACTIVE,
                    stripe_customer_id=session.get("customer"),
                    stripe_subscription_id=session.get("subscription"),
                )
                self.db.add(subscription)
            else:
                subscription.plan_type = PlanType(plan_type)
                subscription.status = SubscriptionStatus.ACTIVE
                subscription.stripe_customer_id = session.get("customer")
                subscription.stripe_subscription_id = session.get("subscription")

            self.db.commit()

            self.logger.info(f"Updated subscription for org {organization_id}: {plan_type}")
            return {"success": True, "message": "Subscription activated"}

        except Exception as e:
            if self.db:
                self.db.rollback()
            raise e

    def _handle_payment_succeeded(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful payment."""
        self.logger.info(f"Payment succeeded for invoice {invoice.get('id')}")
        # TODO: Update payment history, send confirmation email
        return {"success": True, "message": "Payment processed"}

    def _handle_payment_failed(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle failed payment."""
        self.logger.warning(f"Payment failed for invoice {invoice.get('id')}")
        # TODO: Implement dunning logic, notify customer
        return {"success": True, "message": "Payment failure processed"}

    def _handle_subscription_updated(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription update."""
        self.logger.info(f"Subscription updated: {subscription.get('id')}")
        # TODO: Sync subscription changes with database
        return {"success": True, "message": "Subscription updated"}

    def _handle_subscription_cancelled(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription cancellation."""
        self.logger.warning(f"Subscription cancelled: {subscription.get('id')}")
        # TODO: Update subscription status, preserve data for grace period
        return {"success": True, "message": "Subscription cancelled"}

    def get_plans(self) -> List[Dict[str, Any]]:
        """Get available subscription plans."""
        return [
            {
                "id": plan_id,
                **plan_data
            }
            for plan_id, plan_data in self.PLANS.items()
        ]

    def validate_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Validate Stripe webhook signature."""
        try:
            stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            return True
        except (ValueError, stripe.SignatureVerificationError):
            return False