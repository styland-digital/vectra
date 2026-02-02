"""Seed database with initial data."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.core.logging import get_logger

logger = get_logger(__name__)


def seed_database():
    """Seed the database with initial data."""
    db = SessionLocal()
    try:
        # TODO: Add seed data
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
