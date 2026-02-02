"""Unit tests for AnalyticsService.

Tests for business KPI calculations, event tracking, multi-tenant isolation,
and platform admin metrics.
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock, MagicMock, AsyncMock, patch
from uuid import uuid4, UUID

from app.services.analytics_service import AnalyticsService, AnalyticsEvent
from app.db.models.user import User, UserRole
from app.db.models.organization import Organization
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead
from app.db.models.email import Email, EmailStatus
from app.db.models.subscription import Subscription


class TestAnalyticsEvent:
    """Test analytics event constants."""

    def test_event_constants_exist(self):
        """Test that all required analytics events are defined."""
        # User events
        assert AnalyticsEvent.USER_SIGNUP == "user_signup"
        assert AnalyticsEvent.USER_LOGIN == "user_login"
        assert AnalyticsEvent.USER_INVITE_SENT == "user_invite_sent"
        assert AnalyticsEvent.USER_INVITE_ACCEPTED == "user_invite_accepted"

        # Campaign events
        assert AnalyticsEvent.CAMPAIGN_CREATED == "campaign_created"
        assert AnalyticsEvent.CAMPAIGN_STARTED == "campaign_started"
        assert AnalyticsEvent.CAMPAIGN_PAUSED == "campaign_paused"
        assert AnalyticsEvent.CAMPAIGN_COMPLETED == "campaign_completed"

        # Lead events
        assert AnalyticsEvent.LEADS_IMPORTED == "leads_imported"
        assert AnalyticsEvent.LEAD_ENRICHED == "lead_enriched"
        assert AnalyticsEvent.LEAD_BANT_SCORED == "lead_bant_scored"
        assert AnalyticsEvent.LEAD_QUALIFIED == "lead_qualified"

        # Email events
        assert AnalyticsEvent.EMAIL_GENERATED == "email_generated"
        assert AnalyticsEvent.EMAIL_APPROVED == "email_approved"
        assert AnalyticsEvent.EMAIL_SENT == "email_sent"
        assert AnalyticsEvent.EMAIL_OPENED == "email_opened"
        assert AnalyticsEvent.EMAIL_CLICKED == "email_clicked"
        assert AnalyticsEvent.EMAIL_REPLIED == "email_replied"

        # Meeting events
        assert AnalyticsEvent.MEETING_SCHEDULED == "meeting_scheduled"
        assert AnalyticsEvent.MEETING_COMPLETED == "meeting_completed"
        assert AnalyticsEvent.MEETING_NO_SHOW == "meeting_no_show"

        # Billing events
        assert AnalyticsEvent.SUBSCRIPTION_CREATED == "subscription_created"
        assert AnalyticsEvent.SUBSCRIPTION_UPGRADED == "subscription_upgraded"
        assert AnalyticsEvent.SUBSCRIPTION_DOWNGRADED == "subscription_downgraded"
        assert AnalyticsEvent.SUBSCRIPTION_CANCELLED == "subscription_cancelled"
        assert AnalyticsEvent.PAYMENT_SUCCEEDED == "payment_succeeded"
        assert AnalyticsEvent.PAYMENT_FAILED == "payment_failed"


class TestAnalyticsService:
    """Test AnalyticsService methods."""

    @pytest.fixture
    def db_session(self):
        """Mock database session."""
        return Mock()

    @pytest.fixture
    def analytics_service(self, db_session):
        """AnalyticsService instance with mocked DB."""
        return AnalyticsService(db=db_session)

    @pytest.fixture
    def organization_id(self):
        """Test organization ID."""
        return uuid4()

    @pytest.fixture
    def user_id(self):
        """Test user ID."""
        return uuid4()

    @pytest.fixture
    def sample_subscriptions(self, organization_id):
        """Sample subscription data for testing."""
        return [
            Mock(
                organization_id=organization_id,
                status="active",
                plan_type="starter",
                amount=9900,  # €99.00 in cents
            ),
            Mock(
                organization_id=organization_id,
                status="active",
                plan_type="growth",
                amount=29900,  # €299.00 in cents
            ),
            Mock(
                organization_id=uuid4(),  # Different org
                status="active",
                plan_type="scale",
                amount=79900,  # €799.00 in cents
            )
        ]

    @pytest.fixture
    def sample_campaigns(self, organization_id):
        """Sample campaign data for testing."""
        now = datetime.utcnow()
        return [
            Mock(
                id=uuid4(),
                organization_id=organization_id,
                status="active",
                created_at=now - timedelta(days=10),
                created_by=uuid4()
            ),
            Mock(
                id=uuid4(),
                organization_id=organization_id,
                status="completed",
                created_at=now - timedelta(days=20),
                created_by=uuid4()
            )
        ]

    @pytest.fixture
    def sample_leads(self, sample_campaigns):
        """Sample lead data for testing."""
        return [
            Mock(
                campaign_id=sample_campaigns[0].id,
                bant_score=75,
                created_at=datetime.utcnow() - timedelta(days=5)
            ),
            Mock(
                campaign_id=sample_campaigns[0].id,
                bant_score=45,
                created_at=datetime.utcnow() - timedelta(days=8)
            ),
            Mock(
                campaign_id=sample_campaigns[1].id,
                bant_score=85,
                created_at=datetime.utcnow() - timedelta(days=15)
            )
        ]

    @pytest.fixture
    def sample_emails(self, sample_leads):
        """Sample email data for testing."""
        now = datetime.utcnow()
        return [
            Mock(
                lead_id=sample_leads[0].id,
                status="sent",
                opened_at=now - timedelta(days=3),
                clicked_at=now - timedelta(days=3),
                created_at=now - timedelta(days=4)
            ),
            Mock(
                lead_id=sample_leads[0].id,
                status="sent",
                opened_at=now - timedelta(days=2),
                clicked_at=None,
                created_at=now - timedelta(days=3)
            ),
            Mock(
                lead_id=sample_leads[1].id,
                status="sent",
                opened_at=None,
                clicked_at=None,
                created_at=now - timedelta(days=1)
            )
        ]

    @pytest.fixture
    def sample_users(self, organization_id):
        """Sample user data for testing."""
        return [
            Mock(
                id=uuid4(),
                organization_id=organization_id,
                role=Mock(value="admin")
            ),
            Mock(
                id=uuid4(),
                organization_id=organization_id,
                role=Mock(value="operator")
            ),
            Mock(
                id=uuid4(),
                organization_id=organization_id,
                role=Mock(value="viewer")
            )
        ]

    class TestTrackEvent:
        """Test event tracking functionality."""

        @pytest.mark.asyncio
        @patch('app.services.analytics_service.logger')
        async def test_track_event_success(self, mock_logger, analytics_service, organization_id, user_id):
            """Test successful event tracking."""
            properties = {"campaign_id": str(uuid4()), "leads_count": 50}
            value = 150.0

            result = await analytics_service.track_event(
                organization_id=organization_id,
                event_type=AnalyticsEvent.LEADS_IMPORTED,
                user_id=user_id,
                properties=properties,
                value=value
            )

            assert result is True
            mock_logger.info.assert_called_once()

            # Check log call arguments
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "Analytics Event"
            extra = call_args[1]["extra"]
            assert extra["organization_id"] == str(organization_id)
            assert extra["event_type"] == AnalyticsEvent.LEADS_IMPORTED
            assert extra["user_id"] == str(user_id)
            assert extra["properties"] == properties
            assert extra["value"] == value
            assert "timestamp" in extra

        @pytest.mark.asyncio
        async def test_track_event_optional_params(self, analytics_service, organization_id):
            """Test event tracking with minimal parameters."""
            result = await analytics_service.track_event(
                organization_id=organization_id,
                event_type=AnalyticsEvent.USER_LOGIN
            )

            assert result is True

        @pytest.mark.asyncio
        @patch('app.services.analytics_service.logger')
        async def test_track_event_exception_handling(self, mock_logger, analytics_service, organization_id):
            """Test event tracking exception handling."""
            # Force an exception by making logger.info raise
            mock_logger.info.side_effect = Exception("Database error")

            result = await analytics_service.track_event(
                organization_id=organization_id,
                event_type=AnalyticsEvent.USER_SIGNUP
            )

            assert result is False
            mock_logger.error.assert_called_once()

    class TestRevenueMetrics:
        """Test revenue KPI calculations."""

        @pytest.mark.asyncio
        async def test_revenue_metrics_with_organization_filter(
            self, analytics_service, organization_id, sample_subscriptions
        ):
            """Test revenue metrics filtered by organization."""
            # Mock query chain
            query_mock = Mock()
            filter_mock = Mock()

            analytics_service.db.query.return_value = query_mock
            query_mock.filter.return_value = filter_mock
            filter_mock.filter.return_value.all.return_value = sample_subscriptions[:2]  # First 2 subs

            result = await analytics_service.get_revenue_metrics(organization_id)

            # Verify filtering
            analytics_service.db.query.assert_called_once_with(Subscription)
            query_mock.filter.assert_called_once()
            filter_mock.filter.assert_called_once()

            # Check metrics calculation
            expected_mrr = (9900 + 29900) / 100  # €398.00
            assert result["mrr"] == expected_mrr
            assert result["total_customers"] == 2
            assert result["plan_distribution"] == {"starter": 1, "growth": 1}
            assert result["average_revenue_per_customer"] == expected_mrr / 2

        @pytest.mark.asyncio
        async def test_revenue_metrics_platform_wide(self, analytics_service, sample_subscriptions):
            """Test platform-wide revenue metrics (no org filter)."""
            query_mock = Mock()
            filter_mock = Mock()

            analytics_service.db.query.return_value = query_mock
            query_mock.filter = Mock(return_value=filter_mock)
            filter_mock.all.return_value = sample_subscriptions

            result = await analytics_service.get_revenue_metrics(organization_id=None)

            # Should not filter by organization
            query_mock.filter.assert_called_once()  # Only status filter

            # Check metrics with all subscriptions
            expected_mrr = (9900 + 29900 + 79900) / 100  # €1197.00
            assert result["mrr"] == expected_mrr
            assert result["total_customers"] == 3

        @pytest.mark.asyncio
        async def test_revenue_metrics_no_active_subscriptions(self, analytics_service, organization_id):
            """Test revenue metrics with no active subscriptions."""
            query_mock = Mock()
            filter_mock = Mock()

            analytics_service.db.query.return_value = query_mock
            query_mock.filter.return_value = filter_mock
            filter_mock.filter.return_value.all.return_value = []

            result = await analytics_service.get_revenue_metrics(organization_id)

            assert result["mrr"] == 0
            assert result["total_customers"] == 0
            assert result["plan_distribution"] == {}
            assert result["average_revenue_per_customer"] == 0

        @pytest.mark.asyncio
        @patch('app.services.analytics_service.logger')
        async def test_revenue_metrics_exception_handling(self, mock_logger, analytics_service, organization_id):
            """Test revenue metrics exception handling."""
            analytics_service.db.query.side_effect = Exception("Database error")

            result = await analytics_service.get_revenue_metrics(organization_id)

            assert result == {}
            mock_logger.error.assert_called_once()

    class TestUsageMetrics:
        """Test usage KPI calculations."""

        @pytest.mark.asyncio
        async def test_usage_metrics_complete_calculation(
            self, analytics_service, organization_id, sample_campaigns, sample_leads, sample_emails
        ):
            """Test complete usage metrics calculation."""
            # Mock complex query chain for campaigns
            campaign_query = Mock()
            campaign_query.count.return_value = 2  # Total campaigns
            campaign_filter = Mock()
            campaign_filter.count.return_value = 1  # Active campaigns
            campaign_query.filter.return_value = campaign_filter

            # Mock complex query chain for leads
            leads_query = Mock()
            leads_query.count.return_value = 3  # Total leads
            leads_filter = Mock()
            leads_filter.count.return_value = 2  # Qualified leads (score >= 60)
            leads_query.filter.return_value = leads_filter
            leads_query.all.return_value = sample_leads

            # Mock complex query chain for emails
            emails_query = Mock()
            emails_sent_filter = Mock()
            emails_sent_filter.count.return_value = 3
            emails_opened_filter = Mock()
            emails_opened_filter.count.return_value = 2
            emails_clicked_filter = Mock()
            emails_clicked_filter.count.return_value = 1

            # Configure query behavior
            def query_side_effect(model):
                if model == Campaign:
                    return campaign_query
                elif model == Lead:
                    return leads_query
                elif model == Email:
                    return emails_query

            analytics_service.db.query.side_effect = query_side_effect

            # Configure filter chain for emails
            emails_query.join.return_value.join.return_value.filter.return_value = emails_query
            emails_query.filter.side_effect = [
                emails_sent_filter,  # sent emails
                emails_opened_filter,  # opened emails
                emails_clicked_filter  # clicked emails
            ]

            result = await analytics_service.get_usage_metrics(organization_id, days=30)

            # Verify metrics
            assert result["campaigns_created"] == 2
            assert result["campaigns_active"] == 1
            assert result["leads_processed"] == 3
            assert result["leads_qualified"] == 2
            assert result["qualification_rate"] == 66.67  # 2/3 * 100
            assert result["emails_sent"] == 3
            assert result["emails_opened"] == 2
            assert result["emails_clicked"] == 1
            assert result["email_open_rate"] == 66.67  # 2/3 * 100
            assert result["email_click_rate"] == 33.33  # 1/3 * 100
            assert result["period_days"] == 30

        @pytest.mark.asyncio
        async def test_usage_metrics_bant_average_calculation(
            self, analytics_service, organization_id, sample_leads
        ):
            """Test BANT score average calculation."""
            # Mock leads with BANT scores: 75, 45, 85
            leads_query = Mock()
            leads_query.all.return_value = sample_leads
            leads_query.count.return_value = len(sample_leads)

            campaign_query = Mock()
            campaign_query.count.return_value = 2
            campaign_query.filter.return_value.count.return_value = 1

            emails_query = Mock()
            emails_query.join.return_value.join.return_value.filter.return_value = emails_query
            emails_query.filter.return_value.count.return_value = 0

            def query_side_effect(model):
                if model == Campaign:
                    return campaign_query
                elif model == Lead:
                    return leads_query
                elif model == Email:
                    return emails_query

            analytics_service.db.query.side_effect = query_side_effect

            result = await analytics_service.get_usage_metrics(organization_id)

            # BANT average should be (75 + 45 + 85) / 3 = 68.33
            assert result["bant_average_score"] == 68.33

        @pytest.mark.asyncio
        async def test_usage_metrics_zero_division_handling(self, analytics_service, organization_id):
            """Test usage metrics with zero values to avoid division by zero."""
            # Mock all counts as zero
            empty_query = Mock()
            empty_query.count.return_value = 0
            empty_query.all.return_value = []
            empty_query.filter.return_value = empty_query
            empty_query.join.return_value.join.return_value.filter.return_value = empty_query

            analytics_service.db.query.return_value = empty_query

            result = await analytics_service.get_usage_metrics(organization_id)

            # All rates should be 0, not NaN or error
            assert result["qualification_rate"] == 0
            assert result["email_open_rate"] == 0
            assert result["email_click_rate"] == 0
            assert result["bant_average_score"] == 0

    class TestUserEngagementMetrics:
        """Test user engagement KPI calculations."""

        @pytest.mark.asyncio
        async def test_user_engagement_metrics_complete(
            self, analytics_service, organization_id, sample_users
        ):
            """Test complete user engagement metrics calculation."""
            # Mock users query
            users_query = Mock()
            users_query.filter.return_value.all.return_value = sample_users

            # Mock active users query (complex join)
            active_users_query = Mock()
            join_result = Mock()
            filter_result = Mock()
            distinct_result = Mock()

            active_users_query.filter.return_value = join_result
            join_result.join.return_value = filter_result
            filter_result.filter.return_value = distinct_result
            distinct_result.distinct.return_value.count.return_value = 2  # 2 active users

            def query_side_effect(model):
                if model == User:
                    return users_query if analytics_service.db.query.call_count == 1 else active_users_query

            analytics_service.db.query.side_effect = query_side_effect

            result = await analytics_service.get_user_engagement_metrics(organization_id)

            assert result["total_users"] == 3
            assert result["active_users"] == 2
            assert result["user_activity_rate"] == 66.67  # 2/3 * 100
            assert result["role_distribution"] == {
                "admin": 1,
                "operator": 1,
                "viewer": 1
            }
            assert result["period_days"] == 30

        @pytest.mark.asyncio
        async def test_user_engagement_metrics_no_users(self, analytics_service, organization_id):
            """Test user engagement metrics with no users."""
            empty_query = Mock()
            empty_query.filter.return_value.all.return_value = []
            empty_query.filter.return_value.join.return_value.filter.return_value.distinct.return_value.count.return_value = 0

            analytics_service.db.query.return_value = empty_query

            result = await analytics_service.get_user_engagement_metrics(organization_id)

            assert result["total_users"] == 0
            assert result["active_users"] == 0
            assert result["user_activity_rate"] == 0
            assert result["role_distribution"] == {}

    class TestAIAgentMetrics:
        """Test AI agent performance KPI calculations."""

        @pytest.mark.asyncio
        async def test_ai_agent_metrics_calculation(
            self, analytics_service, organization_id, sample_campaigns
        ):
            """Test AI agent metrics calculation based on campaign activities."""
            # Mock campaigns query
            campaigns_query = Mock()
            campaigns_query.filter.return_value.all.return_value = sample_campaigns

            # Mock leads and emails counts
            leads_query = Mock()
            emails_query = Mock()

            def query_side_effect(model):
                if model == Campaign:
                    return campaigns_query
                elif model == Lead:
                    return leads_query
                elif model == Email:
                    return emails_query

            analytics_service.db.query.side_effect = query_side_effect

            # Configure leads queries
            leads_query.filter.side_effect = [
                Mock(count=Mock(return_value=10)),  # Campaign 1 leads
                Mock(count=Mock(return_value=5)),   # Campaign 2 leads
                Mock(count=Mock(return_value=8)),   # Campaign 1 BANT scored
                Mock(count=Mock(return_value=3)),   # Campaign 2 BANT scored
            ]

            # Configure emails queries
            emails_query.join.return_value.filter.side_effect = [
                Mock(count=Mock(return_value=15)),  # Campaign 1 emails
                Mock(count=Mock(return_value=8)),   # Campaign 2 emails
            ]

            result = await analytics_service.get_ai_agent_metrics(organization_id)

            # Prospector runs: 2 (both campaigns had leads)
            # BANT runs: 2 (both campaigns had BANT scored leads)
            # Scheduler runs: 2 (both campaigns had emails)
            # Total: 6, Successful: 6
            assert result["prospector_runs"] == 2
            assert result["bant_runs"] == 2
            assert result["scheduler_runs"] == 2
            assert result["total_agent_runs"] == 6
            assert result["successful_runs"] == 6
            assert result["success_rate"] == 100.0

        @pytest.mark.asyncio
        async def test_ai_agent_metrics_no_activity(self, analytics_service, organization_id):
            """Test AI agent metrics with no campaign activity."""
            # Mock empty campaigns
            campaigns_query = Mock()
            campaigns_query.filter.return_value.all.return_value = []

            analytics_service.db.query.return_value = campaigns_query

            result = await analytics_service.get_ai_agent_metrics(organization_id)

            assert result["prospector_runs"] == 0
            assert result["bant_runs"] == 0
            assert result["scheduler_runs"] == 0
            assert result["total_agent_runs"] == 0
            assert result["successful_runs"] == 0
            assert result["success_rate"] == 0

    class TestDashboardOverview:
        """Test comprehensive dashboard overview."""

        @pytest.mark.asyncio
        async def test_dashboard_overview_integration(self, analytics_service, organization_id):
            """Test dashboard overview integrates multiple metrics."""
            # Mock subscription data
            subscription = Mock(
                plan_type="growth",
                status="active",
                current_period_end=datetime.utcnow() + timedelta(days=30)
            )

            sub_query = Mock()
            sub_query.filter.return_value.filter.return_value.first.return_value = subscription
            analytics_service.db.query.return_value = sub_query

            # Mock metric methods
            analytics_service.get_usage_metrics = AsyncMock(side_effect=[
                {
                    "campaigns_active": 5,
                    "leads_processed": 150,
                    "leads_qualified": 90,
                    "emails_sent": 200,
                    "qualification_rate": 60.0,
                    "email_open_rate": 35.5
                },
                {
                    "leads_processed": 40,
                    "emails_sent": 55
                }
            ])

            analytics_service.get_user_engagement_metrics = AsyncMock(return_value={
                "total_users": 8,
                "active_users": 6
            })

            analytics_service.get_ai_agent_metrics = AsyncMock(return_value={
                "success_rate": 95.5
            })

            result = await analytics_service.get_dashboard_overview(organization_id)

            # Verify overview section
            overview = result["overview"]
            assert overview["campaigns_active"] == 5
            assert overview["leads_processed_30d"] == 150
            assert overview["leads_qualified_30d"] == 90
            assert overview["emails_sent_30d"] == 200
            assert overview["qualification_rate"] == 60.0
            assert overview["email_open_rate"] == 35.5

            # Verify growth calculations
            growth = result["growth"]
            assert growth["leads_7d_vs_30d"]["current"] == 40
            assert growth["leads_7d_vs_30d"]["previous"] == 110  # 150 - 40
            assert growth["emails_7d_vs_30d"]["current"] == 55
            assert growth["emails_7d_vs_30d"]["previous"] == 145  # 200 - 55

            # Verify subscription info
            subscription_info = result["subscription"]
            assert subscription_info["plan_type"] == "growth"
            assert subscription_info["status"] == "active"
            assert "current_period_end" in subscription_info

            # Verify integration of other metrics
            assert "team" in result
            assert "ai_agents" in result
            assert "generated_at" in result

        @pytest.mark.asyncio
        async def test_dashboard_overview_no_subscription(self, analytics_service, organization_id):
            """Test dashboard overview with no active subscription."""
            # Mock no subscription
            sub_query = Mock()
            sub_query.filter.return_value.filter.return_value.first.return_value = None
            analytics_service.db.query.return_value = sub_query

            # Mock empty metrics
            analytics_service.get_usage_metrics = AsyncMock(return_value={})
            analytics_service.get_user_engagement_metrics = AsyncMock(return_value={})
            analytics_service.get_ai_agent_metrics = AsyncMock(return_value={})

            result = await analytics_service.get_dashboard_overview(organization_id)

            assert result["subscription"] is None

    class TestPlatformOverview:
        """Test platform-wide admin metrics."""

        @pytest.mark.asyncio
        async def test_platform_overview_complete(self, analytics_service):
            """Test complete platform overview for admin dashboard."""
            # Mock individual count queries
            def count_side_effect():
                counts = [5, 12, 25, 150, 500]  # orgs, subs, campaigns, leads, emails
                for count in counts:
                    yield count

            count_gen = count_side_effect()

            def mock_query(model):
                query_mock = Mock()
                if model == Organization:
                    if hasattr(mock_query, '_org_called'):
                        # Second call for recent orgs
                        query_mock.filter.return_value.count.return_value = 2
                    else:
                        # First call for total orgs
                        query_mock.count.return_value = 5
                        mock_query._org_called = True
                elif model == Subscription:
                    query_mock.filter.return_value.count.return_value = 12
                elif model == Campaign:
                    if hasattr(mock_query, '_campaign_called'):
                        # Second call for recent campaigns
                        query_mock.filter.return_value.count.return_value = 8
                    else:
                        # First call for total campaigns
                        query_mock.count.return_value = 25
                        mock_query._campaign_called = True
                elif model == Lead:
                    query_mock.count.return_value = 150
                elif model == Email:
                    query_mock.count.return_value = 500
                return query_mock

            analytics_service.db.query.side_effect = mock_query

            # Mock revenue metrics
            analytics_service.get_revenue_metrics = AsyncMock(return_value={
                "mrr": 5000.0,
                "total_customers": 12
            })

            result = await analytics_service.get_platform_overview()

            # Verify platform metrics
            platform = result["platform"]
            assert platform["total_organizations"] == 5
            assert platform["active_subscriptions"] == 12
            assert platform["total_campaigns"] == 25
            assert platform["total_leads"] == 150
            assert platform["total_emails"] == 500

            # Verify revenue metrics
            revenue = result["revenue"]
            assert revenue["mrr"] == 5000.0
            assert revenue["total_customers"] == 12

            # Verify recent activity
            recent = result["recent_activity"]
            assert recent["new_organizations_7d"] == 2
            assert recent["new_campaigns_7d"] == 8

            assert "generated_at" in result

    class TestErrorHandling:
        """Test error handling across all methods."""

        @pytest.mark.asyncio
        @patch('app.services.analytics_service.logger')
        async def test_all_methods_handle_exceptions(self, mock_logger, analytics_service, organization_id):
            """Test that all methods handle database exceptions gracefully."""
            # Force database exception
            analytics_service.db.query.side_effect = Exception("Database connection failed")

            # Test each method returns empty dict on exception
            methods_to_test = [
                analytics_service.get_revenue_metrics(organization_id),
                analytics_service.get_usage_metrics(organization_id),
                analytics_service.get_user_engagement_metrics(organization_id),
                analytics_service.get_ai_agent_metrics(organization_id),
                analytics_service.get_dashboard_overview(organization_id),
                analytics_service.get_platform_overview()
            ]

            results = []
            for method in methods_to_test:
                result = await method
                results.append(result)

            # All should return empty dicts
            assert all(result == {} for result in results)

            # Logger should have been called for each exception
            assert mock_logger.error.call_count == len(methods_to_test)