"""Add email verification OTP columns to users table.

Revision ID: 002_add_email_verification_otp
Revises: 001_initial_schema
Create Date: 2026-01-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_add_email_verification_otp'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE users
        ADD COLUMN email_verification_otp VARCHAR(6),
        ADD COLUMN email_verification_otp_expires_at TIMESTAMP
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE users
        DROP COLUMN IF EXISTS email_verification_otp_expires_at,
        DROP COLUMN IF EXISTS email_verification_otp
    """)
