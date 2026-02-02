"""Unit tests for PlatformService."""

import pytest
from uuid import uuid4
from app.services.platform import PlatformService
from app.core.exceptions import NotFoundError, BadRequestError
from app.db.models.user import User, UserRole
from app.db.models.organization import Organization, PlanType


class TestGetOverview:
    """Tests for PlatformService.get_overview method."""

    def test_get_overview_returns_statistics(self, db_session, test_organization, test_user):
        """Should return platform overview statistics."""
        service = PlatformService(db_session)
        overview = service.get_overview()

        assert overview["total_organizations"] == 1
        assert overview["total_users"] == 1
        assert "active_campaigns" in overview
        assert "total_leads" in overview
        assert "conversion_rate" in overview
        assert "emails_sent" in overview
        assert "meetings_scheduled" in overview

    def test_get_overview_empty_platform(self, db_session):
        """Should return zeros for empty platform."""
        service = PlatformService(db_session)
        overview = service.get_overview()

        assert overview["total_organizations"] == 0
        assert overview["total_users"] == 0
        assert overview["conversion_rate"] == 0.0


class TestListOrganizations:
    """Tests for PlatformService.list_organizations method."""

    def test_list_organizations_returns_all(self, db_session, test_organization):
        """Should return all organizations."""
        # Create another organization
        org2 = Organization(
            name="Another Org",
            slug="another-org",
            plan=PlanType.STARTER,
            settings={},
        )
        db_session.add(org2)
        db_session.commit()

        service = PlatformService(db_session)
        orgs = service.list_organizations()

        assert len(orgs) == 2

    def test_list_organizations_with_filters(self, db_session, test_organization):
        """Should filter organizations by plan."""
        # Create another organization with different plan
        org2 = Organization(
            name="Starter Org",
            slug="starter-org",
            plan=PlanType.STARTER,
            settings={},
        )
        db_session.add(org2)
        db_session.commit()

        service = PlatformService(db_session)
        starter_orgs = service.list_organizations(plan="starter")

        assert len(starter_orgs) == 1
        assert starter_orgs[0].plan == PlanType.STARTER

    def test_list_organizations_with_pagination(self, db_session, test_organization):
        """Should paginate results."""
        # Create multiple organizations
        for i in range(5):
            org = Organization(
                name=f"Org {i}",
                slug=f"org-{i}",
                plan=PlanType.TRIAL,
                settings={},
            )
            db_session.add(org)
        db_session.commit()

        service = PlatformService(db_session)
        orgs = service.list_organizations(skip=0, limit=3)

        assert len(orgs) == 3

    def test_list_organizations_invalid_plan_raises(self, db_session):
        """Invalid plan should raise BadRequestError."""
        service = PlatformService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.list_organizations(plan="invalid_plan")

        assert "Invalid plan type" in str(exc_info.value.detail)


class TestGetOrganization:
    """Tests for PlatformService.get_organization method."""

    def test_get_organization_returns_org(self, db_session, test_organization):
        """Should return organization by ID."""
        service = PlatformService(db_session)
        org = service.get_organization(test_organization.id)

        assert org.id == test_organization.id
        assert org.name == test_organization.name

    def test_get_organization_not_found_raises(self, db_session):
        """Non-existent organization should raise NotFoundError."""
        service = PlatformService(db_session)

        with pytest.raises(NotFoundError) as exc_info:
            service.get_organization(uuid4())

        assert "not found" in str(exc_info.value.detail).lower()


class TestCreateOrganization:
    """Tests for PlatformService.create_organization method."""

    def test_create_organization_success(self, db_session):
        """Should create a new organization."""
        service = PlatformService(db_session)
        org = service.create_organization(
            name="New Org",
            plan="trial",
        )

        assert org.name == "New Org"
        assert org.plan == PlanType.TRIAL

    def test_create_organization_with_settings(self, db_session):
        """Should create organization with custom settings."""
        service = PlatformService(db_session)
        settings = {"timezone": "UTC", "language": "fr"}
        org = service.create_organization(
            name="Settings Org",
            settings=settings,
        )

        assert org.settings == settings

    def test_create_organization_invalid_plan_raises(self, db_session):
        """Invalid plan should raise BadRequestError."""
        service = PlatformService(db_session)

        with pytest.raises(BadRequestError) as exc_info:
            service.create_organization(
                name="Invalid Org",
                plan="invalid_plan",
            )

        assert "Invalid plan type" in str(exc_info.value.detail)


class TestUpdateOrganization:
    """Tests for PlatformService.update_organization method."""

    def test_update_organization_name(self, db_session, test_organization):
        """Should update organization name."""
        service = PlatformService(db_session)
        org = service.update_organization(
            org_id=test_organization.id,
            name="Updated Name",
        )

        assert org.name == "Updated Name"

    def test_update_organization_plan(self, db_session, test_organization):
        """Should update organization plan."""
        service = PlatformService(db_session)
        org = service.update_organization(
            org_id=test_organization.id,
            plan="starter",
        )

        assert org.plan == PlanType.STARTER

    def test_update_organization_settings(self, db_session, test_organization):
        """Should update organization settings."""
        service = PlatformService(db_session)
        new_settings = {"timezone": "EST"}
        org = service.update_organization(
            org_id=test_organization.id,
            settings=new_settings,
        )

        assert org.settings == new_settings

    def test_update_organization_not_found_raises(self, db_session):
        """Non-existent organization should raise NotFoundError."""
        service = PlatformService(db_session)

        with pytest.raises(NotFoundError):
            service.update_organization(
                org_id=uuid4(),
                name="Updated",
            )


class TestDeleteOrganization:
    """Tests for PlatformService.delete_organization method."""

    def test_delete_organization_success(self, db_session, test_organization):
        """Should delete organization."""
        service = PlatformService(db_session)
        org_id = test_organization.id

        service.delete_organization(org_id)

        # Verify organization is deleted
        org = db_session.query(Organization).filter(Organization.id == org_id).first()
        assert org is None

    def test_delete_organization_not_found_raises(self, db_session):
        """Non-existent organization should raise NotFoundError."""
        service = PlatformService(db_session)

        with pytest.raises(NotFoundError):
            service.delete_organization(uuid4())


class TestListAllUsers:
    """Tests for PlatformService.list_all_users method."""

    def test_list_all_users_returns_users(self, db_session, test_user):
        """Should return all users."""
        service = PlatformService(db_session)
        users = service.list_all_users()

        assert len(users) == 1
        assert users[0].id == test_user.id

    def test_list_all_users_excludes_platform_admin(self, db_session, test_organization):
        """Should exclude platform admins from user list."""
        # Create platform admin
        platform_admin = User(
            email="admin@vectra.io",
            password_hash="hash",
            organization_id=None,
            role=UserRole.PLATFORM_ADMIN,
            is_active=True,
        )
        db_session.add(platform_admin)

        # Create regular user
        regular_user = User(
            email="user@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=True,
        )
        db_session.add(regular_user)
        db_session.commit()

        service = PlatformService(db_session)
        users = service.list_all_users()

        assert len(users) == 1
        assert users[0].email == "user@example.com"

    def test_list_all_users_with_filters(self, db_session, test_organization):
        """Should filter users by organization, role, and active status."""
        # Create users with different attributes
        user1 = User(
            email="admin1@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.ADMIN,
            is_active=True,
        )
        user2 = User(
            email="operator1@example.com",
            password_hash="hash",
            organization_id=test_organization.id,
            role=UserRole.OPERATOR,
            is_active=False,
        )
        db_session.add_all([user1, user2])
        db_session.commit()

        service = PlatformService(db_session)

        # Filter by role
        admins = service.list_all_users(role="admin")
        assert len(admins) == 1
        assert admins[0].role == UserRole.ADMIN

        # Filter by active status
        active_users = service.list_all_users(is_active=True)
        assert all(user.is_active for user in active_users)

    def test_list_all_users_with_pagination(self, db_session, test_organization):
        """Should paginate user results."""
        # Create multiple users
        for i in range(5):
            user = User(
                email=f"user{i}@example.com",
                password_hash="hash",
                organization_id=test_organization.id,
                role=UserRole.OPERATOR,
                is_active=True,
            )
            db_session.add(user)
        db_session.commit()

        service = PlatformService(db_session)
        users = service.list_all_users(skip=0, limit=3)

        assert len(users) == 3


class TestGetSystemMetrics:
    """Tests for PlatformService.get_system_metrics method."""

    def test_get_system_metrics_returns_dict(self, db_session):
        """Should return system metrics dictionary."""
        service = PlatformService(db_session)
        metrics = service.get_system_metrics()

        assert "api_requests_per_minute" in metrics
        assert "average_response_time_ms" in metrics
        assert "agent_latency_avg_ms" in metrics
        assert "error_rate" in metrics
        assert "active_users" in metrics
