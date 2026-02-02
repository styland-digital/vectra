"""BANT qualifier agent."""

from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.agents.base import BaseVectraAgent
from app.agents.bant.prompts import BANT_MAIN_PROMPT
from app.services.scoring import BANTScoringService
from app.db.models.lead import Lead, LeadStatus
from app.core.logging import get_logger

logger = get_logger(__name__)


class BANTAgent(BaseVectraAgent):
    """
    Agent BANT: Qualifies leads using BANT framework.
    
    Responsibilities:
    - Analyze lead profile and enrichment data
    - Calculate BANT score (Budget, Authority, Need, Timeline)
    - Determine qualification status
    - Update lead status in database
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None,
    ):
        """
        Initialize BANT agent.
        
        Args:
            config: Agent configuration
            db: Database session (optional, required for updating leads)
        """
        super().__init__(config)
        self.db = db
        self.scoring_service = BANTScoringService()

    def _get_role(self) -> str:
        """Return the agent's role."""
        return "BANT Qualification Expert"

    def _get_goal(self) -> str:
        """Return the agent's goal."""
        return "Qualifier des prospects en utilisant le framework BANT (Budget, Authority, Need, Timeline) pour déterminer s'ils sont prêts pour une démonstration produit."

    def _get_backstory(self) -> str:
        """Return the agent's backstory."""
        return """Tu es un expert en qualification commerciale B2B avec plus de 15 ans d'expérience.
        Tu maîtrises parfaitement le framework BANT et tu sais analyser des profils pour évaluer
        leur budget, leur autorité décisionnelle, leur besoin et leur timeline d'achat."""

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute BANT qualification.
        
        Args:
            input_data: Input data with lead information:
                - lead_id: UUID (optional)
                - lead_data: Dict with lead fields (email, job_title, company_size, etc.)
                - campaign: Dict with campaign info (product_description, bant_threshold, etc.)
                
        Returns:
            Result dictionary with BANT score and qualification status
        """
        try:
            lead_data = input_data.get("lead_data", {})
            campaign = input_data.get("campaign", {})
            lead_id = input_data.get("lead_id")
            
            if not lead_data:
                raise ValueError("lead_data is required")
            
            # Extract lead information
            company_size = lead_data.get("company_size")
            job_title = lead_data.get("job_title")
            enrichment_data = lead_data.get("enrichment_data", {})
            industry = lead_data.get("company_industry") or lead_data.get("company_name")
            linkedin_url = lead_data.get("linkedin_url")
            
            # Calculate BANT score using scoring service
            bant_result = self.scoring_service.calculate_bant_score(
                company_size=company_size,
                job_title=job_title,
                enrichment_data=enrichment_data,
                industry=industry,
                linkedin_url=linkedin_url,
            )
            
            bant_score = bant_result["bant_score"]
            bant_breakdown = bant_result["bant_breakdown"]
            qualified = bant_result["qualified"]
            
            # Update lead in database if lead_id provided
            if lead_id and self.db:
                lead = self.db.query(Lead).filter(Lead.id == UUID(lead_id)).first()
                if lead:
                    lead.bant_score = bant_score
                    lead.bant_breakdown = bant_breakdown
                    lead.status = LeadStatus.QUALIFIED if qualified else LeadStatus.REJECTED
                    self.db.commit()
                    self.logger.info(f"Updated lead {lead_id} with BANT score {bant_score}")
            
            result = {
                "bant_score": bant_score,
                "bant_breakdown": bant_breakdown,
                "qualified": qualified,
                "recommendation": bant_result["recommendation"],
            }
            
            self.logger.info(
                f"BANT qualification completed: score={bant_score}, qualified={qualified}"
            )
            
            return {
                "success": True,
                "data": result,
            }
            
        except Exception as e:
            self.logger.error(f"Error in BANT agent: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "data": {
                    "bant_score": 0,
                    "qualified": False,
                },
            }
