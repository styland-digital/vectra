"""Initial database schema with all core tables.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-01-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create all ENUMs first using raw SQL
    op.execute("CREATE TYPE plan_type AS ENUM ('trial', 'starter', 'growth', 'scale')")
    op.execute("CREATE TYPE user_role AS ENUM ('owner', 'admin', 'manager', 'operator', 'viewer')")
    op.execute("CREATE TYPE campaign_status AS ENUM ('draft', 'active', 'paused', 'completed', 'archived')")
    op.execute("CREATE TYPE lead_status AS ENUM ('new', 'enriched', 'scoring', 'qualified', 'contacted', 'meeting_scheduled', 'completed', 'rejected')")
    op.execute("CREATE TYPE lead_intent AS ENUM ('interested_now', 'interested_later', 'objection_price', 'objection_timing', 'polite_decline', 'not_interested', 'out_of_office', 'wrong_person')")
    op.execute("CREATE TYPE email_status AS ENUM ('pending', 'approved', 'rejected', 'sent', 'delivered', 'bounced')")
    op.execute("CREATE TYPE bounce_type AS ENUM ('hard', 'soft', 'complaint')")
    op.execute("CREATE TYPE meeting_status AS ENUM ('scheduled', 'confirmed', 'completed', 'canceled', 'no_show')")
    op.execute("CREATE TYPE meeting_outcome AS ENUM ('qualified', 'needs_followup', 'not_interested', 'wrong_fit', 'deal_closed')")
    op.execute("CREATE TYPE subscription_status AS ENUM ('active', 'past_due', 'unpaid', 'canceled', 'incomplete', 'incomplete_expired', 'trialing', 'paused')")
    op.execute("CREATE TYPE billing_cycle AS ENUM ('monthly', 'yearly')")
    op.execute("CREATE TYPE agent_type AS ENUM ('prospector', 'bant_qualifier', 'scheduler', 'intent_classifier')")
    op.execute("CREATE TYPE agent_run_status AS ENUM ('pending', 'running', 'completed', 'failed', 'canceled')")
    op.execute("CREATE TYPE integration_type AS ENUM ('hubspot', 'salesforce', 'calendly', 'google_calendar', 'slack')")
    op.execute("CREATE TYPE integration_status AS ENUM ('connected', 'disconnected', 'error', 'pending')")

    # 1. Organizations table (root entity)
    op.execute("""
        CREATE TABLE organizations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            plan plan_type NOT NULL DEFAULT 'trial',
            settings JSONB NOT NULL DEFAULT '{}',
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_organizations_slug ON organizations(slug)")

    # 2. Users table
    op.execute("""
        CREATE TABLE users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            role user_role NOT NULL DEFAULT 'operator',
            is_active BOOLEAN NOT NULL DEFAULT true,
            email_verified_at TIMESTAMP,
            last_login_at TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_users_org ON users(organization_id)")
    op.execute("CREATE INDEX idx_users_email ON users(email)")

    # 3. Campaigns table
    op.execute("""
        CREATE TABLE campaigns (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
            created_by UUID REFERENCES users(id) ON DELETE SET NULL,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            status campaign_status NOT NULL DEFAULT 'draft',
            target_criteria JSONB NOT NULL DEFAULT '{}',
            email_template JSONB,
            bant_threshold INTEGER NOT NULL DEFAULT 60,
            daily_limit INTEGER NOT NULL DEFAULT 50,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_campaigns_org ON campaigns(organization_id)")
    op.execute("CREATE INDEX idx_campaigns_status ON campaigns(status)")

    # 4. Leads table
    op.execute("""
        CREATE TABLE leads (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
            organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
            email VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            job_title VARCHAR(200),
            company_name VARCHAR(255),
            company_size VARCHAR(50),
            linkedin_url VARCHAR(500),
            phone VARCHAR(50),
            enrichment_data JSONB NOT NULL DEFAULT '{}',
            bant_score INTEGER,
            bant_breakdown JSONB,
            intent lead_intent,
            status lead_status NOT NULL DEFAULT 'new',
            source VARCHAR(100),
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            UNIQUE(campaign_id, email)
        )
    """)
    op.execute("CREATE INDEX idx_leads_campaign ON leads(campaign_id)")
    op.execute("CREATE INDEX idx_leads_org ON leads(organization_id)")
    op.execute("CREATE INDEX idx_leads_status ON leads(status)")
    op.execute("CREATE INDEX idx_leads_score ON leads(bant_score)")

    # 5. Emails table
    op.execute("""
        CREATE TABLE emails (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
            campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
            subject VARCHAR(500) NOT NULL,
            body TEXT NOT NULL,
            status email_status NOT NULL DEFAULT 'pending',
            approved_by UUID REFERENCES users(id) ON DELETE SET NULL,
            approved_at TIMESTAMP,
            sent_at TIMESTAMP,
            delivered_at TIMESTAMP,
            opened_at TIMESTAMP,
            open_count INTEGER NOT NULL DEFAULT 0,
            clicked_at TIMESTAMP,
            click_count INTEGER NOT NULL DEFAULT 0,
            replied_at TIMESTAMP,
            bounced_at TIMESTAMP,
            bounce_type bounce_type,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_emails_lead ON emails(lead_id)")
    op.execute("CREATE INDEX idx_emails_campaign ON emails(campaign_id)")
    op.execute("CREATE INDEX idx_emails_status ON emails(status)")

    # 6. Meetings table
    op.execute("""
        CREATE TABLE meetings (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
            campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
            organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
            scheduled_at TIMESTAMP NOT NULL,
            duration_minutes INTEGER NOT NULL DEFAULT 30,
            meeting_url VARCHAR(500),
            calendly_event_id VARCHAR(255),
            status meeting_status NOT NULL DEFAULT 'scheduled',
            completed_at TIMESTAMP,
            no_show BOOLEAN NOT NULL DEFAULT false,
            notes TEXT,
            outcome meeting_outcome,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_meetings_lead ON meetings(lead_id)")
    op.execute("CREATE INDEX idx_meetings_org ON meetings(organization_id)")
    op.execute("CREATE INDEX idx_meetings_scheduled ON meetings(scheduled_at)")
    op.execute("CREATE INDEX idx_meetings_status ON meetings(status)")

    # 7. Subscriptions table
    op.execute("""
        CREATE TABLE subscriptions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id UUID UNIQUE NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
            stripe_customer_id VARCHAR(255),
            stripe_subscription_id VARCHAR(255) UNIQUE,
            plan VARCHAR(50) NOT NULL,
            billing_cycle billing_cycle,
            status subscription_status NOT NULL,
            current_period_start TIMESTAMP,
            current_period_end TIMESTAMP,
            trial_end TIMESTAMP,
            cancel_at_period_end BOOLEAN NOT NULL DEFAULT false,
            canceled_at TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_subscription_id)")

    # 8. Usage records table
    op.execute("""
        CREATE TABLE usage_records (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            leads_used INTEGER NOT NULL DEFAULT 0,
            leads_limit INTEGER,
            emails_sent INTEGER NOT NULL DEFAULT 0,
            emails_limit INTEGER,
            api_calls INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            UNIQUE(organization_id, period_start)
        )
    """)
    op.execute("CREATE INDEX idx_usage_org ON usage_records(organization_id, period_start DESC)")

    # 9. Agent runs table
    op.execute("""
        CREATE TABLE agent_runs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
            agent_type agent_type NOT NULL,
            status agent_run_status NOT NULL DEFAULT 'pending',
            input_data JSONB,
            output_data JSONB,
            error_message TEXT,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            duration_ms INTEGER,
            tokens_used INTEGER,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_agent_runs_campaign ON agent_runs(campaign_id)")
    op.execute("CREATE INDEX idx_agent_runs_status ON agent_runs(status)")

    # 10. Integrations table
    op.execute("""
        CREATE TABLE integrations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
            type integration_type NOT NULL,
            status integration_status NOT NULL DEFAULT 'disconnected',
            credentials JSONB,
            settings JSONB NOT NULL DEFAULT '{}',
            last_sync_at TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            UNIQUE(organization_id, type)
        )
    """)
    op.execute("CREATE INDEX idx_integrations_org ON integrations(organization_id)")

    # Create updated_at trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)

    # Apply trigger to all tables with updated_at
    tables_with_updated_at = [
        'organizations', 'users', 'campaigns', 'leads', 'emails',
        'meetings', 'subscriptions', 'usage_records', 'integrations'
    ]
    for table in tables_with_updated_at:
        op.execute(f"""
            CREATE TRIGGER update_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at()
        """)


def downgrade() -> None:
    # Drop triggers
    tables_with_updated_at = [
        'organizations', 'users', 'campaigns', 'leads', 'emails',
        'meetings', 'subscriptions', 'usage_records', 'integrations'
    ]
    for table in tables_with_updated_at:
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table}")

    op.execute("DROP FUNCTION IF EXISTS update_updated_at()")

    # Drop tables in reverse order
    op.execute("DROP TABLE IF EXISTS integrations")
    op.execute("DROP TABLE IF EXISTS agent_runs")
    op.execute("DROP TABLE IF EXISTS usage_records")
    op.execute("DROP TABLE IF EXISTS subscriptions")
    op.execute("DROP TABLE IF EXISTS meetings")
    op.execute("DROP TABLE IF EXISTS emails")
    op.execute("DROP TABLE IF EXISTS leads")
    op.execute("DROP TABLE IF EXISTS campaigns")
    op.execute("DROP TABLE IF EXISTS users")
    op.execute("DROP TABLE IF EXISTS organizations")

    # Drop ENUMs
    op.execute("DROP TYPE IF EXISTS integration_status")
    op.execute("DROP TYPE IF EXISTS integration_type")
    op.execute("DROP TYPE IF EXISTS agent_run_status")
    op.execute("DROP TYPE IF EXISTS agent_type")
    op.execute("DROP TYPE IF EXISTS billing_cycle")
    op.execute("DROP TYPE IF EXISTS subscription_status")
    op.execute("DROP TYPE IF EXISTS meeting_outcome")
    op.execute("DROP TYPE IF EXISTS meeting_status")
    op.execute("DROP TYPE IF EXISTS bounce_type")
    op.execute("DROP TYPE IF EXISTS email_status")
    op.execute("DROP TYPE IF EXISTS lead_intent")
    op.execute("DROP TYPE IF EXISTS lead_status")
    op.execute("DROP TYPE IF EXISTS campaign_status")
    op.execute("DROP TYPE IF EXISTS user_role")
    op.execute("DROP TYPE IF EXISTS plan_type")
