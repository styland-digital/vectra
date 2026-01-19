"""Add invitations table for OTP-based invitations.

Revision ID: 004_add_invitations_table
Revises: 003_add_platform_admin
Create Date: 2026-01-18
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = '004_add_invitations_table'
down_revision: Union[str, None] = '003_add_platform_admin'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create invitations table
    op.create_table(
        'invitations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('organization_id', UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('invited_by', UUID(as_uuid=True), nullable=False),
        sa.Column('otp', sa.String(6), nullable=False),
        sa.Column('otp_expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Create indexes
    op.create_index('idx_invitations_email', 'invitations', ['email'])
    op.create_index('idx_invitations_otp', 'invitations', ['otp'])
    op.create_index('idx_invitations_organization', 'invitations', ['organization_id'])
    op.create_index('idx_invitations_expires_at', 'invitations', ['otp_expires_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_invitations_expires_at', 'invitations')
    op.drop_index('idx_invitations_organization', 'invitations')
    op.drop_index('idx_invitations_otp', 'invitations')
    op.drop_index('idx_invitations_email', 'invitations')
    
    # Drop table
    op.drop_table('invitations')
