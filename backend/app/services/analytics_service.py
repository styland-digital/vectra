"""Analytics service for tracking business KPIs and user events."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from sqlalchemy.dialects.postgresql import JSON

from app.core.logging import get_logger
from app.db.models.user import User
from app.db.models.organization import Organization
from app.db.models.campaign import Campaign, CampaignStatus
from app.db.models.lead import Lead
from app.db.models.email import Email, EmailStatus
from app.db.models.subscription import Subscription, SubscriptionStatus

logger = get_logger(__name__)


class AnalyticsEvent:
    """Standard analytics events for tracking."""

    # User Events
    USER_SIGNUP = "user_signup"
    USER_LOGIN = "user_login"
    USER_INVITE_SENT = "user_invite_sent"
    USER_INVITE_ACCEPTED = "user_invite_accepted"

    # Campaign Events
    CAMPAIGN_CREATED = "campaign_created"
    CAMPAIGN_STARTED = "campaign_started"
    CAMPAIGN_PAUSED = "campaign_paused"
    CAMPAIGN_COMPLETED = "campaign_completed"

    # Lead Events
    LEADS_IMPORTED = "leads_imported"
    LEAD_ENRICHED = "lead_enriched"
    LEAD_BANT_SCORED = "lead_bant_scored"
    LEAD_QUALIFIED = "lead_qualified"

    # Email Events
    EMAIL_GENERATED = "email_generated"
    EMAIL_APPROVED = "email_approved"
    EMAIL_SENT = "email_sent"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    EMAIL_REPLIED = "email_replied"

    # Meeting Events
    MEETING_SCHEDULED = "meeting_scheduled"
    MEETING_COMPLETED = "meeting_completed"
    MEETING_NO_SHOW = "meeting_no_show"

    # Billing Events
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_UPGRADED = "subscription_upgraded"
    SUBSCRIPTION_DOWNGRADED = "subscription_downgraded"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    PAYMENT_SUCCEEDED = "payment_succeeded"
    PAYMENT_FAILED = "payment_failed"


class AnalyticsService:
    """Service for tracking analytics events and computing business KPIs."""

    def __init__(self, db: Session):
        self.db = db

    async def track_event(
        self,
        organization_id: UUID,
        event_type: str,
        user_id: Optional[UUID] = None,
        properties: Optional[Dict[str, Any]] = None,
        value: Optional[float] = None
    ) -> bool:
        """Track an analytics event."""
        try:
            # For now, we'll log events. Later, we can store in a dedicated analytics table
            logger.info(
                f"Analytics Event",
                extra={
                    "organization_id": str(organization_id),
                    "event_type": event_type,
                    "user_id": str(user_id) if user_id else None,
                    "properties": properties or {},
                    "value": value,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            return True

        except Exception as e:
            logger.error(f"Failed to track analytics event: {e}", exc_info=True)
            return False

    async def get_revenue_metrics(self, organization_id: Optional[UUID] = None) -> Dict[str, Any]:
        """Get revenue-related KPIs."""
        try:
            # Base query for subscriptions
            query = self.db.query(Subscription)

            if organization_id:
                query = query.filter(Subscription.organization_id == organization_id)

            # Get active subscriptions
            active_subscriptions = query.filter(
                Subscription.status == SubscriptionStatus.ACTIVE
            ).all()

            # Calculate metrics
            mrr = sum(sub.amount / 100 for sub in active_subscriptions)  # Convert from cents

            # Plan distribution
            plan_distribution = {}
            for subscription in active_subscriptions:
                plan = subscription.plan_type
                plan_distribution[plan] = plan_distribution.get(plan, 0) + 1

            # Total customers
            total_customers = len(active_subscriptions)

            return {
                "mrr": mrr,
                "total_customers": total_customers,
                "plan_distribution": plan_distribution,
                "average_revenue_per_customer": mrr / total_customers if total_customers > 0 else 0
            }

        except Exception as e:
            logger.error(f"Failed to get revenue metrics: {e}", exc_info=True)
            return {}

    async def get_usage_metrics(self, organization_id: UUID, days: int = 30) -> Dict[str, Any]:
        """Get usage-related KPIs for an organization."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # Campaigns metrics
            campaigns_query = self.db.query(Campaign).filter(
                Campaign.organization_id == organization_id,
                Campaign.created_at >= start_date
            )

            campaigns_created = campaigns_query.count()
            campaigns_active = campaigns_query.filter(
                Campaign.status == CampaignStatus.ACTIVE
            ).count()

            # Leads metrics
            leads_query = self.db.query(Lead).join(
                Campaign, Lead.campaign_id == Campaign.id
            ).filter(
                Campaign.organization_id == organization_id,
                Lead.created_at >= start_date
            )

            leads_processed = leads_query.count()
            leads_qualified = leads_query.filter(
                Lead.bant_score >= 60
            ).count()

            # BANT score distribution
            bant_scores = [lead.bant_score for lead in leads_query.all() if lead.bant_score is not None]
            bant_average = sum(bant_scores) / len(bant_scores) if bant_scores else 0

            # Email metrics — join directly via campaign_id to avoid ambiguous multi-hop
            emails_query = self.db.query(Email).join(
                Campaign, Email.campaign_id == Campaign.id
            ).filter(
                Campaign.organization_id == organization_id,
                Email.created_at >= start_date
            )

            emails_sent = emails_query.filter(Email.status == EmailStatus.SENT).count()
            emails_opened = emails_query.filter(Email.opened_at.isnot(None)).count()
            emails_clicked = emails_query.filter(Email.clicked_at.isnot(None)).count()

            # Calculate rates
            open_rate = (emails_opened / emails_sent * 100) if emails_sent > 0 else 0
            click_rate = (emails_clicked / emails_sent * 100) if emails_sent > 0 else 0
            qualification_rate = (leads_qualified / leads_processed * 100) if leads_processed > 0 else 0

            return {
                "campaigns_created": campaigns_created,
                "campaigns_active": campaigns_active,
                "leads_processed": leads_processed,
                "leads_qualified": leads_qualified,
                "qualification_rate": round(qualification_rate, 2),
                "emails_sent": emails_sent,
                "emails_opened": emails_opened,
                "emails_clicked": emails_clicked,
                "email_open_rate": round(open_rate, 2),
                "email_click_rate": round(click_rate, 2),
                "bant_average_score": round(bant_average, 2),
                "period_days": days
            }

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to get usage metrics: {e}", exc_info=True)
            return {
                "campaigns_created": 0, "campaigns_active": 0,
                "leads_processed": 0, "leads_qualified": 0,
                "qualification_rate": 0.0, "emails_sent": 0,
                "emails_opened": 0, "emails_clicked": 0,
                "email_open_rate": 0.0, "email_click_rate": 0.0,
                "bant_average_score": 0.0, "period_days": days
            }

    async def get_user_engagement_metrics(self, organization_id: UUID, days: int = 30) -> Dict[str, Any]:
        """Get user engagement KPIs for an organization."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            users = self.db.query(User).filter(
                User.organization_id == organization_id
            ).all()

            total_users = len(users)

            # Active users = users who created at least one campaign in the period
            active_user_rows = self.db.query(Campaign.created_by).filter(
                Campaign.organization_id == organization_id,
                Campaign.created_at >= start_date,
                Campaign.created_by.isnot(None)
            ).distinct().all()
            active_users = len(active_user_rows)

            role_distribution = {}
            for user in users:
                role = user.role.value if user.role else "unknown"
                role_distribution[role] = role_distribution.get(role, 0) + 1

            return {
                "total_users": total_users,
                "active_users": active_users,
                "user_activity_rate": round((active_users / total_users * 100) if total_users > 0 else 0, 2),
                "role_distribution": role_distribution,
                "period_days": days
            }

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to get user engagement metrics: {e}", exc_info=True)
            return {
                "total_users": 0,
                "active_users": 0,
                "user_activity_rate": 0.0,
                "role_distribution": {},
                "period_days": days
            }

    async def get_ai_agent_metrics(self, organization_id: UUID, days: int = 30) -> Dict[str, Any]:
        """Get AI agent performance KPIs."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # Get campaigns with agent runs
            campaigns = self.db.query(Campaign).filter(
                Campaign.organization_id == organization_id,
                Campaign.created_at >= start_date
            ).all()

            total_agent_runs = 0
            successful_runs = 0
            prospector_runs = 0
            bant_runs = 0
            scheduler_runs = 0

            for campaign in campaigns:
                # Count agent runs based on campaign leads and emails
                leads_count = self.db.query(Lead).filter(
                    Lead.campaign_id == campaign.id
                ).count()

                emails_count = self.db.query(Email).filter(
                    Email.campaign_id == campaign.id
                ).count()

                if leads_count > 0:
                    prospector_runs += 1
                    total_agent_runs += 1
                    if leads_count > 0:  # Consider successful if leads were found
                        successful_runs += 1

                # BANT runs = leads with BANT scores
                bant_scored_leads = self.db.query(Lead).filter(
                    Lead.campaign_id == campaign.id,
                    Lead.bant_score.isnot(None)
                ).count()

                if bant_scored_leads > 0:
                    bant_runs += 1
                    total_agent_runs += 1
                    successful_runs += 1

                # Scheduler runs = emails generated
                if emails_count > 0:
                    scheduler_runs += 1
                    total_agent_runs += 1
                    successful_runs += 1

            success_rate = (successful_runs / total_agent_runs * 100) if total_agent_runs > 0 else 0

            return {
                "total_agent_runs": total_agent_runs,
                "successful_runs": successful_runs,
                "success_rate": round(success_rate, 2),
                "prospector_runs": prospector_runs,
                "bant_runs": bant_runs,
                "scheduler_runs": scheduler_runs,
                "period_days": days
            }

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to get AI agent metrics: {e}", exc_info=True)
            return {
                "total_agent_runs": 0, "successful_runs": 0,
                "success_rate": 0.0, "prospector_runs": 0,
                "bant_runs": 0, "scheduler_runs": 0, "period_days": days
            }

    async def get_dashboard_overview(self, organization_id: UUID) -> Dict[str, Any]:
        """Get comprehensive overview for dashboard."""
        try:
            metrics_30d = await self.get_usage_metrics(organization_id, 30)
            metrics_prev = await self.get_usage_metrics(organization_id, 60)
            engagement = await self.get_user_engagement_metrics(organization_id)
            ai_metrics = await self.get_ai_agent_metrics(organization_id)

            # Current period = last 30d, previous period = 30d before that
            leads_current = metrics_30d.get("leads_processed", 0)
            leads_previous = max(metrics_prev.get("leads_processed", 0) - leads_current, 0)
            leads_change = round(
                ((leads_current - leads_previous) / leads_previous * 100) if leads_previous > 0 else 0,
                2
            )

            emails_current = metrics_30d.get("emails_sent", 0)
            emails_previous = max(metrics_prev.get("emails_sent", 0) - emails_current, 0)
            emails_change = round(
                ((emails_current - emails_previous) / emails_previous * 100) if emails_previous > 0 else 0,
                2
            )

            # Total qualified leads all-time for the org
            total_qualified = self.db.query(Lead).join(
                Campaign, Lead.campaign_id == Campaign.id
            ).filter(
                Campaign.organization_id == organization_id,
                Lead.bant_score >= 60
            ).count()

            # Active campaigns
            active_campaigns = self.db.query(Campaign).filter(
                Campaign.organization_id == organization_id,
                Campaign.status == CampaignStatus.ACTIVE
            ).count()

            # Subscription info
            subscription = self.db.query(Subscription).filter(
                Subscription.organization_id == organization_id,
                Subscription.status == SubscriptionStatus.ACTIVE
            ).first()

            plan_limits = {"starter": 500, "growth": 1000, "scale": 5000}
            plan_name = subscription.plan_type if subscription else "starter"
            sub_status = subscription.status.value if subscription else "active"
            leads_limit = plan_limits.get(plan_name, 500)
            leads_used = self.db.query(Lead).join(
                Campaign, Lead.campaign_id == Campaign.id
            ).filter(
                Campaign.organization_id == organization_id
            ).count()

            return {
                "overview": {
                    "active_campaigns": active_campaigns,
                    "qualified_leads": total_qualified,
                    "emails_sent": metrics_30d.get("emails_sent", 0),
                    "ai_success_rate": ai_metrics.get("success_rate", 0),
                },
                "growth": {
                    "leads_current": leads_current,
                    "leads_previous": leads_previous,
                    "leads_change": leads_change,
                    "emails_current": emails_current,
                    "emails_previous": emails_previous,
                    "emails_change": emails_change,
                },
                "team": engagement,
                "ai_agents": ai_metrics,
                "subscription": {
                    "plan": plan_name,
                    "status": sub_status,
                    "leads_used": leads_used,
                    "leads_limit": leads_limit,
                },
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get dashboard overview: {e}", exc_info=True)
            return {}

    async def get_platform_overview(self) -> Dict[str, Any]:
        """Get platform-wide metrics for admin dashboard."""
        try:
            # Total organizations
            total_orgs = self.db.query(Organization).count()

            # Active subscriptions
            active_subscriptions = self.db.query(Subscription).filter(
                Subscription.status == SubscriptionStatus.ACTIVE
            ).count()

            # Revenue metrics
            revenue_metrics = await self.get_revenue_metrics()

            # Usage aggregates
            total_campaigns = self.db.query(Campaign).count()
            total_leads = self.db.query(Lead).count()
            total_emails = self.db.query(Email).count()

            # Recent activity (last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)

            new_orgs_week = self.db.query(Organization).filter(
                Organization.created_at >= week_ago
            ).count()

            new_campaigns_week = self.db.query(Campaign).filter(
                Campaign.created_at >= week_ago
            ).count()

            return {
                "platform": {
                    "total_organizations": total_orgs,
                    "active_subscriptions": active_subscriptions,
                    "total_campaigns": total_campaigns,
                    "total_leads": total_leads,
                    "total_emails": total_emails
                },
                "revenue": revenue_metrics,
                "recent_activity": {
                    "new_organizations_7d": new_orgs_week,
                    "new_campaigns_7d": new_campaigns_week
                },
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get platform overview: {e}", exc_info=True)
            return {}