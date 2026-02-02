# VECTRA - PROMPTS & TEMPLATES AGENTS
## Documentation des Prompts LLM
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-006  
**Statut:** APPROUVÉ  
**Objectif:** Documenter tous les prompts utilisés par les agents IA  

---

## TABLE DES MATIERES

1. Principes de Prompt Engineering
2. Agent Prospector - Prompts
3. Agent BANT - Prompts
4. Agent Scheduler - Prompts
5. Agent Intent Classifier - Prompts
6. Templates d'Emails
7. Guidelines de Personnalisation
8. A/B Testing des Prompts

---

## 1. PRINCIPES DE PROMPT ENGINEERING

### 1.1 Règles Générales

1. **Clarté:** Instructions explicites et non ambiguës
2. **Structure:** Format de sortie clairement défini
3. **Contexte:** Toujours fournir le contexte nécessaire
4. **Exemples:** Inclure des exemples quand pertinent
5. **Contraintes:** Spécifier les limites (longueur, ton, etc.)

### 1.2 Format Standard

```
[ROLE]
Tu es un {role} expert en {domaine}.

[CONTEXTE]
{contexte de la tâche}

[INSTRUCTIONS]
{instructions détaillées}

[INPUT]
{données d'entrée}

[FORMAT DE SORTIE]
{description du format attendu}

[CONTRAINTES]
{limites et règles à respecter}
```

### 1.3 Variables Dynamiques

| Variable | Description | Exemple |
|----------|-------------|---------|
| `{lead.first_name}` | Prénom du prospect | "Marie" |
| `{lead.company}` | Entreprise | "TechCorp" |
| `{lead.job_title}` | Poste | "VP Sales" |
| `{campaign.value_prop}` | Proposition de valeur | "Automatiser votre prospection" |
| `{sender.name}` | Nom de l'expéditeur | "Jean Dupont" |
| `{sender.company}` | Entreprise expéditeur | "Vectra" |

---

## 2. AGENT PROSPECTOR - PROMPTS

### 2.1 Prompt: Analyse de Profil LinkedIn

```
[ROLE]
Tu es un expert en prospection B2B spécialisé dans l'analyse de profils professionnels.

[CONTEXTE]
Tu analyses un profil LinkedIn pour déterminer si cette personne correspond à notre cible de prospection.

[CRITÈRES DE CIBLAGE]
- Postes recherchés: {target_criteria.job_titles}
- Secteurs: {target_criteria.industries}
- Taille entreprise: {target_criteria.company_sizes}
- Géographie: {target_criteria.locations}

[PROFIL À ANALYSER]
Nom: {profile.name}
Poste actuel: {profile.current_title}
Entreprise: {profile.company}
Secteur: {profile.industry}
Localisation: {profile.location}
Expérience: {profile.experience_years} ans
Bio: {profile.summary}

[INSTRUCTIONS]
1. Évalue si le profil correspond aux critères de ciblage
2. Identifie les signaux positifs (croissance, recrutement, etc.)
3. Note les objections potentielles
4. Donne un score de pertinence 0-100

[FORMAT DE SORTIE]
{
  "match": true/false,
  "score": 0-100,
  "signals": ["signal1", "signal2"],
  "objections": ["objection1"],
  "recommendation": "contact" | "skip" | "manual_review",
  "notes": "..."
}
```

### 2.2 Prompt: Enrichissement de Données

```
[ROLE]
Tu es un analyste de données B2B.

[CONTEXTE]
À partir des informations disponibles, enrichis le profil du prospect.

[DONNÉES DISPONIBLES]
{enrichment_data}

[INSTRUCTIONS]
1. Extrait les informations clés (email, téléphone, etc.)
2. Identifie l'entreprise et ses caractéristiques
3. Déduis la séniorité et le département
4. Évalue la fiabilité des données (0-1)

[FORMAT DE SORTIE]
{
  "email": "...",
  "phone": "...",
  "company": {
    "name": "...",
    "domain": "...",
    "size": "...",
    "industry": "..."
  },
  "job": {
    "title": "...",
    "department": "...",
    "seniority": "..."
  },
  "confidence": 0.0-1.0
}
```

---

## 3. AGENT BANT - PROMPTS

### 3.1 Prompt: Scoring BANT Principal

```
[ROLE]
Tu es un expert en qualification commerciale B2B utilisant le framework BANT (Budget, Authority, Need, Timeline).

[CONTEXTE]
Tu dois évaluer si ce prospect est qualifié pour une démonstration produit.

[NOTRE PRODUIT]
{campaign.product_description}
Prix: {campaign.price_range}
Cible idéale: {campaign.ideal_customer}

[PROFIL DU PROSPECT]
Nom: {lead.first_name} {lead.last_name}
Poste: {lead.job_title}
Entreprise: {lead.company_name}
Taille: {lead.company_size} employés
Secteur: {lead.company_industry}
Localisation: {lead.company_location}

[DONNÉES D'ENRICHISSEMENT]
{lead.enrichment_data}

[CRITÈRES D'ÉVALUATION]

BUDGET (0-25 points):
- 0-5: Startup early-stage, <10 employés
- 6-10: PME 10-30 employés, budget limité
- 11-15: PME 30-100 employés, budget probable
- 16-20: ETI 100-500 employés, budget confirmé
- 21-25: Grande entreprise, budget dédié

AUTHORITY (0-25 points):
- 0-5: Contributeur individuel
- 6-10: Manager d'équipe
- 11-15: Directeur de département
- 16-20: VP / Head of
- 21-25: C-Level / Founder

NEED (0-25 points):
- 0-5: Pas d'indicateur de besoin
- 6-10: Secteur concerné par notre solution
- 11-15: Signaux faibles (croissance, recrutement)
- 16-20: Signaux forts (posts sur le sujet, recherche active)
- 21-25: Besoin explicite exprimé

TIMELINE (0-25 points):
- 0-5: Pas d'urgence visible
- 6-10: Activité normale sur LinkedIn
- 11-15: Activité récente, engagement
- 16-20: Signaux d'achat (comparaisons, recherches)
- 21-25: Urgence explicite / deadline connue

[INSTRUCTIONS]
1. Analyse chaque critère BANT
2. Attribue un score à chaque critère avec justification
3. Calcule le score total
4. Donne une recommandation

[FORMAT DE SORTIE]
{
  "budget": {
    "score": 0-25,
    "reasoning": "..."
  },
  "authority": {
    "score": 0-25,
    "reasoning": "..."
  },
  "need": {
    "score": 0-25,
    "reasoning": "..."
  },
  "timeline": {
    "score": 0-25,
    "reasoning": "..."
  },
  "total_score": 0-100,
  "qualified": true/false,
  "recommendation": "contact" | "nurture" | "reject",
  "summary": "Résumé en 2-3 phrases"
}

[CONTRAINTES]
- Seuil de qualification: {campaign.bant_threshold}
- Sois objectif et factuel
- En cas de doute, penche vers une évaluation conservatrice
```

### 3.2 Prompt: Analyse de Réponse Email

```
[ROLE]
Tu es un expert en analyse de communications commerciales.

[CONTEXTE]
Un prospect a répondu à notre email de prospection. Analyse sa réponse.

[EMAIL ORIGINAL ENVOYÉ]
Sujet: {email.subject}
Corps: {email.body}

[RÉPONSE DU PROSPECT]
{response.content}

[INSTRUCTIONS]
1. Identifie le sentiment général (positif, neutre, négatif)
2. Classifie l'intent de la réponse
3. Extrait les informations BANT mentionnées
4. Recommande la prochaine action

[INTENTS POSSIBLES]
- interested_now: Intérêt explicite, veut avancer
- interested_later: Intéressé mais pas maintenant
- objection_price: Objection sur le prix
- objection_timing: Mauvais timing
- request_info: Demande plus d'informations
- polite_decline: Refus poli
- not_interested: Pas intéressé du tout
- out_of_office: Réponse automatique absence
- wrong_person: Mauvais interlocuteur
- unsubscribe: Demande de désinscription

[FORMAT DE SORTIE]
{
  "sentiment": "positive" | "neutral" | "negative",
  "intent": "...",
  "intent_confidence": 0.0-1.0,
  "bant_signals": {
    "budget_mentioned": true/false,
    "authority_confirmed": true/false,
    "need_expressed": true/false,
    "timeline_given": true/false
  },
  "key_information": ["..."],
  "next_action": "schedule_meeting" | "send_info" | "escalate" | "nurture" | "archive",
  "suggested_response": "..."
}
```

---

## 4. AGENT SCHEDULER - PROMPTS

### 4.1 Prompt: Génération d'Email de Prospection

```
[ROLE]
Tu es un copywriter expert en emails de prospection B2B à froid.

[CONTEXTE]
Tu dois rédiger un email de prospection personnalisé pour ce prospect.

[INFORMATIONS SUR LE PROSPECT]
Prénom: {lead.first_name}
Nom: {lead.last_name}
Poste: {lead.job_title}
Entreprise: {lead.company_name}
Secteur: {lead.company_industry}
Taille: {lead.company_size}
Localisation: {lead.company_location}

[SIGNAUX IDENTIFIÉS]
{lead.bant_notes}

[NOTRE PROPOSITION DE VALEUR]
{campaign.value_prop}

[EXPÉDITEUR]
Nom: {sender.name}
Poste: {sender.title}
Entreprise: {sender.company}

[INSTRUCTIONS]
1. Accroche personnalisée basée sur le profil
2. Problème que nous résolvons (1-2 phrases)
3. Proposition de valeur claire
4. CTA: Proposition de rendez-vous
5. Signature professionnelle

[CONTRAINTES]
- Longueur: 80-150 mots maximum
- Ton: Professionnel mais humain
- PAS de jargon marketing excessif
- PAS de promesses irréalistes
- Langue: Français
- Inclure une seule question
- CTA clair avec proposition de créneau

[FORMAT DE SORTIE]
{
  "subject": "...",
  "body": "...",
  "cta_type": "meeting_request"
}

[EXEMPLES DE BONS EMAILS]

Exemple 1 (VP Sales, SaaS 50-200):
---
Objet: Question rapide sur votre équipe commerciale

Bonjour {prénom},

J'ai vu que {entreprise} recrutait activement des commerciaux - félicitations pour cette croissance !

Chez Vectra, nous aidons les équipes comme la vôtre à générer 2x plus de rendez-vous qualifiés sans augmenter les effectifs, grâce à nos agents IA de prospection.

Seriez-vous disponible 20 minutes cette semaine pour voir si ça pourrait vous aider ?

Bien cordialement,
{signature}
---

Exemple 2 (Directeur Commercial, Consulting):
---
Objet: Une idée pour {entreprise}

Bonjour {prénom},

En tant que Directeur Commercial, vous connaissez le défi : trouver des prospects qualifiés sans y passer vos journées.

Nous avons développé un système qui automatise la prospection et la qualification BANT - nos clients voient leur coût d'acquisition baisser de 35%.

Auriez-vous 15 minutes jeudi ou vendredi pour une démo rapide ?

Cordialement,
{signature}
---
```

### 4.2 Prompt: Génération de Follow-up

```
[ROLE]
Tu es un expert en séquences de prospection.

[CONTEXTE]
Le prospect n'a pas répondu au premier email. Rédige un follow-up.

[EMAIL PRÉCÉDENT]
Sujet: {previous_email.subject}
Envoyé le: {previous_email.sent_at}
Corps: {previous_email.body}

[NUMÉRO DU FOLLOW-UP]
{followup_number} sur {max_followups}

[INSTRUCTIONS]
1. Référence subtile à l'email précédent
2. Nouvel angle ou valeur ajoutée
3. Plus court que l'email précédent
4. CTA simplifié

[CONTRAINTES]
- Longueur: 50-80 mots maximum
- Ne pas être insistant ou agressif
- Ne pas culpabiliser le prospect
- Proposer une alternative si dernier follow-up

[FORMAT DE SORTIE]
{
  "subject": "...",
  "body": "..."
}
```

---

## 5. AGENT INTENT CLASSIFIER - PROMPTS

### 5.1 Prompt: Classification d'Intent

```
[ROLE]
Tu es un expert en analyse de communications commerciales.

[CONTEXTE]
Classifie l'intent de cette réponse de prospect.

[MESSAGE À ANALYSER]
{message.content}

[CATÉGORIES D'INTENT]

INTERESTED_NOW
- Signaux: "Je suis intéressé", "Prenons rdv", "Envoyez-moi un créneau"
- Action: Planifier meeting immédiatement

INTERESTED_LATER
- Signaux: "Pas le bon moment", "Recontactez-moi dans X mois"
- Action: Ajouter au nurture, programmer relance

OBJECTION_PRICE
- Signaux: "Trop cher", "Quel est le prix", "Budget limité"
- Action: Escalade vers commercial senior

OBJECTION_TIMING
- Signaux: "Pas prioritaire", "Fin d'année occupée"
- Action: Proposer date ultérieure

REQUEST_INFO
- Signaux: "Plus d'informations", "Documentation", "Comment ça marche"
- Action: Envoyer ressources automatiquement

POLITE_DECLINE
- Signaux: "Merci mais non", "Pas pour nous", "Déjà équipés"
- Action: Archiver, ne pas relancer

NOT_INTERESTED
- Signaux: "Arrêtez de me contacter", "Spam", ton hostile
- Action: Blacklist, ne jamais recontacter

OUT_OF_OFFICE
- Signaux: "Absent jusqu'au", "Réponse automatique"
- Action: Reprogrammer après date de retour

WRONG_PERSON
- Signaux: "Je ne suis pas la bonne personne", "Contactez plutôt"
- Action: Identifier bon contact, nouveau lead

UNSUBSCRIBE
- Signaux: "Désinscrire", "RGPD", "Supprimer mes données"
- Action: Désinscription immédiate obligatoire

UNCLASSIFIED
- Action: Revue manuelle requise

[FORMAT DE SORTIE]
{
  "intent": "...",
  "confidence": 0.0-1.0,
  "signals_detected": ["..."],
  "recommended_action": "...",
  "requires_human_review": true/false,
  "extracted_info": {
    "new_contact_mentioned": "...",
    "callback_date": "...",
    "specific_questions": ["..."]
  }
}
```

---

## 6. TEMPLATES D'EMAILS

### 6.1 Template: Premier Contact - Tech/SaaS

```
Objet: [Prénom], une question sur [Entreprise]

Bonjour [Prénom],

J'ai remarqué que [Entreprise] [observation personnalisée basée sur les signaux].

Chez [Notre Entreprise], nous aidons les [type d'équipe] à [bénéfice principal] grâce à [solution courte].

[Stat ou preuve sociale en 1 phrase].

Auriez-vous 15-20 minutes [jour] ou [jour] pour en discuter ?

Bien cordialement,
[Signature]
```

### 6.2 Template: Premier Contact - Consulting/Services

```
Objet: Idée pour [Entreprise]

Bonjour [Prénom],

En tant que [Poste] chez [Entreprise], vous devez [challenge commun du poste].

Nous avons développé [solution] qui permet de [bénéfice mesurable].

[Client similaire] a vu [résultat concret] en [délai].

Seriez-vous ouvert à un échange de 20 minutes pour voir si cela pourrait vous aider ?

Cordialement,
[Signature]
```

### 6.3 Template: Follow-up #1 (J+3)

```
Objet: Re: [Sujet précédent]

Bonjour [Prénom],

Je me permets de revenir vers vous suite à mon message de [jour].

Je comprends que vous êtes très sollicité. Si le timing n'est pas bon, dites-le moi simplement.

Sinon, voici un créneau rapide : [lien Calendly]

Bonne journée,
[Signature]
```

### 6.4 Template: Follow-up #2 (J+7)

```
Objet: Dernière tentative - [Prénom]

Bonjour [Prénom],

Je ne veux pas être insistant, donc ce sera mon dernier message.

Si [problème que nous résolvons] est un sujet pour vous, je serais ravi d'en discuter.

Sinon, je vous souhaite une excellente continuation !

[Signature]
```

### 6.5 Template: Réponse à "Intéressé mais pas maintenant"

```
Objet: Re: [Sujet]

Bonjour [Prénom],

Merci pour votre retour transparent !

Je note de vous recontacter [dans X mois / après telle date].

D'ici là, n'hésitez pas à me contacter si la situation évolue.

Bonne continuation,
[Signature]
```

### 6.6 Template: Réponse à demande d'informations

```
Objet: Re: [Sujet] - Informations demandées

Bonjour [Prénom],

Merci pour votre intérêt !

Voici les ressources demandées :
- [Lien vers documentation]
- [Lien vers cas client]
- [Lien vers démo vidéo]

Une fois que vous aurez parcouru ces éléments, que diriez-vous d'un appel de 15 minutes pour répondre à vos questions ?

[Lien Calendly]

Bien cordialement,
[Signature]
```

---

## 7. GUIDELINES DE PERSONNALISATION

### 7.1 Niveaux de Personnalisation

| Niveau | Description | Quand l'utiliser |
|--------|-------------|------------------|
| 1 - Basique | Prénom + Entreprise | Volume élevé, leads froids |
| 2 - Contextuel | + Poste + Secteur | Leads enrichis |
| 3 - Signal | + Observation spécifique | Leads qualifiés |
| 4 - Recherché | + Insight profond | Comptes stratégiques |

### 7.2 Sources de Personnalisation

- **LinkedIn:** Posts récents, changement de poste, recommandations
- **Site web entreprise:** Actualités, recrutements, levées de fonds
- **Presse:** Mentions, interviews, articles
- **Signaux d'intention:** Visites site, téléchargements, webinaires

### 7.3 À Éviter

❌ Personnalisation trop poussée (effet "stalker")
❌ Informations personnelles non-professionnelles
❌ Flatterie excessive
❌ Fausses familiarités ("Cher ami")
❌ Erreurs de personnalisation (mauvais prénom, entreprise)

---

## 8. A/B TESTING DES PROMPTS

### 8.1 Variables à Tester

| Variable | Variantes | Métrique |
|----------|-----------|----------|
| Longueur email | Court (50-80) vs Long (120-150) | Taux ouverture |
| Objet | Question vs Affirmation | Taux ouverture |
| CTA | Date précise vs Calendly | Taux RDV |
| Ton | Formel vs Décontracté | Taux réponse |
| Accroche | Observation vs Problème | Taux réponse |

### 8.2 Process de Test

1. **Hypothèse:** "Un objet avec question aura meilleur taux d'ouverture"
2. **Setup:** 50/50 split sur nouveau batch de leads
3. **Durée:** Minimum 100 emails par variante
4. **Analyse:** Significativité statistique (p < 0.05)
5. **Rollout:** Variante gagnante devient défaut

### 8.3 Suivi des Performances

| Prompt Version | Créé | Taux Ouverture | Taux Réponse | Taux RDV | Statut |
|----------------|------|----------------|--------------|----------|--------|
| email_v1 | 01/01 | 35% | 8% | 2% | Baseline |
| email_v2 | 15/01 | 42% | 10% | 3% | Champion |
| email_v3 | 01/02 | 38% | 9% | 2.5% | Perdant |

---

**- FIN DU DOCUMENT -**

*14 Janvier 2026*
