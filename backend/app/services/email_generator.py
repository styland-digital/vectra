"""Email generation service — uses Claude (Anthropic) for personalized B2B outreach."""

from typing import Dict, Any, Optional

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def _get_api_key() -> Optional[str]:
    return settings.ANTHROPIC_API_KEY or settings.CLAUDE_API_KEY


def _get_anthropic_client():
    """Return a synchronous Anthropic client (for non-async callers)."""
    api_key = _get_api_key()
    if not api_key:
        return None
    try:
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    except Exception as exc:
        logger.warning(f"Failed to init Anthropic client: {exc}")
        return None


def _get_async_anthropic_client():
    """Return an async Anthropic client for use in async contexts."""
    api_key = _get_api_key()
    if not api_key:
        return None
    try:
        import anthropic
        return anthropic.AsyncAnthropic(api_key=api_key)
    except Exception as exc:
        logger.warning(f"Failed to init async Anthropic client: {exc}")
        return None


class EmailGeneratorService:
    """
    Generates personalized B2B prospection emails.

    When ANTHROPIC_API_KEY is configured, Claude writes a fully tailored email
    (subject + HTML body) based on lead profile and campaign context.
    Falls back to a professional template if Claude is unavailable.
    """

    @staticmethod
    async def generate_email_async(
        lead_data: Dict[str, Any],
        campaign: Dict[str, Any],
        calendly_url: Optional[str] = None,
    ) -> Dict[str, str]:
        """Async version of generate_email — uses AsyncAnthropic for pipeline compatibility."""
        client = _get_async_anthropic_client()
        if client:
            try:
                return await EmailGeneratorService._generate_with_claude_async(
                    client, lead_data, campaign, calendly_url
                )
            except Exception as exc:
                logger.error(f"Claude async email generation failed, falling back to template: {exc}")

        return EmailGeneratorService._generate_template(lead_data, campaign, calendly_url)

    @staticmethod
    def generate_email(
        lead_data: Dict[str, Any],
        campaign: Dict[str, Any],
        calendly_url: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Generate subject + HTML body for a prospection email.

        Args:
            lead_data:     Lead fields (first_name, last_name, job_title, company_name, …)
            campaign:      Campaign context (product_description, value_prop, …)
            calendly_url:  Pre-filled Calendly link to embed in CTA (optional)

        Returns:
            {"subject": str, "body": str}  — body is HTML
        """
        client = _get_anthropic_client()
        if client:
            try:
                return EmailGeneratorService._generate_with_claude(
                    client, lead_data, campaign, calendly_url
                )
            except Exception as exc:
                logger.error(f"Claude email generation failed, falling back to template: {exc}")

        return EmailGeneratorService._generate_template(lead_data, campaign, calendly_url)

    # ── Claude generation ──────────────────────────────────────────────────────

    @staticmethod
    def _generate_with_claude(
        client,
        lead_data: Dict[str, Any],
        campaign: Dict[str, Any],
        calendly_url: Optional[str],
    ) -> Dict[str, str]:
        first_name   = lead_data.get("first_name", "")
        last_name    = lead_data.get("last_name", "")
        job_title    = lead_data.get("job_title", "")
        company_name = lead_data.get("company_name", "")
        product_desc = campaign.get("product_description", "Vectra — agents IA de prospection B2B")
        value_prop   = campaign.get("value_prop", "automatiser votre pipeline de ventes B2B")

        cta = (
            f'<a href="{calendly_url}" style="background:#2E5BFF;color:#fff;padding:12px 24px;'
            f'text-decoration:none;border-radius:6px;display:inline-block;font-weight:600;">'
            f'Réserver un créneau de 15 min</a>'
            if calendly_url
            else "<p>Seriez-vous disponible pour un échange de 15 minutes cette semaine ?</p>"
        )

        prompt = f"""Tu es un expert en prospection B2B. Rédige un email de prospection court et percutant.

PROFIL DU PROSPECT :
- Prénom : {first_name or 'N/A'}
- Nom : {last_name or 'N/A'}
- Titre : {job_title or 'N/A'}
- Entreprise : {company_name or 'N/A'}

CONTEXTE PRODUIT :
- Description : {product_desc}
- Proposition de valeur : {value_prop}

CONTRAINTES :
- Longueur : 3 à 4 paragraphes courts (max 150 mots au total)
- Ton : professionnel, direct, personnalisé — pas de formules génériques
- body_text commence DIRECTEMENT par le premier paragraphe de fond — SANS salutation, SANS prénom, SANS "Bonjour", SANS "Madame/Monsieur"
- Ne mentionne PAS de ROI ou pourcentages inventés
- Termine par une question ouverte simple pour encourager la réponse
- Langue : français

INSTRUCTIONS DE FORMAT :
Réponds UNIQUEMENT avec ce JSON (pas de markdown, pas d'explication) :
{{"subject": "...", "body_text": "..."}}

body_text = texte brut de l'email (sans HTML, sans salutation initiale, sans signature)"""

        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        import json
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        parsed = json.loads(raw.strip())

        subject   = parsed["subject"]
        body_text = parsed["body_text"]

        # Wrap text in HTML preserving paragraphs
        paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]
        html_paras = "".join(f"<p>{p}</p>" for p in paragraphs)

        salutation = f"<p>Bonjour {first_name}," if first_name else "<p>Bonjour,"
        body_html = f"""<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#222;">
{salutation}</p>
{html_paras}
{cta}
<p style="margin-top:24px;">Cordialement,<br><strong>L'équipe Vectra</strong></p>
</div>"""

        logger.info(f"Claude generated email for {first_name} {last_name} @ {company_name}")
        return {"subject": subject, "body": body_html}

    @staticmethod
    async def _generate_with_claude_async(
        client,
        lead_data: Dict[str, Any],
        campaign: Dict[str, Any],
        calendly_url: Optional[str],
    ) -> Dict[str, str]:
        first_name   = lead_data.get("first_name", "")
        last_name    = lead_data.get("last_name", "")
        job_title    = lead_data.get("job_title", "")
        company_name = lead_data.get("company_name", "")
        product_desc = campaign.get("product_description", "Vectra — agents IA de prospection B2B")
        value_prop   = campaign.get("value_prop", "automatiser votre pipeline de ventes B2B")

        cta = (
            f'<a href="{calendly_url}" style="background:#2E5BFF;color:#fff;padding:12px 24px;'
            f'text-decoration:none;border-radius:6px;display:inline-block;font-weight:600;">'
            f'Réserver un créneau de 15 min</a>'
            if calendly_url
            else "<p>Seriez-vous disponible pour un échange de 15 minutes cette semaine ?</p>"
        )

        prompt = f"""Tu es un expert en prospection B2B. Rédige un email de prospection court et percutant.

PROFIL DU PROSPECT :
- Prénom : {first_name or 'N/A'}
- Nom : {last_name or 'N/A'}
- Titre : {job_title or 'N/A'}
- Entreprise : {company_name or 'N/A'}

CONTEXTE PRODUIT :
- Description : {product_desc}
- Proposition de valeur : {value_prop}

CONTRAINTES :
- Longueur : 3 à 4 paragraphes courts (max 150 mots au total)
- Ton : professionnel, direct, personnalisé — pas de formules génériques
- body_text commence DIRECTEMENT par le premier paragraphe de fond — SANS salutation, SANS prénom, SANS "Bonjour", SANS "Madame/Monsieur"
- Ne mentionne PAS de ROI ou pourcentages inventés
- Termine par une question ouverte simple pour encourager la réponse
- Langue : français

INSTRUCTIONS DE FORMAT :
Réponds UNIQUEMENT avec ce JSON (pas de markdown, pas d'explication) :
{{"subject": "...", "body_text": "..."}}

body_text = texte brut de l'email (sans HTML, sans salutation initiale, sans signature)"""

        response = await client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        import json
        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        parsed = json.loads(raw.strip())

        subject   = parsed["subject"]
        body_text = parsed["body_text"]

        paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]
        html_paras = "".join(f"<p>{p}</p>" for p in paragraphs)

        salutation = f"<p>Bonjour {first_name}," if first_name else "<p>Bonjour,"
        body_html = f"""<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#222;">
{salutation}</p>
{html_paras}
{cta}
<p style="margin-top:24px;">Cordialement,<br><strong>L'équipe Vectra</strong></p>
</div>"""

        logger.info(f"Claude (async) generated email for {first_name} {last_name} @ {company_name}")
        return {"subject": subject, "body": body_html}

    # ── Template fallback ──────────────────────────────────────────────────────

    @staticmethod
    def _generate_template(
        lead_data: Dict[str, Any],
        campaign: Dict[str, Any],
        calendly_url: Optional[str],
    ) -> Dict[str, str]:
        first_name   = lead_data.get("first_name", "")
        job_title    = lead_data.get("job_title", "")
        company_name = lead_data.get("company_name", "")
        value_prop   = campaign.get("value_prop") or "Automatiser votre prospection B2B"
        product_desc = campaign.get("product_description") or "Notre solution d'agents IA pour la prospection"

        subject = (
            f"{first_name}, {value_prop} pour {company_name or 'votre équipe'}"
            if first_name
            else f"{value_prop} pour {company_name or 'votre équipe'}"
        )

        salutation = f"<p>Bonjour {first_name}," if first_name else "<p>Bonjour,"

        cta = (
            f'<p><a href="{calendly_url}" style="background:#2E5BFF;color:#fff;padding:12px 24px;'
            f'text-decoration:none;border-radius:6px;display:inline-block;">Réserver un créneau</a></p>'
            if calendly_url
            else "<p>Seriez-vous intéressé(e) par une démonstration de 15 minutes ?</p>"
        )

        body = f"""<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#222;">
{salutation}</p>
<p>J'ai remarqué que vous êtes <strong>{job_title or "professionnel"}</strong> chez <strong>{company_name}</strong>.</p>
<p>{product_desc}</p>
<p><strong>{value_prop}</strong></p>
{cta}
<p style="margin-top:24px;">Cordialement,<br><strong>L'équipe Vectra</strong></p>
</div>"""

        return {"subject": subject, "body": body}

    # ── Legacy static methods (kept for backward compatibility) ───────────────

    @staticmethod
    def generate_subject(lead_data: Dict[str, Any], campaign: Dict[str, Any]) -> str:
        return EmailGeneratorService._generate_template(lead_data, campaign, None)["subject"]

    @staticmethod
    def generate_body(
        lead_data: Dict[str, Any],
        campaign: Dict[str, Any],
        calendly_url: Optional[str] = None,
    ) -> str:
        return EmailGeneratorService._generate_template(lead_data, campaign, calendly_url)["body"]
