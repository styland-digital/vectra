"""Integration tests for state machine."""

import pytest
from sqlalchemy.orm import Session

from app.db.models.lead import Lead, LeadStatus
from app.orchestrator.state_machine import LeadStateMachine, TransitionError
from tests.conftest import test_organization


@pytest.fixture
def test_campaign(db_session, test_organization):
    """Create a test campaign."""
    from app.db.models.campaign import Campaign, CampaignStatus
    campaign = Campaign(
        organization_id=test_organization.id,
        name="Test Campaign",
        status=CampaignStatus.DRAFT,
    )
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)
    return campaign


def test_valid_transition_new_to_enriched(db_session, test_organization, test_campaign):
    """Test valid transition from NEW to ENRICHED."""
    lead = Lead(
        campaign_id=test_campaign.id,
        organization_id=test_organization.id,
        email="test@example.com",
        status=LeadStatus.NEW,
    )
    db_session.add(lead)
    db_session.commit()
    
    LeadStateMachine.transition(lead, LeadStatus.ENRICHED, db_session)
    
    assert lead.status == LeadStatus.ENRICHED


def test_invalid_transition_new_to_qualified(db_session, test_organization, test_campaign):
    """Test invalid transition from NEW to QUALIFIED."""
    lead = Lead(
        campaign_id=test_campaign.id,
        organization_id=test_organization.id,
        email="test@example.com",
        status=LeadStatus.NEW,
    )
    db_session.add(lead)
    db_session.commit()
    
    with pytest.raises(TransitionError):
        LeadStateMachine.transition(lead, LeadStatus.QUALIFIED, db_session)


def test_transition_flow(db_session, test_organization, test_campaign):
    """Test complete transition flow."""
    lead = Lead(
        campaign_id=test_campaign.id,
        organization_id=test_organization.id,
        email="test@example.com",
        status=LeadStatus.NEW,
    )
    db_session.add(lead)
    db_session.commit()
    
    # NEW → ENRICHED
    LeadStateMachine.transition(lead, LeadStatus.ENRICHED, db_session)
    assert lead.status == LeadStatus.ENRICHED
    
    # ENRICHED → SCORING
    LeadStateMachine.transition(lead, LeadStatus.SCORING, db_session)
    assert lead.status == LeadStatus.SCORING
    
    # SCORING → QUALIFIED
    LeadStateMachine.transition(lead, LeadStatus.QUALIFIED, db_session)
    assert lead.status == LeadStatus.QUALIFIED
    
    # QUALIFIED → CONTACTED
    LeadStateMachine.transition(lead, LeadStatus.CONTACTED, db_session)
    assert lead.status == LeadStatus.CONTACTED


def test_can_transition():
    """Test can_transition method."""
    assert LeadStateMachine.can_transition(LeadStatus.NEW, LeadStatus.ENRICHED) is True
    assert LeadStateMachine.can_transition(LeadStatus.NEW, LeadStatus.QUALIFIED) is False
    assert LeadStateMachine.can_transition(LeadStatus.REJECTED, LeadStatus.QUALIFIED) is False
