"""Celery application configuration."""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "vectra",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.campaign",
        "app.tasks.prospector",
        "app.tasks.bant",
        "app.tasks.scheduler",
    ],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    # Windows: billiard's prefork pool uses semaphores that require elevated
    # privileges. Use solo pool (single-threaded) for local dev on Windows.
    worker_pool="solo",
    beat_schedule={
        "cleanup-stale-scoring-hourly": {
            "task": "campaign.cleanup_stale_scoring",
            "schedule": crontab(minute=0),
        },
    },
)
