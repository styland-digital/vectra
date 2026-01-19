"""Add password change OTP columns to users table.

Revision ID: 005_add_password_change_otp
Revises: 004_add_invitations_table
Create Date: 2026-01-19
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '005_add_password_change_otp'
down_revision: Union[str, None] = '004_add_invitations_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE users
        ADD COLUMN password_change_otp VARCHAR(6),
        ADD COLUMN password_change_otp_expires_at TIMESTAMP
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE users
        DROP COLUMN IF EXISTS password_change_otp_expires_at,
        DROP COLUMN IF EXISTS password_change_otp
    """)
