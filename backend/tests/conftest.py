"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.main import app
from app.api.deps import get_db
from app.core.config import settings

# Use PostgreSQL test database (same driver, different DB name)
# Replace only the database name, not the user
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/vectra", "/vectra_test").replace("vectra_test:", "vectra:")

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session with clean tables."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_organization(db_session):
    """Create a test organization."""
    from app.db.models.organization import Organization, PlanType

    org = Organization(
        name="Test Organization",
        slug="test-org",
        plan=PlanType.TRIAL.value,
        settings={},
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)
    return org


@pytest.fixture
def test_user(db_session, test_organization):
    """Create a test user with organization."""
    from app.db.models.user import User, UserRole
    from app.core.security import get_password_hash

    user = User(
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        organization_id=test_organization.id,
        first_name="Test",
        last_name="User",
        role=UserRole.OPERATOR,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session, test_organization):
    """Create a test admin user."""
    from app.db.models.user import User, UserRole
    from app.core.security import get_password_hash

    user = User(
        email="admin@example.com",
        password_hash=get_password_hash("password123"),
        organization_id=test_organization.id,
        first_name="Admin",
        last_name="User",
        role=UserRole.ADMIN,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_owner_user(db_session, test_organization):
    """Create a test owner user."""
    from app.db.models.user import User, UserRole
    from app.core.security import get_password_hash

    user = User(
        email="owner@example.com",
        password_hash=get_password_hash("password123"),
        organization_id=test_organization.id,
        first_name="Owner",
        last_name="User",
        role=UserRole.OWNER,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def inactive_user(db_session, test_organization):
    """Create an inactive test user."""
    from app.db.models.user import User, UserRole
    from app.core.security import get_password_hash

    user = User(
        email="inactive@example.com",
        password_hash=get_password_hash("password123"),
        organization_id=test_organization.id,
        first_name="Inactive",
        last_name="User",
        role=UserRole.OPERATOR,
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    """Get a valid access token for test user."""
    from app.core.security import create_access_token

    token_data = {
        "sub": str(test_user.id),
        "role": test_user.role.value,
    }
    if test_user.organization_id:
        token_data["org"] = str(test_user.organization_id)
    token = create_access_token(token_data)
    return token


@pytest.fixture
def auth_headers(auth_token):
    """Get authorization headers with valid token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def refresh_token(test_user):
    """Get a valid refresh token for test user."""
    from app.core.security import create_refresh_token

    token = create_refresh_token({
        "sub": str(test_user.id),
        "role": test_user.role.value,
    })
    # Only add org if user belongs to organization
    if test_user.organization_id:
        token = create_refresh_token({
            "sub": str(test_user.id),
            "org": str(test_user.organization_id),
            "role": test_user.role.value,
        })
    return token


@pytest.fixture
def platform_admin_user(db_session):
    """Create a platform admin user."""
    from app.db.models.user import User, UserRole
    from app.core.security import get_password_hash

    user = User(
        email="admin@vectra.io",
        password_hash=get_password_hash("password123"),
        organization_id=None,
        first_name="Platform",
        last_name="Admin",
        role=UserRole.PLATFORM_ADMIN,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def platform_admin_token(platform_admin_user):
    """Get a valid access token for platform admin."""
    from app.core.security import create_access_token

    token = create_access_token({
        "sub": str(platform_admin_user.id),
        "role": platform_admin_user.role.value,
    })
    return token


@pytest.fixture
def platform_admin_headers(platform_admin_token):
    """Get authorization headers with platform admin token."""
    return {"Authorization": f"Bearer {platform_admin_token}"}


@pytest.fixture(scope="session", autouse=True)
def configure_llm_for_tests():
    """Configure LLM environment variables for tests."""
    import os
    
    # Set LLM provider to ollama for tests
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # Use test-friendly Ollama configuration
    # For tests, we can use a mock or test instance
    # If OLLAMA_BASE_URL is not set, tests will use mocks
    if "OLLAMA_BASE_URL" not in os.environ:
        os.environ["OLLAMA_BASE_URL"] = "https://api.ollama.com"
    
    if "OLLAMA_MODEL" not in os.environ:
        os.environ["OLLAMA_MODEL"] = "llama2:7b"
    
    # Set Claude API key if available (for fallback)
    # Tests will use mocks if LLM is not available
    if "CLAUDE_API_KEY" not in os.environ:
        # Use test key or leave empty to use mocks
        os.environ["CLAUDE_API_KEY"] = ""
    
    # Set ANTHROPIC_API_KEY for CrewAI Claude support
    if "ANTHROPIC_API_KEY" not in os.environ and os.environ.get("CLAUDE_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = os.environ["CLAUDE_API_KEY"]
    
    yield
    
    # Cleanup (optional)
    # os.environ.pop("LLM_PROVIDER", None)


@pytest.fixture
def mock_llm():
    """Mock LLM for unit/integration tests that don't need real LLM."""
    from unittest.mock import MagicMock
    return MagicMock()


@pytest.fixture
def mock_crew_llm(monkeypatch):
    """Mock CrewAI LLM functions for tests."""
    from unittest.mock import MagicMock
    
    def mock_get_llm():
        return None  # Use CrewAI default (which will be mocked)
    
    def mock_get_memory():
        return None  # No memory for tests
    
    monkeypatch.setattr("app.agents.crew.get_llm", mock_get_llm)
    monkeypatch.setattr("app.agents.crew.get_memory", mock_get_memory)
    
    yield
