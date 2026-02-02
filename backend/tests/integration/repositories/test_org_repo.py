"""Integration tests for OrganizationRepository."""

import pytest
from uuid import uuid4

from app.db.repositories.organization import OrganizationRepository
from app.db.models.organization import Organization, PlanType


class TestOrganizationRepository:
    """Tests for OrganizationRepository CRUD operations."""

    def test_get_by_id_found(self, db_session, test_organization):
        """Should return organization when ID exists."""
        repo = OrganizationRepository(db_session)

        org = repo.get_by_id(test_organization.id)

        assert org is not None
        assert org.id == test_organization.id
        assert org.name == "Test Organization"

    def test_get_by_id_not_found(self, db_session):
        """Should return None when ID doesn't exist."""
        repo = OrganizationRepository(db_session)

        org = repo.get_by_id(uuid4())

        assert org is None

    def test_get_by_slug_found(self, db_session, test_organization):
        """Should return organization when slug exists."""
        repo = OrganizationRepository(db_session)

        org = repo.get_by_slug("test-org")

        assert org is not None
        assert org.slug == "test-org"

    def test_get_by_slug_not_found(self, db_session):
        """Should return None when slug doesn't exist."""
        repo = OrganizationRepository(db_session)

        org = repo.get_by_slug("nonexistent-slug")

        assert org is None

    def test_slug_exists_true(self, db_session, test_organization):
        """Should return True when slug exists."""
        repo = OrganizationRepository(db_session)

        exists = repo.slug_exists("test-org")

        assert exists is True

    def test_slug_exists_false(self, db_session):
        """Should return False when slug doesn't exist."""
        repo = OrganizationRepository(db_session)

        exists = repo.slug_exists("nonexistent-slug")

        assert exists is False

    def test_generate_unique_slug_simple(self, db_session):
        """Should generate slug from name."""
        repo = OrganizationRepository(db_session)

        slug = repo.generate_unique_slug("My Company")

        assert slug == "my-company"

    def test_generate_unique_slug_special_chars(self, db_session):
        """Should handle special characters in name."""
        repo = OrganizationRepository(db_session)

        slug = repo.generate_unique_slug("Company & Co. (US)")

        assert "company" in slug
        assert "&" not in slug
        assert "(" not in slug

    def test_generate_unique_slug_collision(self, db_session, test_organization):
        """Should add suffix when slug exists."""
        repo = OrganizationRepository(db_session)

        # test-org already exists from fixture
        slug = repo.generate_unique_slug("Test Org")

        assert slug.startswith("test-org-")
        assert slug != "test-org"

    def test_create_organization(self, db_session):
        """Should create a new organization."""
        repo = OrganizationRepository(db_session)

        org = repo.create(
            name="New Organization",
        )

        assert org.id is not None
        assert org.name == "New Organization"
        assert org.slug == "new-organization"
        assert org.plan == PlanType.TRIAL

    def test_create_organization_with_custom_slug(self, db_session):
        """Should use custom slug when provided."""
        repo = OrganizationRepository(db_session)

        org = repo.create(
            name="Custom Slug Org",
            slug="custom-slug",
        )

        assert org.slug == "custom-slug"

    def test_create_organization_with_plan(self, db_session):
        """Should set plan when provided."""
        repo = OrganizationRepository(db_session)

        org = repo.create(
            name="Growth Org",
            plan=PlanType.GROWTH,
        )

        assert org.plan == PlanType.GROWTH

    def test_update_organization_name(self, db_session, test_organization):
        """Should update organization name."""
        repo = OrganizationRepository(db_session)

        updated = repo.update(
            test_organization,
            name="Updated Organization",
        )

        assert updated.name == "Updated Organization"

    def test_update_organization_settings(self, db_session, test_organization):
        """Should update organization settings."""
        repo = OrganizationRepository(db_session)
        new_settings = {"timezone": "UTC", "theme": "dark"}

        updated = repo.update(
            test_organization,
            settings=new_settings,
        )

        assert updated.settings == new_settings

    def test_upgrade_plan(self, db_session, test_organization):
        """Should upgrade organization plan."""
        repo = OrganizationRepository(db_session)
        assert test_organization.plan == PlanType.TRIAL

        updated = repo.upgrade_plan(test_organization, PlanType.SCALE)

        assert updated.plan == PlanType.SCALE

    def test_upgrade_plan_persists(self, db_session, test_organization):
        """Plan upgrade should persist in database."""
        repo = OrganizationRepository(db_session)

        repo.upgrade_plan(test_organization, PlanType.GROWTH)

        # Fetch fresh from database
        db_session.expire_all()
        org = repo.get_by_id(test_organization.id)
        assert org.plan == PlanType.GROWTH
