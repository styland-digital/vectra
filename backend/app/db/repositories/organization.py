"""Organization repository for database operations."""

from typing import Optional
from uuid import UUID
import re

from sqlalchemy.orm import Session

from app.db.models.organization import Organization, PlanType


class OrganizationRepository:
    """Repository for Organization CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, org_id: UUID) -> Optional[Organization]:
        """Get organization by ID."""
        return self.db.query(Organization).filter(Organization.id == org_id).first()

    def get_by_slug(self, slug: str) -> Optional[Organization]:
        """Get organization by slug."""
        return self.db.query(Organization).filter(Organization.slug == slug).first()

    def slug_exists(self, slug: str) -> bool:
        """Check if slug already exists."""
        return (
            self.db.query(Organization).filter(Organization.slug == slug).first()
            is not None
        )

    def generate_unique_slug(self, name: str) -> str:
        """Generate a unique slug from organization name."""
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

        # Check if slug exists, append number if needed
        base_slug = slug
        counter = 1
        while self.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def create(
        self,
        name: str,
        slug: Optional[str] = None,
        plan: PlanType = PlanType.TRIAL,
    ) -> Organization:
        """Create a new organization."""
        if not slug:
            slug = self.generate_unique_slug(name)

        # Ensure plan is a PlanType enum instance
        if isinstance(plan, str):
            plan = PlanType(plan.lower())

        org = Organization(
            name=name,
            slug=slug,
            plan=plan,
            settings={},
        )
        self.db.add(org)
        self.db.commit()
        self.db.refresh(org)
        return org

    def update(
        self,
        org: Organization,
        name: Optional[str] = None,
        settings: Optional[dict] = None,
    ) -> Organization:
        """Update organization details."""
        if name:
            org.name = name
        if settings is not None:
            org.settings = settings
        self.db.commit()
        self.db.refresh(org)
        return org

    def upgrade_plan(self, org: Organization, new_plan: PlanType) -> Organization:
        """Upgrade organization's plan."""
        org.plan = new_plan
        self.db.commit()
        self.db.refresh(org)
        return org
