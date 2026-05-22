"""Analytics schema definitions for API documentation."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class AnalyticsEventTrack(BaseModel):
    """Schema for tracking analytics events."""
    event_type: str = Field(..., description="Type of event to track")
    properties: Optional[Dict[str, Any]] = Field(None, description="Event properties")
    value: Optional[float] = Field(None, description="Numeric value associated with event")

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "campaign_created",
                "properties": {
                    "campaign_type": "prospecting",
                    "target_count": 100
                },
                "value": 100.0
            }
        }


class UsageMetrics(BaseModel):
    """Usage metrics for an organization."""
    campaigns_created: int = Field(..., description="Number of campaigns created")
    campaigns_active: int = Field(..., description="Number of active campaigns")
    leads_processed: int = Field(..., description="Total leads processed")
    leads_qualified: int = Field(..., description="Number of qualified leads")
    qualification_rate: float = Field(..., description="Lead qualification rate percentage")
    emails_sent: int = Field(..., description="Number of emails sent")
    emails_opened: int = Field(..., description="Number of emails opened")
    emails_clicked: int = Field(..., description="Number of emails clicked")
    email_open_rate: float = Field(..., description="Email open rate percentage")
    email_click_rate: float = Field(..., description="Email click rate percentage")
    bant_average_score: float = Field(..., description="Average BANT score")
    period_days: int = Field(..., description="Period in days for metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "campaigns_created": 5,
                "campaigns_active": 3,
                "leads_processed": 1250,
                "leads_qualified": 287,
                "qualification_rate": 22.96,
                "emails_sent": 450,
                "emails_opened": 162,
                "emails_clicked": 23,
                "email_open_rate": 36.0,
                "email_click_rate": 5.11,
                "bant_average_score": 58.4,
                "period_days": 30
            }
        }


class EngagementMetrics(BaseModel):
    """User engagement metrics for an organization."""
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    user_activity_rate: float = Field(..., description="User activity rate percentage")
    role_distribution: Dict[str, int] = Field(..., description="Distribution of user roles")
    period_days: int = Field(..., description="Period in days for metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "total_users": 8,
                "active_users": 6,
                "user_activity_rate": 75.0,
                "role_distribution": {
                    "owner": 1,
                    "admin": 2,
                    "manager": 2,
                    "operator": 3
                },
                "period_days": 30
            }
        }


class AIAgentMetrics(BaseModel):
    """AI agent performance metrics."""
    total_agent_runs: int = Field(..., description="Total number of agent runs")
    successful_runs: int = Field(..., description="Number of successful runs")
    success_rate: float = Field(..., description="Agent success rate percentage")
    prospector_runs: int = Field(..., description="Number of prospector agent runs")
    bant_runs: int = Field(..., description="Number of BANT agent runs")
    scheduler_runs: int = Field(..., description="Number of scheduler agent runs")
    period_days: int = Field(..., description="Period in days for metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "total_agent_runs": 15,
                "successful_runs": 13,
                "success_rate": 86.67,
                "prospector_runs": 5,
                "bant_runs": 5,
                "scheduler_runs": 5,
                "period_days": 30
            }
        }


class OverviewMetrics(BaseModel):
    """Key overview metrics for dashboard."""
    active_campaigns: int = Field(..., description="Currently active campaigns")
    qualified_leads: int = Field(..., description="Total qualified leads (BANT >= 60)")
    emails_sent: int = Field(..., description="Emails sent in the period")
    ai_success_rate: float = Field(..., description="AI agent success rate percentage")


class GrowthMetrics(BaseModel):
    """Growth metrics comparing current period vs previous period."""
    leads_current: int = Field(..., description="Leads in current period")
    leads_previous: int = Field(..., description="Leads in previous period")
    leads_change: float = Field(..., description="Leads change percentage")
    emails_current: int = Field(..., description="Emails in current period")
    emails_previous: int = Field(..., description="Emails in previous period")
    emails_change: float = Field(..., description="Emails change percentage")


class SubscriptionInfo(BaseModel):
    """Subscription information."""
    plan: str = Field(..., description="Subscription plan name")
    status: str = Field(..., description="Subscription status")
    leads_used: int = Field(..., description="Leads consumed in current period")
    leads_limit: int = Field(..., description="Maximum leads allowed by plan")


class AnalyticsDashboard(BaseModel):
    """Complete dashboard analytics response."""
    overview: OverviewMetrics = Field(..., description="Key overview metrics")
    growth: GrowthMetrics = Field(..., description="Growth metrics vs previous period")
    team: EngagementMetrics = Field(..., description="Team engagement metrics")
    ai_agents: AIAgentMetrics = Field(..., description="AI agent metrics")
    subscription: SubscriptionInfo = Field(..., description="Subscription info")
    generated_at: str = Field(..., description="Timestamp when metrics were generated")

    class Config:
        json_schema_extra = {
            "example": {
                "overview": {
                    "active_campaigns": 3,
                    "qualified_leads": 287,
                    "emails_sent": 450,
                    "ai_success_rate": 86.67
                },
                "growth": {
                    "leads_current": 95,
                    "leads_previous": 82,
                    "leads_change": 15.85,
                    "emails_current": 34,
                    "emails_previous": 29,
                    "emails_change": 17.24
                },
                "team": {
                    "total_users": 8,
                    "active_users": 6,
                    "user_activity_rate": 75.0,
                    "role_distribution": {"owner": 1, "admin": 2, "manager": 2, "operator": 3},
                    "period_days": 30
                },
                "ai_agents": {
                    "total_agent_runs": 15,
                    "successful_runs": 13,
                    "success_rate": 86.67,
                    "prospector_runs": 5,
                    "bant_runs": 5,
                    "scheduler_runs": 5,
                    "period_days": 30
                },
                "subscription": {
                    "plan": "growth",
                    "status": "active",
                    "leads_used": 287,
                    "leads_limit": 1000
                },
                "generated_at": "2026-02-02T13:45:00Z"
            }
        }


class RevenueMetrics(BaseModel):
    """Revenue metrics for business analytics."""
    mrr: float = Field(..., description="Monthly Recurring Revenue")
    total_customers: int = Field(..., description="Total active customers")
    plan_distribution: Dict[str, int] = Field(..., description="Distribution by plan type")
    average_revenue_per_customer: float = Field(..., description="ARPU")

    class Config:
        json_schema_extra = {
            "example": {
                "mrr": 12450.0,
                "total_customers": 127,
                "plan_distribution": {
                    "starter": 85,
                    "growth": 32,
                    "scale": 10
                },
                "average_revenue_per_customer": 98.03
            }
        }


class PlatformMetrics(BaseModel):
    """Platform-wide metrics for admin dashboard."""
    total_organizations: int = Field(..., description="Total organizations")
    active_subscriptions: int = Field(..., description="Active subscriptions")
    total_campaigns: int = Field(..., description="Total campaigns across platform")
    total_leads: int = Field(..., description="Total leads processed")
    total_emails: int = Field(..., description="Total emails sent")


class RecentActivity(BaseModel):
    """Recent activity metrics."""
    new_organizations_7d: int = Field(..., description="New organizations in last 7 days")
    new_campaigns_7d: int = Field(..., description="New campaigns in last 7 days")


class PlatformOverview(BaseModel):
    """Complete platform overview for admin."""
    platform: PlatformMetrics = Field(..., description="Platform-wide metrics")
    revenue: RevenueMetrics = Field(..., description="Revenue metrics")
    recent_activity: RecentActivity = Field(..., description="Recent activity")
    generated_at: str = Field(..., description="Generation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "platform": {
                    "total_organizations": 127,
                    "active_subscriptions": 127,
                    "total_campaigns": 456,
                    "total_leads": 125400,
                    "total_emails": 45600
                },
                "revenue": {
                    "mrr": 12450.0,
                    "total_customers": 127,
                    "plan_distribution": {"starter": 85, "growth": 32, "scale": 10},
                    "average_revenue_per_customer": 98.03
                },
                "recent_activity": {
                    "new_organizations_7d": 5,
                    "new_campaigns_7d": 23
                },
                "generated_at": "2026-02-02T13:45:00Z"
            }
        }


class EventTrackResponse(BaseModel):
    """Response for tracking analytics events."""
    success: bool = Field(..., description="Whether event was tracked successfully")
    message: str = Field(..., description="Response message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Event tracked successfully"
            }
        }