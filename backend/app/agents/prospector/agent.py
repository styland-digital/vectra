"""Prospector agent for finding and enriching prospects."""

from typing import Dict, List, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from crewai import Task

from app.agents.base import BaseVectraAgent
from app.agents.prospector.prompts import (
    PROSPECTOR_MAIN_PROMPT,
    PROSPECTOR_ANALYSIS_PROMPT,
    PROSPECTOR_ENRICHMENT_PROMPT,
)
from app.services.rocketreach import RocketReachService
from app.services.enrichment import EnrichmentService
from app.core.logging import get_logger

logger = get_logger(__name__)


class ProspectorAgent(BaseVectraAgent):
    """
    Agent Prospector: Finds and enriches prospects based on search criteria.
    
    Responsibilities:
    - Search for prospects using RocketReach API
    - Enrich prospect data
    - Check for duplicates
    - Score prospects by firmographic priority
    - Return sorted list of qualified prospects
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None,
        rocketreach_service: Optional[RocketReachService] = None,
    ):
        """
        Initialize Prospector agent.
        
        Args:
            config: Agent configuration
            db: Database session (optional, required for duplicate checking)
            rocketreach_service: RocketReach service instance (optional)
        """
        super().__init__(config)
        self.db = db
        self.rocketreach_service = rocketreach_service or RocketReachService()
        self.enrichment_service = (
            EnrichmentService(db, self.rocketreach_service) if db else None
        )

    def _get_role(self) -> str:
        """Return the agent's role."""
        return "Prospector B2B Expert"

    def _get_goal(self) -> str:
        """Return the agent's goal."""
        return "Trouver et enrichir des prospects qualifiés selon les critères de recherche de la campagne."

    def _get_backstory(self) -> str:
        """Return the agent's backstory."""
        return """Tu es un expert en prospection B2B avec plus de 10 ans d'expérience.
        Tu es spécialisé dans la recherche de prospects qualifiés, l'enrichissement de données,
        et l'évaluation de la pertinence firmographique. Tu utilises des outils comme RocketReach
        pour trouver des contacts professionnels et tu sais identifier les signaux positifs
        ainsi que les objections potentielles."""

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute prospection task.
        
        Args:
            input_data: Input data with search criteria:
                - campaign_id: UUID
                - organization_id: UUID
                - job_titles: List[str]
                - industries: List[str] (optional)
                - company_sizes: List[str] (optional)
                - locations: List[str] (optional)
                - limit: int (default: 50)
                - target_criteria: Dict (optional, for scoring)
                
        Returns:
            Result dictionary with prospects list and metadata
        """
        try:
            # Extract input parameters
            campaign_id = input_data.get("campaign_id")
            organization_id = input_data.get("organization_id")
            job_titles = input_data.get("job_titles", [])
            industries = input_data.get("industries", [])
            company_sizes = input_data.get("company_sizes", [])
            locations = input_data.get("locations", [])
            limit = input_data.get("limit", 50)
            target_criteria = input_data.get("target_criteria", {})
            
            if not campaign_id or not organization_id:
                raise ValueError("campaign_id and organization_id are required")
            
            if not job_titles:
                raise ValueError("job_titles are required")
            
            self.logger.info(
                f"Starting prospection for campaign {campaign_id} "
                f"with {len(job_titles)} job titles"
            )
            
            # Step 1: Search for prospects using RocketReach
            raw_prospects = await self.rocketreach_service.search_people(
                job_titles=job_titles,
                industries=industries if industries else None,
                company_sizes=company_sizes if company_sizes else None,
                locations=locations if locations else None,
                limit=limit,
            )
            
            if not raw_prospects:
                self.logger.warning("No prospects found from RocketReach")
                return {
                    "success": True,
                    "data": {
                        "prospects": [],
                        "total_found": 0,
                        "total_qualified": 0,
                    },
                }
            
            self.logger.info(f"Found {len(raw_prospects)} raw prospects from RocketReach")
            
            # Step 2: Process prospects (enrich, check duplicates, score)
            if self.enrichment_service:
                processed_prospects = await self.enrichment_service.process_prospects(
                    prospects=raw_prospects,
                    campaign_id=UUID(campaign_id),
                    organization_id=UUID(organization_id),
                    target_criteria=target_criteria,
                    enrich=True,
                )
            else:
                # Without DB, just score them manually
                enrichment_service_temp = EnrichmentService(None, self.rocketreach_service)
                processed_prospects = []
                for prospect in raw_prospects:
                    score = enrichment_service_temp.calculate_firmographic_score(
                        prospect,
                        target_criteria=target_criteria,
                    )
                    prospect["firmographic_score"] = score
                    processed_prospects.append(prospect)
            
            # Step 3: Filter and sort by score
            qualified_prospects = [
                p for p in processed_prospects
                if p.get("firmographic_score", 0) >= 50  # Minimum threshold
            ]
            
            # Step 4: Use LLM to analyze top prospects if enabled
            # For now, we'll skip LLM analysis and rely on firmographic scoring
            # This can be added later for more sophisticated analysis
            
            result = {
                "prospects": qualified_prospects[:limit],  # Return top N
                "total_found": len(raw_prospects),
                "total_processed": len(processed_prospects),
                "total_qualified": len(qualified_prospects),
            }
            
            self.logger.info(
                f"Prospection completed: {len(qualified_prospects)} qualified prospects "
                f"out of {len(raw_prospects)} found"
            )
            
            return {
                "success": True,
                "data": result,
            }
            
        except Exception as e:
            self.logger.error(f"Error in prospector agent: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "data": {
                    "prospects": [],
                    "total_found": 0,
                    "total_qualified": 0,
                },
            }
