"""RocketReach API integration for prospect finding and enrichment."""

from typing import Dict, List, Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# RocketReach API endpoints
ROCKETREACH_BASE_URL = "https://api.rocketreach.co/v2"
ROCKETREACH_RATE_LIMIT = 50  # requests per minute


class RocketReachService:
    """Service for interacting with RocketReach API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize RocketReach service.
        
        Args:
            api_key: RocketReach API key (defaults to settings)
        """
        self.api_key = api_key or settings.ROCKETREACH_API_KEY
        if not self.api_key:
            logger.warning("ROCKETREACH_API_KEY not configured")
        
        self.base_url = ROCKETREACH_BASE_URL
        self.headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
        } if self.api_key else {}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def search_people(
        self,
        job_titles: Optional[List[str]] = None,
        companies: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        company_sizes: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search for people using RocketReach API.
        
        Args:
            job_titles: List of job titles to search for
            companies: List of company names
            locations: List of locations (e.g., ["France", "Paris"])
            company_sizes: List of company sizes (e.g., ["51-200", "201-500"])
            industries: List of industries
            limit: Maximum number of results (default: 50)
            
        Returns:
            List of prospect data dictionaries
        """
        if not self.api_key:
            logger.error("RocketReach API key not configured")
            return []
        
        # Build search query
        query = {}
        
        if job_titles:
            query["job_titles"] = job_titles
        
        if companies:
            query["companies"] = companies
        
        if locations:
            query["locations"] = locations
        
        if company_sizes:
            query["company_sizes"] = company_sizes
        
        if industries:
            query["industries"] = industries
        
        query["limit"] = min(limit, 100)  # RocketReach max is 100
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/search/profile",
                    headers=self.headers,
                    json=query,
                )
                response.raise_for_status()
                
                data = response.json()
                profiles = data.get("profiles", [])
                
                logger.info(f"RocketReach search returned {len(profiles)} profiles")
                
                return profiles
                
        except httpx.HTTPStatusError as e:
            logger.error(f"RocketReach API error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded, will retry with exponential backoff")
                raise
            return []
        except Exception as e:
            logger.error(f"Error searching RocketReach: {e}", exc_info=True)
            return []

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def lookup_person(
        self,
        email: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Look up a specific person's profile using RocketReach API.
        
        Args:
            email: Email address
            linkedin_url: LinkedIn profile URL
            first_name: First name
            last_name: Last name
            company: Company name
            
        Returns:
            Person profile data or None
        """
        if not self.api_key:
            logger.error("RocketReach API key not configured")
            return None
        
        # Build lookup query
        query = {}
        
        if email:
            query["email"] = email
        if linkedin_url:
            query["linkedin_url"] = linkedin_url
        if first_name:
            query["first_name"] = first_name
        if last_name:
            query["last_name"] = last_name
        if company:
            query["company"] = company
        
        if not query:
            logger.warning("No lookup criteria provided")
            return None
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/lookup/person",
                    headers=self.headers,
                    json=query,
                )
                response.raise_for_status()
                
                data = response.json()
                profile = data.get("person", {})
                
                logger.info(f"RocketReach lookup successful for {query}")
                
                return profile
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.debug(f"Person not found in RocketReach: {query}")
                return None
            logger.error(f"RocketReach API error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded, will retry with exponential backoff")
                raise
            return None
        except Exception as e:
            logger.error(f"Error looking up person in RocketReach: {e}", exc_info=True)
            return None

    async def enrich_prospect(
        self,
        email: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Enrich prospect data using RocketReach API.
        
        Args:
            email: Email address
            linkedin_url: LinkedIn profile URL
            first_name: First name
            last_name: Last name
            company: Company name
            
        Returns:
            Enriched prospect data dictionary
        """
        profile = await self.lookup_person(
            email=email,
            linkedin_url=linkedin_url,
            first_name=first_name,
            last_name=last_name,
            company=company,
        )
        
        if not profile:
            return {}
        
        # Extract and normalize data
        enriched_data = {
            "email": profile.get("email"),
            "phone": profile.get("phone_numbers", [{}])[0].get("number") if profile.get("phone_numbers") else None,
            "first_name": profile.get("first_name"),
            "last_name": profile.get("last_name"),
            "job_title": profile.get("current_title"),
            "company_name": profile.get("current_employer"),
            "linkedin_url": profile.get("linkedin_url"),
            "location": profile.get("location"),
            "company_domain": profile.get("current_employer_domain"),
            "company_size": profile.get("current_employer_size"),
            "company_industry": profile.get("current_employer_industry"),
            "seniority_level": profile.get("seniority_level"),
            "raw_data": profile,  # Store raw response for reference
        }
        
        logger.info(f"Enriched prospect data for {enriched_data.get('email')}")
        
        return enriched_data
