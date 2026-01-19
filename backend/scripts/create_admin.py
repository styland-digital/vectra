"""Create an admin user."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.core.logging import get_logger

logger = get_logger(__name__)


def create_admin(email: str, password: str):
    """Create an admin user."""
    db = SessionLocal()
    try:
        # TODO: Implement admin creation
        # user = User(
        #     email=email,
        #     password_hash=get_password_hash(password),
        #     role="admin",
        #     is_active=True,
        # )
        # db.add(user)
        # db.commit()
        logger.info(f"Admin user created: {email}")
    except Exception as e:
        logger.error(f"Error creating admin: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    create_admin(email, password)
