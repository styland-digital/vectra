"""Add enriched_at and qualified_at tracking timestamps to leads table.

Revision ID: 007_add_enriched_at_qualified_at_to_leads
Revises: 006_add_campaign_launched_by
Create Date: 2026-05-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '007_add_lead_timestamps'
down_revision: Union[str, None] = '006_add_campaign_launched_by'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'leads',
        sa.Column('enriched_at', sa.DateTime(), nullable=True),
    )
    op.add_column(
        'leads',
        sa.Column('qualified_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('leads', 'qualified_at')
    op.drop_column('leads', 'enriched_at')
