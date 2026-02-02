"""Scheduler agent for generating and sending personalized emails."""

from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.agents.base import BaseVectraAgent
from app.agents.scheduler.prompts import SCHEDULER_MAIN_PROMPT
from app.services.email_generator import EmailGeneratorService
from app.services.calendly import CalendlyService
from app.services.resend import send_email
from app.db.models.lead import Lead, LeadStatus
from app.db.models.email import Email, EmailStatus
from app.core.logging import get_logger

logger = get_logger(__name__)


class SchedulerAgent(BaseVectraAgent):
    """
    Agent Scheduler: Generates personalized emails and schedules meetings.
    
    Responsibilities:
    - Generate personalized email content
    - Create Calendly scheduling links
    - Send emails via Resend
    - Update lead and email status in database
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None,
    ):
        """
        Initialize Scheduler agent.
        
        Args:
            config: Agent configuration
            db: Database session (optional, required for saving emails)
        """
        super().__init__(config)
        self.db = db
        self.email_generator = EmailGeneratorService()
        self.calendly_service = CalendlyService()

    def _get_role(self) -> str:
        """Return the agent's role."""
        return "Email Outreach Specialist"

    def _get_goal(self) -> str:
        """Return the agent's goal."""
        return "Générer et envoyer des emails personnalisés de prospection B2B avec proposition de rendez-vous."

    def _get_backstory(self) -> str:
        """Return the agent's backstory."""
        return """Tu es un expert en email marketing B2B avec plus de 10 ans d'expérience.
        Tu sais créer des emails personnalisés qui génèrent des réponses positives et tu utilises
        des outils comme Calendly pour faciliter la prise de rendez-vous."""

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute email generation and sending.
        
        Args:
            input_data: Input data with lead and campaign information:
                - lead_id: UUID (optional)
                - lead_data: Dict with lead fields
                - campaign: Dict with campaign info
                - send_email: bool (default: False, only generate)
                
        Returns:
            Result dictionary with email content and sending status
        """
        try:
            lead_data = input_data.get("lead_data", {})
            campaign = input_data.get("campaign", {})
            lead_id = input_data.get("lead_id")
            should_send = input_data.get("send_email", False)
            
            if not lead_data:
                raise ValueError("lead_data is required")
            
            # Generate Calendly link
            lead_email = lead_data.get("email")
            lead_name = f"{lead_data.get('first_name', '')} {lead_data.get('last_name', '')}".strip()
            
            calendly_url = self.calendly_service.generate_scheduling_link(
                lead_email=lead_email,
                lead_name=lead_name if lead_name else None,
            )
            
            # Generate email content
            email_content = self.email_generator.generate_email(
                lead_data=lead_data,
                campaign=campaign,
                calendly_url=calendly_url,
            )
            
            subject = email_content["subject"]
            body = email_content["body"]
            
            # Save email to database if lead_id provided
            email_id = None
            if lead_id and self.db:
                lead = self.db.query(Lead).filter(Lead.id == UUID(lead_id)).first()
                if lead:
                    email = Email(
                        lead_id=lead.id,
                        campaign_id=lead.campaign_id,
                        subject=subject,
                        body=body,
                        status=EmailStatus.PENDING,
                    )
                    self.db.add(email)
                    self.db.commit()
                    email_id = str(email.id)
            
            # Send email if requested
            sent = False
            if should_send and lead_email:
                try:
                    send_email(
                        to=lead_email,
                        subject=subject,
                        html_content=body,
                        from_name="Vectra",
                    )
                    
                    # Update email status
                    if email_id and self.db:
                        email = self.db.query(Email).filter(Email.id == UUID(email_id)).first()
                        if email:
                            email.status = EmailStatus.SENT
                            self.db.commit()
                    
                    # Update lead status
                    if lead_id and self.db:
                        lead = self.db.query(Lead).filter(Lead.id == UUID(lead_id)).first()
                        if lead:
                            lead.status = LeadStatus.CONTACTED
                            self.db.commit()
                    
                    sent = True
                    self.logger.info(f"Email sent to {lead_email}")
                except Exception as e:
                    self.logger.error(f"Failed to send email: {e}", exc_info=True)
            
            result = {
                "email_id": email_id,
                "subject": subject,
                "body": body,
                "calendly_url": calendly_url,
                "sent": sent,
            }
            
            self.logger.info(f"Email generated for {lead_email}, sent={sent}")
            
            return {
                "success": True,
                "data": result,
            }
            
        except Exception as e:
            self.logger.error(f"Error in scheduler agent: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "data": {},
            }
