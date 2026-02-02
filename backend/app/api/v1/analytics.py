"""Analytics API endpoints for business KPIs and metrics."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.core.logging import get_logger
from app.api.deps import get_db, get_organization_user, get_platform_admin
from app.db.models.user import User
from app.services.analytics_service import AnalyticsService, AnalyticsEvent
from app.schemas.analytics import (
    AnalyticsDashboard,
    UsageMetrics,
    EngagementMetrics,
    AIAgentMetrics,
    PlatformOverview,
    RevenueMetrics,
    AnalyticsEventTrack,
    EventTrackResponse
)

logger = get_logger(__name__)
router = APIRouter()


@router.get("/overview", response_model=AnalyticsDashboard)
async def get_analytics_overview(
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics overview for organization dashboard."""
    try:
        analytics_service = AnalyticsService(db)

        overview = await analytics_service.get_dashboard_overview(
            organization_id=current_user.organization_id
        )

        if not overview:
            raise HTTPException(status_code=500, detail="Failed to generate analytics overview")

        return overview

    except Exception as e:
        logger.error(f"Analytics overview failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage", response_model=UsageMetrics)
async def get_usage_metrics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Get detailed usage metrics for organization."""
    try:
        analytics_service = AnalyticsService(db)

        metrics = await analytics_service.get_usage_metrics(
            organization_id=current_user.organization_id,
            days=days
        )

        return metrics

    except Exception as e:
        logger.error(f"Usage metrics failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/engagement", response_model=EngagementMetrics)
async def get_engagement_metrics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Get user engagement metrics for organization."""
    try:
        analytics_service = AnalyticsService(db)

        metrics = await analytics_service.get_user_engagement_metrics(
            organization_id=current_user.organization_id,
            days=days
        )

        return metrics

    except Exception as e:
        logger.error(f"Engagement metrics failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai-agents", response_model=AIAgentMetrics)
async def get_ai_agent_metrics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Get AI agent performance metrics for organization."""
    try:
        analytics_service = AnalyticsService(db)

        metrics = await analytics_service.get_ai_agent_metrics(
            organization_id=current_user.organization_id,
            days=days
        )

        return metrics

    except Exception as e:
        logger.error(f"AI agent metrics failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/events", response_model=EventTrackResponse)
async def track_analytics_event(
    request: AnalyticsEventTrack,
    current_user: User = Depends(get_organization_user),
    db: Session = Depends(get_db)
):
    """Track a custom analytics event."""
    try:
        analytics_service = AnalyticsService(db)

        success = await analytics_service.track_event(
            organization_id=current_user.organization_id,
            event_type=request.event_type,
            user_id=current_user.id,
            properties=request.properties,
            value=request.value
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to track event")

        return {"success": True, "message": "Event tracked successfully"}

    except Exception as e:
        logger.error(f"Event tracking failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Platform Admin Analytics Endpoints
@router.get("/platform/overview", response_model=PlatformOverview)
async def get_platform_analytics_overview(
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db)
):
    """Get platform-wide analytics overview (Platform Admin only)."""
    try:
        analytics_service = AnalyticsService(db)

        overview = await analytics_service.get_platform_overview()

        if not overview:
            raise HTTPException(status_code=500, detail="Failed to generate platform overview")

        return overview

    except Exception as e:
        logger.error(f"Platform analytics overview failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platform/revenue", response_model=RevenueMetrics)
async def get_platform_revenue_metrics(
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db)
):
    """Get platform-wide revenue metrics (Platform Admin only)."""
    try:
        analytics_service = AnalyticsService(db)

        metrics = await analytics_service.get_revenue_metrics()

        return metrics

    except Exception as e:
        logger.error(f"Platform revenue metrics failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))