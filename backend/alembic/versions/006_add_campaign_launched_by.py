"""Add launched_by column to campaigns table.

Revision ID: 006_add_campaign_launched_by
Revises: 005_add_password_change_otp
Create Date: 2026-05-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = '006_add_campaign_launched_by'
down_revision: Union[str, None] = '005_add_password_change_otp'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'campaigns',
        sa.Column(
            'launched_by',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
        ),
    )
    op.create_index('ix_campaigns_launched_by', 'campaigns', ['launched_by'])


def downgrade() -> None:
    op.drop_index('ix_campaigns_launched_by', table_name='campaigns')
    op.drop_column('campaigns', 'launched_by')
