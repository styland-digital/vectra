"""Data enrichment service for prospects."""

from typing import Dict, List, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models.lead import Lead, LeadStatus
from app.services.rocketreach import RocketReachService
from app.core.logging import get_logger

logger = get_logger(__name__)


class EnrichmentService:
    """Service for enriching prospect data and managing duplicates."""

    def __init__(self, db: Session, rocketreach_service: Optional[RocketReachService] = None):
        """
        Initialize enrichment service.
        
        Args:
            db: Database session
            rocketreach_service: RocketReach service instance (optional)
        """
        self.db = db
        self.rocketreach_service = rocketreach_service or RocketReachService()

    async def enrich_prospect_data(
        self,
        prospect_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Enrich prospect data using RocketReach API.
        
        Args:
            prospect_data: Basic prospect data
            
        Returns:
            Enriched prospect data
        """
        email = prospect_data.get("email")
        linkedin_url = prospect_data.get("linkedin_url")
        first_name = prospect_data.get("first_name")
        last_name = prospect_data.get("last_name")
        company = prospect_data.get("company_name")
        
        # Use RocketReach to enrich data
        enriched = await self.rocketreach_service.enrich_prospect(
            email=email,
            linkedin_url=linkedin_url,
            first_name=first_name,
            last_name=last_name,
            company=company,
        )
        
        # Merge with original data (enriched takes precedence)
        enriched_data = {**prospect_data, **enriched}
        
        # Remove None values
        enriched_data = {k: v for k, v in enriched_data.items() if v is not None}
        
        return enriched_data

    def check_duplicate(
        self,
        email: str,
        campaign_id: UUID,
        organization_id: UUID,
    ) -> Optional[Lead]:
        """
        Check if a lead with this email already exists in the campaign.
        
        Args:
            email: Email address to check
            campaign_id: Campaign ID
            organization_id: Organization ID
            
        Returns:
            Existing Lead if found, None otherwise
        """
        lead = (
            self.db.query(Lead)
            .filter(
                Lead.email == email,
                Lead.campaign_id == campaign_id,
                Lead.organization_id == organization_id,
            )
            .first()
        )
        
        if lead:
            logger.debug(f"Duplicate lead found: {email} in campaign {campaign_id}")
        
        return lead

    def calculate_firmographic_score(
        self,
        prospect_data: Dict[str, Any],
        target_criteria: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Calculate firmographic priority score (0-100) for a prospect.
        
        Scoring factors:
        - Company size match (0-30)
        - Industry match (0-25)
        - Location match (0-20)
        - Job title match (0-15)
        - Data completeness (0-10)
        
        Args:
            prospect_data: Prospect data dictionary
            target_criteria: Target criteria from campaign (optional)
            
        Returns:
            Firmographic score (0-100)
        """
        score = 0
        
        # Company size match (0-30)
        company_size = prospect_data.get("company_size", "").lower()
        if target_criteria and "company_sizes" in target_criteria:
            target_sizes = [s.lower() for s in target_criteria["company_sizes"]]
            if any(target in company_size or company_size in target for target in target_sizes):
                score += 30
            elif company_size:
                # Partial match
                score += 15
        elif company_size:
            # No target criteria, but data exists
            score += 15
        
        # Industry match (0-25)
        industry = prospect_data.get("company_industry", "").lower()
        if target_criteria and "industries" in target_criteria:
            target_industries = [i.lower() for i in target_criteria["industries"]]
            if any(target in industry or industry in target for target in target_industries):
                score += 25
            elif industry:
                score += 12
        elif industry:
            score += 12
        
        # Location match (0-20)
        location = prospect_data.get("location", "").lower()
        if target_criteria and "locations" in target_criteria:
            target_locations = [l.lower() for l in target_criteria["locations"]]
            if any(target in location or location in target for target in target_locations):
                score += 20
            elif location:
                score += 10
        elif location:
            score += 10
        
        # Job title match (0-15)
        job_title = prospect_data.get("job_title", "").lower()
        if target_criteria and "job_titles" in target_criteria:
            target_titles = [t.lower() for t in target_criteria["job_titles"]]
            if any(target in job_title or job_title in target for target in target_titles):
                score += 15
            elif job_title:
                score += 7
        elif job_title:
            score += 7
        
        # Data completeness (0-10)
        required_fields = ["email", "first_name", "last_name", "company_name", "job_title"]
        completed_fields = sum(1 for field in required_fields if prospect_data.get(field))
        score += int((completed_fields / len(required_fields)) * 10)
        
        logger.debug(f"Firmographic score calculated: {score}/100 for {prospect_data.get('email')}")
        
        return score

    async def process_prospects(
        self,
        prospects: List[Dict[str, Any]],
        campaign_id: UUID,
        organization_id: UUID,
        target_criteria: Optional[Dict[str, Any]] = None,
        enrich: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Process a list of prospects: enrich, check duplicates, score.
        
        Args:
            prospects: List of prospect data dictionaries
            campaign_id: Campaign ID
            organization_id: Organization ID
            target_criteria: Target criteria for scoring (optional)
            enrich: Whether to enrich data using RocketReach (default: True)
            
        Returns:
            List of processed prospects with enrichment and scoring
        """
        processed = []
        
        for prospect in prospects:
            # Check for duplicate
            email = prospect.get("email")
            if not email:
                logger.warning("Prospect missing email, skipping")
                continue
            
            duplicate = self.check_duplicate(email, campaign_id, organization_id)
            if duplicate:
                logger.debug(f"Skipping duplicate prospect: {email}")
                continue
            
            # Enrich data if requested
            if enrich:
                prospect = await self.enrich_prospect_data(prospect)
            
            # Calculate firmographic score
            firmographic_score = self.calculate_firmographic_score(
                prospect,
                target_criteria=target_criteria,
            )
            
            prospect["firmographic_score"] = firmographic_score
            
            processed.append(prospect)
        
        # Sort by firmographic score (descending)
        processed.sort(key=lambda x: x.get("firmographic_score", 0), reverse=True)
        
        logger.info(f"Processed {len(processed)} prospects (skipped {len(prospects) - len(processed)} duplicates)")
        
        return processed
