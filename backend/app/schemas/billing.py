"""Billing and Stripe schema definitions."""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum


class PlanType(str, Enum):
    """Available subscription plans."""
    STARTER = "starter"
    GROWTH = "growth"
    SCALE = "scale"


class CheckoutSessionCreate(BaseModel):
    """Request schema for creating a Stripe checkout session."""
    plan_type: PlanType = Field(..., description="The subscription plan to purchase")
    customer_id: Optional[str] = Field(None, description="Existing Stripe customer ID")
    success_url: Optional[str] = Field(None, description="URL to redirect to on success")
    cancel_url: Optional[str] = Field(None, description="URL to redirect to on cancellation")

    class Config:
        json_schema_extra = {
            "example": {
                "plan_type": "starter",
                "customer_id": "cus_example123",
                "success_url": "https://app.vectra.io/billing/success",
                "cancel_url": "https://app.vectra.io/pricing"
            }
        }


class CheckoutSessionResponse(BaseModel):
    """Response schema for Stripe checkout session."""
    session_id: str = Field(..., description="Stripe checkout session ID")
    session_url: str = Field(..., description="URL to redirect user to Stripe checkout")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "cs_test_example123",
                "session_url": "https://checkout.stripe.com/c/pay/cs_test_example123"
            }
        }


class PortalSessionResponse(BaseModel):
    """Response schema for Stripe customer portal session."""
    session_url: str = Field(..., description="URL to redirect user to Stripe customer portal")

    class Config:
        json_schema_extra = {
            "example": {
                "session_url": "https://billing.stripe.com/p/session/cs_test_example123"
            }
        }


class PlanFeatures(BaseModel):
    """Features included in a subscription plan."""
    leads_per_month: int = Field(..., description="Maximum leads per month")
    campaigns_active: int = Field(..., description="Maximum active campaigns")
    users: int = Field(..., description="Maximum number of users")
    emails_per_day: int = Field(..., description="Maximum emails per day")
    support: str = Field(..., description="Support level included")


class Plan(BaseModel):
    """Subscription plan details."""
    id: str = Field(..., description="Plan identifier")
    name: str = Field(..., description="Plan display name")
    price: float = Field(..., description="Monthly price in euros")
    currency: str = Field("eur", description="Currency code")
    interval: str = Field("month", description="Billing interval")
    features: PlanFeatures = Field(..., description="Plan features")
    stripe_price_id: str = Field(..., description="Stripe price ID")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "starter",
                "name": "Starter",
                "price": 99.0,
                "currency": "eur",
                "interval": "month",
                "features": {
                    "leads_per_month": 500,
                    "campaigns_active": 2,
                    "users": 2,
                    "emails_per_day": 50,
                    "support": "Email"
                },
                "stripe_price_id": "price_starter_monthly"
            }
        }


class PlansResponse(BaseModel):
    """Response schema for available plans."""
    plans: List[Plan] = Field(..., description="List of available subscription plans")

    class Config:
        json_schema_extra = {
            "example": {
                "plans": [
                    {
                        "id": "starter",
                        "name": "Starter",
                        "price": 99.0,
                        "currency": "eur",
                        "interval": "month",
                        "features": {
                            "leads_per_month": 500,
                            "campaigns_active": 2,
                            "users": 2,
                            "emails_per_day": 50,
                            "support": "Email"
                        },
                        "stripe_price_id": "price_starter_monthly"
                    }
                ]
            }
        }


class WebhookEvent(BaseModel):
    """Stripe webhook event schema."""
    id: str = Field(..., description="Event ID")
    type: str = Field(..., description="Event type")
    data: Dict[str, Any] = Field(..., description="Event data")
    created: int = Field(..., description="Event creation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "evt_example123",
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "id": "cs_test_example123",
                        "customer": "cus_example123",
                        "subscription": "sub_example123"
                    }
                },
                "created": 1640995200
            }
        }