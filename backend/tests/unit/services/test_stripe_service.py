"""Unit tests for StripeService.

Tests for Stripe payment processing, subscription management, webhook handling,
and plan configuration.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from uuid import uuid4, UUID
import stripe

from app.services.stripe_service import StripeService
from app.db.models.organization import Organization
from app.db.models.subscription import Subscription, SubscriptionStatus, PlanType


class TestStripeService:
    """Test StripeService functionality."""

    @pytest.fixture
    def db_session(self):
        """Mock database session."""
        return Mock()

    @pytest.fixture
    def stripe_service(self, db_session):
        """StripeService instance with mocked DB."""
        return StripeService(db=db_session)

    @pytest.fixture
    def stripe_service_no_db(self):
        """StripeService instance without DB for some tests."""
        return StripeService()

    @pytest.fixture
    def organization(self):
        """Sample organization for testing."""
        return Mock(
            id=uuid4(),
            name="Acme Corp",
            spec=Organization
        )

    @pytest.fixture
    def customer_data(self):
        """Sample Stripe customer data."""
        return {
            "id": "cus_test123",
            "email": "billing@acme.com",
            "name": "Acme Corp"
        }

    @pytest.fixture
    def checkout_session_data(self):
        """Sample Stripe checkout session data."""
        return {
            "id": "cs_test123",
            "url": "https://checkout.stripe.com/pay/cs_test123",
            "customer": "cus_test123",
            "subscription": "sub_test123",
            "metadata": {
                "organization_id": str(uuid4()),
                "plan_type": "growth"
            }
        }

    @pytest.fixture
    def webhook_event_data(self):
        """Sample webhook event data."""
        return {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test123",
                    "customer": "cus_test123",
                    "subscription": "sub_test123",
                    "metadata": {
                        "organization_id": str(uuid4()),
                        "plan_type": "growth"
                    }
                }
            }
        }

    class TestInitialization:
        """Test service initialization."""

        def test_init_with_db(self, db_session):
            """Test initialization with database session."""
            service = StripeService(db=db_session)
            assert service.db == db_session
            assert service.logger is not None

        def test_init_without_db(self):
            """Test initialization without database session."""
            service = StripeService()
            assert service.db is None
            assert service.logger is not None

        def test_plans_configuration(self, stripe_service):
            """Test that plans are properly configured."""
            plans = stripe_service.PLANS

            # Check all required plans exist
            assert "starter" in plans
            assert "growth" in plans
            assert "scale" in plans

            # Check starter plan structure
            starter = plans["starter"]
            assert starter["name"] == "Starter"
            assert starter["price"] == 99.00
            assert starter["currency"] == "eur"
            assert starter["interval"] == "month"
            assert "features" in starter
            assert "stripe_price_id" in starter

            # Check features structure
            features = starter["features"]
            assert "leads_per_month" in features
            assert "campaigns_active" in features
            assert "users" in features
            assert "emails_per_day" in features
            assert "support" in features

            # Verify price progression
            assert plans["starter"]["price"] < plans["growth"]["price"] < plans["scale"]["price"]

    class TestCreateCustomer:
        """Test Stripe customer creation."""

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.Customer.create')
        async def test_create_customer_success(
            self, mock_create, stripe_service, organization, customer_data
        ):
            """Test successful customer creation."""
            mock_create.return_value = Mock(**customer_data)

            result = await stripe_service.create_customer(
                organization=organization,
                email="billing@acme.com",
                name="Acme Corp"
            )

            # Verify Stripe API call
            mock_create.assert_called_once_with(
                email="billing@acme.com",
                name="Acme Corp",
                metadata={
                    "organization_id": str(organization.id),
                    "organization_name": organization.name
                }
            )

            # Verify result
            assert result["success"] is True
            assert result["customer_id"] == customer_data["id"]
            assert "customer" in result

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.Customer.create')
        async def test_create_customer_default_name(
            self, mock_create, stripe_service, organization, customer_data
        ):
            """Test customer creation with default name from organization."""
            mock_create.return_value = Mock(**customer_data)

            result = await stripe_service.create_customer(
                organization=organization,
                email="billing@acme.com"
            )

            # Should use organization name as default
            mock_create.assert_called_once_with(
                email="billing@acme.com",
                name=organization.name,
                metadata={
                    "organization_id": str(organization.id),
                    "organization_name": organization.name
                }
            )

            assert result["success"] is True

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.Customer.create')
        async def test_create_customer_stripe_error(
            self, mock_create, stripe_service, organization
        ):
            """Test customer creation with Stripe error."""
            mock_create.side_effect = stripe.StripeError("Payment method required")

            result = await stripe_service.create_customer(
                organization=organization,
                email="billing@acme.com"
            )

            assert result["success"] is False
            assert "error" in result
            assert "Payment method required" in result["error"]

    class TestCreateCheckoutSession:
        """Test Stripe checkout session creation."""

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.checkout.Session.create')
        @patch('app.services.stripe_service.settings')
        async def test_create_checkout_session_success(
            self, mock_settings, mock_create, stripe_service, checkout_session_data
        ):
            """Test successful checkout session creation."""
            mock_settings.FRONTEND_URL = "https://app.vectra.com"
            mock_settings.STRIPE_PRICE_ID_GROWTH = "price_growth123"
            mock_create.return_value = Mock(**checkout_session_data)

            organization_id = uuid4()
            customer_id = "cus_test123"

            result = await stripe_service.create_checkout_session(
                plan_type="growth",
                organization_id=organization_id,
                customer_id=customer_id,
                success_url="https://app.vectra.com/success",
                cancel_url="https://app.vectra.com/cancel"
            )

            # Verify Stripe API call
            mock_create.assert_called_once()
            call_args = mock_create.call_args[1]

            assert call_args["payment_method_types"] == ["card"]
            assert call_args["mode"] == "subscription"
            assert call_args["line_items"][0]["price"] == "price_growth123"
            assert call_args["customer"] == customer_id
            assert call_args["success_url"] == "https://app.vectra.com/success"
            assert call_args["cancel_url"] == "https://app.vectra.com/cancel"
            assert call_args["metadata"]["organization_id"] == str(organization_id)
            assert call_args["metadata"]["plan_type"] == "growth"

            # Verify result
            assert result["success"] is True
            assert result["session_id"] == checkout_session_data["id"]
            assert result["session_url"] == checkout_session_data["url"]

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.checkout.Session.create')
        @patch('app.services.stripe_service.settings')
        async def test_create_checkout_session_no_customer(
            self, mock_settings, mock_create, stripe_service, checkout_session_data
        ):
            """Test checkout session creation without existing customer."""
            mock_settings.FRONTEND_URL = "https://app.vectra.com"
            mock_settings.STRIPE_PRICE_ID_STARTER = "price_starter123"
            mock_create.return_value = Mock(**checkout_session_data)

            organization_id = uuid4()

            result = await stripe_service.create_checkout_session(
                plan_type="starter",
                organization_id=organization_id
            )

            # Verify customer creation is enabled
            call_args = mock_create.call_args[1]
            assert "customer" not in call_args
            assert call_args["customer_creation"] == "always"

            assert result["success"] is True

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.settings')
        async def test_create_checkout_session_default_urls(
            self, mock_settings, stripe_service
        ):
            """Test checkout session with default URLs."""
            mock_settings.FRONTEND_URL = "https://app.vectra.com"

            with patch('app.services.stripe_service.stripe.checkout.Session.create') as mock_create:
                mock_create.return_value = Mock(id="cs_test", url="https://test.com")

                await stripe_service.create_checkout_session(
                    plan_type="growth",
                    organization_id=uuid4()
                )

                call_args = mock_create.call_args[1]
                assert "session_id={CHECKOUT_SESSION_ID}" in call_args["success_url"]
                assert call_args["cancel_url"].endswith("/pricing")

        @pytest.mark.asyncio
        async def test_create_checkout_session_invalid_plan(self, stripe_service):
            """Test checkout session creation with invalid plan type."""
            result = await stripe_service.create_checkout_session(
                plan_type="invalid_plan",
                organization_id=uuid4()
            )

            assert result["success"] is False
            assert "Invalid plan type" in result["error"]

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.checkout.Session.create')
        async def test_create_checkout_session_stripe_error(
            self, mock_create, stripe_service
        ):
            """Test checkout session creation with Stripe error."""
            mock_create.side_effect = stripe.StripeError("Card declined")

            result = await stripe_service.create_checkout_session(
                plan_type="starter",
                organization_id=uuid4()
            )

            assert result["success"] is False
            assert "Card declined" in result["error"]

    class TestCreatePortalSession:
        """Test Stripe customer portal session creation."""

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.billing_portal.Session.create')
        @patch('app.services.stripe_service.settings')
        async def test_create_portal_session_success(
            self, mock_settings, mock_create, stripe_service
        ):
            """Test successful portal session creation."""
            mock_settings.FRONTEND_URL = "https://app.vectra.com"
            mock_create.return_value = Mock(
                url="https://billing.stripe.com/p/session_123"
            )

            customer_id = "cus_test123"
            return_url = "https://app.vectra.com/settings"

            result = await stripe_service.create_portal_session(
                customer_id=customer_id,
                return_url=return_url
            )

            # Verify Stripe API call
            mock_create.assert_called_once_with(
                customer=customer_id,
                return_url=return_url
            )

            assert result["success"] is True
            assert result["session_url"] == "https://billing.stripe.com/p/session_123"

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.billing_portal.Session.create')
        @patch('app.services.stripe_service.settings')
        async def test_create_portal_session_default_url(
            self, mock_settings, mock_create, stripe_service
        ):
            """Test portal session creation with default return URL."""
            mock_settings.FRONTEND_URL = "https://app.vectra.com"
            mock_create.return_value = Mock(url="https://billing.stripe.com/test")

            await stripe_service.create_portal_session(customer_id="cus_test123")

            call_args = mock_create.call_args[1]
            assert call_args["return_url"].endswith("/settings/billing")

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.billing_portal.Session.create')
        async def test_create_portal_session_stripe_error(
            self, mock_create, stripe_service
        ):
            """Test portal session creation with Stripe error."""
            mock_create.side_effect = stripe.StripeError("Customer not found")

            result = await stripe_service.create_portal_session(customer_id="cus_invalid")

            assert result["success"] is False
            assert "Customer not found" in result["error"]

    class TestGetSession:
        """Test Stripe session retrieval."""

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.checkout.Session.retrieve')
        async def test_get_session_success(self, mock_retrieve, stripe_service):
            """Test successful session retrieval."""
            session_data = {"id": "cs_test123", "status": "complete"}
            mock_retrieve.return_value = Mock(**session_data)

            result = await stripe_service.get_session("cs_test123")

            # Verify Stripe API call with expand
            mock_retrieve.assert_called_once_with(
                "cs_test123",
                expand=["subscription", "customer"]
            )

            assert result["success"] is True
            assert "session" in result

        @pytest.mark.asyncio
        @patch('app.services.stripe_service.stripe.checkout.Session.retrieve')
        async def test_get_session_stripe_error(self, mock_retrieve, stripe_service):
            """Test session retrieval with Stripe error."""
            mock_retrieve.side_effect = stripe.StripeError("Session not found")

            result = await stripe_service.get_session("cs_invalid")

            assert result["success"] is False
            assert "Session not found" in result["error"]

    class TestWebhookHandling:
        """Test webhook event handling."""

        def test_handle_webhook_event_checkout_completed(
            self, stripe_service, webhook_event_data
        ):
            """Test handling checkout.session.completed webhook."""
            with patch.object(stripe_service, '_handle_checkout_completed') as mock_handler:
                mock_handler.return_value = {"success": True, "message": "Subscription activated"}

                result = stripe_service.handle_webhook_event(webhook_event_data)

                mock_handler.assert_called_once_with(webhook_event_data["data"]["object"])
                assert result["success"] is True

        def test_handle_webhook_event_payment_succeeded(self, stripe_service):
            """Test handling invoice.payment_succeeded webhook."""
            event_data = {
                "type": "invoice.payment_succeeded",
                "data": {"object": {"id": "in_test123"}}
            }

            with patch.object(stripe_service, '_handle_payment_succeeded') as mock_handler:
                mock_handler.return_value = {"success": True, "message": "Payment processed"}

                result = stripe_service.handle_webhook_event(event_data)

                mock_handler.assert_called_once()
                assert result["success"] is True

        def test_handle_webhook_event_unhandled_type(self, stripe_service):
            """Test handling unhandled webhook event type."""
            event_data = {
                "type": "some.unknown.event",
                "data": {"object": {}}
            }

            result = stripe_service.handle_webhook_event(event_data)

            assert result["success"] is True
            assert "ignored" in result["message"]

        def test_handle_webhook_event_exception(self, stripe_service):
            """Test webhook handling with exception."""
            invalid_event = {"invalid": "structure"}

            result = stripe_service.handle_webhook_event(invalid_event)

            assert result["success"] is False
            assert "error" in result

    class TestCheckoutCompletedHandler:
        """Test _handle_checkout_completed webhook handler."""

        def test_handle_checkout_completed_new_subscription(self, stripe_service, db_session):
            """Test handling checkout completion for new subscription."""
            organization_id = uuid4()
            session_data = {
                "metadata": {
                    "organization_id": str(organization_id),
                    "plan_type": "growth"
                },
                "customer": "cus_test123",
                "subscription": "sub_test123"
            }

            # Mock no existing subscription
            db_session.query.return_value.filter.return_value.first.return_value = None

            result = stripe_service._handle_checkout_completed(session_data)

            # Verify new subscription creation
            db_session.add.assert_called_once()
            db_session.commit.assert_called_once()

            # Check created subscription
            created_subscription = db_session.add.call_args[0][0]
            assert created_subscription.organization_id == organization_id
            assert created_subscription.plan_type == PlanType.GROWTH
            assert created_subscription.status == SubscriptionStatus.ACTIVE
            assert created_subscription.stripe_customer_id == "cus_test123"
            assert created_subscription.stripe_subscription_id == "sub_test123"

            assert result["success"] is True

        def test_handle_checkout_completed_existing_subscription(self, stripe_service, db_session):
            """Test handling checkout completion for existing subscription."""
            organization_id = uuid4()
            session_data = {
                "metadata": {
                    "organization_id": str(organization_id),
                    "plan_type": "scale"
                },
                "customer": "cus_test123",
                "subscription": "sub_test123"
            }

            # Mock existing subscription
            existing_subscription = Mock(spec=Subscription)
            db_session.query.return_value.filter.return_value.first.return_value = existing_subscription

            result = stripe_service._handle_checkout_completed(session_data)

            # Verify subscription update
            assert existing_subscription.plan_type == PlanType.SCALE
            assert existing_subscription.status == SubscriptionStatus.ACTIVE
            assert existing_subscription.stripe_customer_id == "cus_test123"
            assert existing_subscription.stripe_subscription_id == "sub_test123"

            db_session.commit.assert_called_once()
            assert result["success"] is True

        def test_handle_checkout_completed_missing_organization_id(self, stripe_service):
            """Test handling checkout completion without organization ID."""
            session_data = {"metadata": {}}

            with pytest.raises(ValueError, match="Missing organization_id"):
                stripe_service._handle_checkout_completed(session_data)

        def test_handle_checkout_completed_no_db_session(self, stripe_service_no_db):
            """Test handling checkout completion without database session."""
            session_data = {
                "metadata": {"organization_id": str(uuid4()), "plan_type": "starter"}
            }

            with pytest.raises(ValueError, match="database session"):
                stripe_service_no_db._handle_checkout_completed(session_data)

        def test_handle_checkout_completed_exception_rollback(self, stripe_service, db_session):
            """Test checkout completion handling with exception and rollback."""
            organization_id = uuid4()
            session_data = {
                "metadata": {
                    "organization_id": str(organization_id),
                    "plan_type": "invalid_plan"  # Will cause enum error
                }
            }

            db_session.query.return_value.filter.return_value.first.return_value = None
            db_session.add.side_effect = ValueError("Invalid enum value")

            with pytest.raises(ValueError):
                stripe_service._handle_checkout_completed(session_data)

            db_session.rollback.assert_called_once()

    class TestGetPlans:
        """Test get_plans method."""

        def test_get_plans_returns_all_plans(self, stripe_service):
            """Test that get_plans returns all configured plans."""
            plans = stripe_service.get_plans()

            assert len(plans) == 3

            # Check that all plans have required structure
            for plan in plans:
                assert "id" in plan
                assert "name" in plan
                assert "price" in plan
                assert "currency" in plan
                assert "features" in plan
                assert "stripe_price_id" in plan

            # Check specific plans exist
            plan_ids = [plan["id"] for plan in plans]
            assert "starter" in plan_ids
            assert "growth" in plan_ids
            assert "scale" in plan_ids

        def test_get_plans_structure(self, stripe_service):
            """Test detailed structure of returned plans."""
            plans = stripe_service.get_plans()
            starter_plan = next(p for p in plans if p["id"] == "starter")

            assert starter_plan["price"] == 99.00
            assert starter_plan["currency"] == "eur"
            assert starter_plan["features"]["leads_per_month"] == 500
            assert starter_plan["features"]["users"] == 2

    class TestValidateWebhookSignature:
        """Test webhook signature validation."""

        @patch('app.services.stripe_service.stripe.Webhook.construct_event')
        @patch('app.services.stripe_service.settings')
        def test_validate_webhook_signature_success(
            self, mock_settings, mock_construct, stripe_service
        ):
            """Test successful webhook signature validation."""
            mock_settings.STRIPE_WEBHOOK_SECRET = "whsec_test123"
            mock_construct.return_value = {"type": "test"}

            payload = b'{"test": "data"}'
            signature = "test_signature"

            result = stripe_service.validate_webhook_signature(payload, signature)

            mock_construct.assert_called_once_with(
                payload, signature, "whsec_test123"
            )
            assert result is True

        @patch('app.services.stripe_service.stripe.Webhook.construct_event')
        def test_validate_webhook_signature_invalid_signature(
            self, mock_construct, stripe_service
        ):
            """Test webhook signature validation with invalid signature."""
            mock_construct.side_effect = stripe.SignatureVerificationError(
                "Invalid signature", "sig_header"
            )

            result = stripe_service.validate_webhook_signature(b'{"test": "data"}', "invalid")

            assert result is False

        @patch('app.services.stripe_service.stripe.Webhook.construct_event')
        def test_validate_webhook_signature_invalid_payload(
            self, mock_construct, stripe_service
        ):
            """Test webhook signature validation with invalid payload."""
            mock_construct.side_effect = ValueError("Invalid JSON")

            result = stripe_service.validate_webhook_signature(b'invalid json', "signature")

            assert result is False

    class TestPaymentHandlers:
        """Test payment webhook handlers."""

        def test_handle_payment_succeeded(self, stripe_service):
            """Test payment succeeded handler."""
            invoice_data = {"id": "in_test123", "amount_paid": 9900}

            result = stripe_service._handle_payment_succeeded(invoice_data)

            assert result["success"] is True
            assert "Payment processed" in result["message"]

        def test_handle_payment_failed(self, stripe_service):
            """Test payment failed handler."""
            invoice_data = {"id": "in_test123", "amount_due": 9900}

            result = stripe_service._handle_payment_failed(invoice_data)

            assert result["success"] is True
            assert "Payment failure processed" in result["message"]

        def test_handle_subscription_updated(self, stripe_service):
            """Test subscription updated handler."""
            subscription_data = {"id": "sub_test123", "status": "active"}

            result = stripe_service._handle_subscription_updated(subscription_data)

            assert result["success"] is True
            assert "Subscription updated" in result["message"]

        def test_handle_subscription_cancelled(self, stripe_service):
            """Test subscription cancelled handler."""
            subscription_data = {"id": "sub_test123", "status": "canceled"}

            result = stripe_service._handle_subscription_cancelled(subscription_data)

            assert result["success"] is True
            assert "Subscription cancelled" in result["message"]