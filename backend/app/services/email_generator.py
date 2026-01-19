"""Email generation service for personalized outreach."""

from typing import Dict, Any, Optional

from app.core.logging import get_logger

logger = get_logger(__name__)


class EmailGeneratorService:
    """Service for generating personalized emails."""

    @staticmethod
    def generate_subject(lead_data: Dict[str, Any], campaign: Dict[str, Any]) -> str:
        """
        Generate email subject.
        
        Args:
            lead_data: Lead data dictionary
            campaign: Campaign data dictionary
            
        Returns:
            Email subject string
        """
        first_name = lead_data.get("first_name", "")
        company_name = lead_data.get("company_name", "")
        value_prop = campaign.get("value_prop", "Automatiser votre prospection")
        
        if first_name:
            return f"{first_name}, {value_prop} pour {company_name or 'votre équipe'}"
        else:
            return f"{value_prop} pour {company_name or 'votre équipe'}"

    @staticmethod
    def generate_body(lead_data: Dict[str, Any], campaign: Dict[str, Any], calendly_url: Optional[str] = None) -> str:
        """
        Generate email body.
        
        Args:
            lead_data: Lead data dictionary
            campaign: Campaign data dictionary
            calendly_url: Calendly scheduling URL (optional)
            
        Returns:
            Email body HTML string
        """
        first_name = lead_data.get("first_name", "")
        job_title = lead_data.get("job_title", "")
        company_name = lead_data.get("company_name", "")
        value_prop = campaign.get("value_prop", "Automatiser votre prospection B2B")
        product_description = campaign.get("product_description", "Notre solution d'agents IA pour la prospection")
        
        salutation = f"Bonjour {first_name}," if first_name else "Bonjour,"
        
        body_parts = [
            f"<p>{salutation}</p>",
            f"<p>J'ai remarqué que vous êtes {job_title or 'dans le domaine'} chez <strong>{company_name}</strong>.</p>",
            f"<p>{product_description}</p>",
            f"<p><strong>{value_prop}</strong></p>",
        ]
        
        if calendly_url:
            body_parts.append(
                f'<p><a href="{calendly_url}" style="background-color: #2E5BFF; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Réserver un créneau</a></p>'
            )
        else:
            body_parts.append(
                "<p>Seriez-vous intéressé(e) par une démonstration de 15 minutes ?</p>"
            )
        
        body_parts.append("<p>Cordialement,<br>L'équipe Vectra</p>")
        
        return "\n".join(body_parts)

    @staticmethod
    def generate_email(lead_data: Dict[str, Any], campaign: Dict[str, Any], calendly_url: Optional[str] = None) -> Dict[str, str]:
        """
        Generate complete email (subject + body).
        
        Args:
            lead_data: Lead data dictionary
            campaign: Campaign data dictionary
            calendly_url: Calendly scheduling URL (optional)
            
        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        subject = EmailGeneratorService.generate_subject(lead_data, campaign)
        body = EmailGeneratorService.generate_body(lead_data, campaign, calendly_url)
        
        return {
            "subject": subject,
            "body": body,
        }
