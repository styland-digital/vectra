"""RocketReach API integration for prospect finding and enrichment."""

from typing import Dict, List, Any, Optional, Tuple
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

ROCKETREACH_BASE_URL = "https://api.rocketreach.co/v2"
ROCKETREACH_RATE_LIMIT = 50  # requests per minute


def _split_name(full_name: str) -> Tuple[str, str]:
    """Split 'First Last' into (first, last)."""
    parts = (full_name or "").strip().split()
    if len(parts) >= 2:
        return parts[0], " ".join(parts[1:])
    return full_name or "", ""


def _construct_email(first_name: str, last_name: str, domain: str) -> Optional[str]:
    """
    Construct a likely professional email from name + domain.
    Returns None when insufficient data.
    """
    if not first_name or not domain:
        return None
    fn = first_name.lower().replace(" ", "").replace("-", "").replace("'", "")
    ln = last_name.lower().replace(" ", "").replace("-", "").replace("'", "") if last_name else ""
    if ln:
        return f"{fn}.{ln}@{domain}"
    return f"{fn}@{domain}"


def _normalize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw RocketReach search profile to Vectra's internal format.

    The search API returns teaser data only — email domains, not full addresses.
    We construct a likely professional email when possible.
    """
    full_name = profile.get("name", "")
    first_name, last_name = _split_name(full_name)

    # Prefer professional email domain, fall back to any domain
    teaser = profile.get("teaser") or {}
    pro_emails = teaser.get("professional_emails") or []
    all_emails = teaser.get("emails") or []
    domain = (pro_emails or all_emails or [None])[0]

    # Attempt to construct a professional email from name + domain
    email = _construct_email(first_name, last_name, domain) if domain else None

    return {
        "rocketreach_id": profile.get("id"),
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "email_domain": domain,
        "email_verified": False,
        "job_title": profile.get("current_title"),
        "company_name": profile.get("current_employer"),
        "company_domain": profile.get("current_employer_domain"),
        "linkedin_url": profile.get("linkedin_url"),
        "location": profile.get("location"),
        "city": profile.get("city"),
        "country": profile.get("country"),
        "seniority_level": profile.get("seniority_level"),
        "source": "rocketreach",
        "enrichment_data": profile,
    }


class RocketReachService:
    """Service for interacting with RocketReach API."""

    def __init__(self, api_key: Optional[str] = None):
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
        reraise=True,
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
        Search for people using the RocketReach v2 API.

        Args:
            job_titles:    Filter by current job title (e.g., ["CEO", "CTO"])
            companies:     Filter by employer name
            locations:     Filter by location string (e.g., ["France", "Paris"])
            company_sizes: Filter by employee count range (e.g., ["11-50", "51-200"])
            industries:    Filter by industry keyword
            limit:         Maximum results to return (capped at 100)

        Returns:
            List of normalized prospect dicts (email may be constructed / unverified).
        """
        if not self.api_key:
            logger.error("RocketReach API key not configured")
            return []

        # Build the query object — only include non-empty filters
        query: Dict[str, Any] = {}

        if job_titles:
            query["current_title"] = job_titles
        if companies:
            query["current_employer"] = companies
        if locations:
            query["location"] = locations
        if company_sizes:
            query["company_size"] = company_sizes
        if industries:
            query["current_employer_industry"] = industries

        payload = {
            "query": query,
            "start": 1,
            "page_size": min(limit, 100),
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/search",
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()

                data = response.json()
                raw_profiles = data.get("profiles", [])

                logger.info(
                    f"RocketReach search returned {len(raw_profiles)} profiles "
                    f"(total available: {data.get('pagination', {}).get('total', '?')})"
                )

                normalized = [_normalize_profile(p) for p in raw_profiles]
                return normalized

        except httpx.HTTPStatusError as e:
            logger.error(
                f"RocketReach API error: {e.response.status_code} — {e.response.text}"
            )
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
        reraise=True,
    )
    async def lookup_person(
        self,
        rocketreach_id: Optional[int] = None,
        linkedin_url: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Look up a specific person's full profile (requires lookup credits).

        Returns verified email and full contact data, or None if not found / no credits.
        """
        if not self.api_key:
            logger.error("RocketReach API key not configured")
            return None

        query: Dict[str, Any] = {}
        if rocketreach_id:
            query["id"] = rocketreach_id
        if linkedin_url:
            query["linkedin_url"] = linkedin_url
        if email:
            query["email"] = email
        if first_name:
            query["first_name"] = first_name
        if last_name:
            query["last_name"] = last_name
        if company:
            query["current_employer"] = company

        if not query:
            logger.warning("No lookup criteria provided")
            return None

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/lookupProfile",
                    headers=self.headers,
                    json=query,
                )
                response.raise_for_status()

                data = response.json()
                logger.info(f"RocketReach lookup successful for {query}")
                return data

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.debug(f"Person not found in RocketReach: {query}")
                return None
            if e.response.status_code == 403:
                logger.warning("RocketReach lookup requires credits — using search data only")
                return None
            logger.error(
                f"RocketReach lookup error: {e.response.status_code} — {e.response.text}"
            )
            if e.response.status_code == 429:
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
        """Enrich prospect data via lookup (requires credits)."""
        profile = await self.lookup_person(
            linkedin_url=linkedin_url,
            email=email,
            first_name=first_name,
            last_name=last_name,
            company=company,
        )
        if not profile:
            return {}

        first, last = _split_name(profile.get("name", ""))
        return {
            "email": profile.get("email"),
            "phone": (profile.get("phone_numbers") or [{}])[0].get("number"),
            "first_name": profile.get("first_name") or first,
            "last_name": profile.get("last_name") or last,
            "job_title": profile.get("current_title"),
            "company_name": profile.get("current_employer"),
            "linkedin_url": profile.get("linkedin_url"),
            "location": profile.get("location"),
            "company_domain": profile.get("current_employer_domain"),
            "seniority_level": profile.get("seniority_level"),
            "raw_data": profile,
        }
