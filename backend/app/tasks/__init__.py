"""Celery tasks."""

# Import tasks to register them with Celery
from app.tasks import prospector, bant, scheduler  # noqa: F401

__all__ = ["prospector", "bant", "scheduler"]
