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
    campaigns_active: int = Field(..., description="Active campaigns count")
    leads_processed_30d: int = Field(..., description="Leads processed in last 30 days")
    leads_qualified_30d: int = Field(..., description="Leads qualified in last 30 days")
    emails_sent_30d: int = Field(..., description="Emails sent in last 30 days")
    qualification_rate: float = Field(..., description="Lead qualification rate")
    email_open_rate: float = Field(..., description="Email open rate")


class GrowthMetrics(BaseModel):
    """Growth metrics comparing periods."""
    leads_7d_vs_30d: Dict[str, int] = Field(..., description="Leads comparison")
    emails_7d_vs_30d: Dict[str, int] = Field(..., description="Emails comparison")


class SubscriptionInfo(BaseModel):
    """Subscription information."""
    plan_type: str = Field(..., description="Subscription plan type")
    status: str = Field(..., description="Subscription status")
    current_period_end: Optional[str] = Field(None, description="Current period end date")


class AnalyticsDashboard(BaseModel):
    """Complete dashboard analytics response."""
    overview: OverviewMetrics = Field(..., description="Key overview metrics")
    growth: GrowthMetrics = Field(..., description="Growth metrics")
    team: EngagementMetrics = Field(..., description="Team engagement metrics")
    ai_agents: AIAgentMetrics = Field(..., description="AI agent metrics")
    subscription: Optional[SubscriptionInfo] = Field(None, description="Subscription info")
    generated_at: str = Field(..., description="Timestamp when metrics were generated")

    class Config:
        json_schema_extra = {
            "example": {
                "overview": {
                    "campaigns_active": 3,
                    "leads_processed_30d": 1250,
                    "leads_qualified_30d": 287,
                    "emails_sent_30d": 450,
                    "qualification_rate": 22.96,
                    "email_open_rate": 36.0
                },
                "growth": {
                    "leads_7d_vs_30d": {"current": 95, "previous": 1155},
                    "emails_7d_vs_30d": {"current": 34, "previous": 416}
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
                    "plan_type": "growth",
                    "status": "active",
                    "current_period_end": "2026-03-02T00:00:00"
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