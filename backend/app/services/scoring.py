"""BANT scoring service."""

from typing import Dict, Any, Optional
import re

from app.core.logging import get_logger

logger = get_logger(__name__)


class BANTScoringService:
    """Service for calculating BANT scores."""

    @staticmethod
    def calculate_budget_score(company_size: Optional[str] = None) -> tuple[int, str]:
        """
        Calculate budget score (0-25) based on company size.
        
        Args:
            company_size: Company size string (e.g., "51-200", "201-500")
            
        Returns:
            Tuple of (score, reasoning)
        """
        if not company_size:
            return (5, "Taille entreprise inconnue")
        
        size_str = str(company_size).lower()
        
        # Extract numbers
        numbers = re.findall(r'\d+', size_str)
        if not numbers:
            return (5, "Taille entreprise non analysable")
        
        max_size = max(int(n) for n in numbers)
        
        if max_size < 10:
            return (5, "Startup early-stage (<10 employés)")
        elif max_size < 30:
            return (8, "PME 10-30 employés, budget limité")
        elif max_size < 100:
            return (13, "PME 30-100 employés, budget probable")
        elif max_size < 500:
            return (18, "ETI 100-500 employés, budget confirmé")
        else:
            return (23, "Grande entreprise, budget dédié")

    @staticmethod
    def calculate_authority_score(job_title: Optional[str] = None) -> tuple[int, str]:
        """
        Calculate authority score (0-25) based on job title.
        
        Args:
            job_title: Job title string
            
        Returns:
            Tuple of (score, reasoning)
        """
        if not job_title:
            return (5, "Poste inconnu")
        
        title_lower = job_title.lower()
        
        # C-Level / Founder
        if any(term in title_lower for term in ['ceo', 'cto', 'cfo', 'coo', 'founder', 'co-founder', 'president']):
            return (23, "C-Level / Founder")
        
        # VP / Head of
        if any(term in title_lower for term in ['vp', 'vice president', 'head of', 'directeur général']):
            return (18, "VP / Head of")
        
        # Director
        if any(term in title_lower for term in ['director', 'directeur', 'directrice']):
            return (13, "Directeur de département")
        
        # Manager
        if any(term in title_lower for term in ['manager', 'responsable', 'chef de']):
            return (8, "Manager d'équipe")
        
        # Individual contributor
        return (5, "Contributeur individuel")

    @staticmethod
    def calculate_need_score(
        enrichment_data: Optional[Dict[str, Any]] = None,
        industry: Optional[str] = None
    ) -> tuple[int, str]:
        """
        Calculate need score (0-25) based on signals.
        
        Args:
            enrichment_data: Enrichment data dictionary
            industry: Industry string
            
        Returns:
            Tuple of (score, reasoning)
        """
        score = 5
        signals = []
        
        if industry:
            signals.append(f"Secteur: {industry}")
            score += 5
        
        if enrichment_data:
            raw_data = enrichment_data.get("raw_data", {})
            
            # Check for signals in enrichment data
            if raw_data.get("current_employer_size"):
                signals.append("Données entreprise disponibles")
                score += 5
            
            if raw_data.get("seniority_level"):
                signals.append("Niveau seniorité identifié")
                score += 3
        
        if score >= 20:
            return (20, "Signaux forts: " + ", ".join(signals))
        elif score >= 15:
            return (15, "Signaux moyens: " + ", ".join(signals) if signals else "Secteur concerné")
        elif score >= 10:
            return (10, "Signaux faibles" + (": " + ", ".join(signals) if signals else ""))
        else:
            return (5, "Pas d'indicateur de besoin clair")

    @staticmethod
    def calculate_timeline_score(
        linkedin_url: Optional[str] = None,
        enrichment_data: Optional[Dict[str, Any]] = None
    ) -> tuple[int, str]:
        """
        Calculate timeline score (0-25) based on activity signals.
        
        Args:
            linkedin_url: LinkedIn profile URL
            enrichment_data: Enrichment data dictionary
            
        Returns:
            Tuple of (score, reasoning)
        """
        score = 10  # Base: activité normale
        
        if linkedin_url:
            score += 3  # Profile exists
        
        if enrichment_data:
            raw_data = enrichment_data.get("raw_data", {})
            if raw_data.get("updated_at"):
                score += 5
                return (15, "Profil LinkedIn récemment mis à jour")
        
        if score >= 15:
            return (15, "Activité récente détectée")
        else:
            return (10, "Activité normale sur LinkedIn")

    @staticmethod
    def calculate_bant_score(
        company_size: Optional[str] = None,
        job_title: Optional[str] = None,
        enrichment_data: Optional[Dict[str, Any]] = None,
        industry: Optional[str] = None,
        linkedin_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Calculate complete BANT score.
        
        Args:
            company_size: Company size
            job_title: Job title
            enrichment_data: Enrichment data
            industry: Industry
            linkedin_url: LinkedIn URL
            
        Returns:
            Dictionary with BANT breakdown and total score
        """
        budget_score, budget_reasoning = BANTScoringService.calculate_budget_score(company_size)
        authority_score, authority_reasoning = BANTScoringService.calculate_authority_score(job_title)
        need_score, need_reasoning = BANTScoringService.calculate_need_score(enrichment_data, industry)
        timeline_score, timeline_reasoning = BANTScoringService.calculate_timeline_score(linkedin_url, enrichment_data)
        
        total_score = budget_score + authority_score + need_score + timeline_score
        
        breakdown = {
            "budget": {
                "score": budget_score,
                "reasoning": budget_reasoning
            },
            "authority": {
                "score": authority_score,
                "reasoning": authority_reasoning
            },
            "need": {
                "score": need_score,
                "reasoning": need_reasoning
            },
            "timeline": {
                "score": timeline_score,
                "reasoning": timeline_reasoning
            }
        }
        
        qualified = total_score >= 60
        
        return {
            "bant_breakdown": breakdown,
            "bant_score": total_score,
            "qualified": qualified,
            "recommendation": "contact" if qualified else ("nurture" if total_score >= 40 else "reject")
        }
