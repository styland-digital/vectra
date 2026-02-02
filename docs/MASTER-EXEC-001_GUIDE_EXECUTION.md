# VECTRA - GUIDE D'EXÉCUTION COMPLET
## De la Documentation au Produit en Production
### Master Execution Plan v1.0 | 15 Janvier 2026

---

**Document:** MASTER-EXEC-001  
**Statut:** GUIDE PRINCIPAL D'EXÉCUTION  
**Durée totale:** 12 semaines (6 sprints × 2 semaines)  
**Équipe:** 2 développeurs + 1 PM  

---

## TABLE DES MATIÈRES

1. [Vue d'Ensemble du Plan](#1-vue-densemble)
2. [Prérequis & Setup Initial](#2-prérequis)
3. [PHASE 1: Fondations (Semaines 1-2)](#3-phase-1)
4. [PHASE 2: Agents IA (Semaines 3-4)](#4-phase-2)
5. [PHASE 3: Core Product (Semaines 5-6)](#5-phase-3)
6. [PHASE 4: Monétisation (Semaines 7-8)](#6-phase-4)
7. [PHASE 5: Activation & Analytics (Semaines 9-10)](#7-phase-5)
8. [PHASE 6: Polish & Launch (Semaines 11-12)](#8-phase-6)
9. [Commandes Claude Code par Phase](#9-commandes)
10. [Checklist Finale Go-Live](#10-checklist)

---

## 1. VUE D'ENSEMBLE

### 1.1 Architecture des Documents

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION VECTRA                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📋 SPECS INITIALES (10 docs)                                       │
│  ├─ CAHIER_DE_CHARGES_ULTIME.docx                                   │
│  ├─ TECH_REVIEW_SPECIFICATION_DOCUMENT.docx                         │
│  ├─ SPRINT_PLANNING_USER_STORIES.docx                               │
│  ├─ REALISATION_TECHNIQUE_DESIGN_UX_MVP_SCOPE_FINAL.docx           │
│  ├─ SAAS_PRODUCT_MAP.docx                                           │
│  ├─ DECISIONS_PRODUIT_VERROUILLEES.docx                            │
│  ├─ DESIGN_TOKENS_FOUNDATION.docx                                   │
│  ├─ GUIDE_COMPLET_DEPLOYER_AGENTS_IA.docx                          │
│  ├─ Guide_UI_UX_Design_System_SaaS.docx                            │
│  └─ VECTRA_SPECIFICATION_TECHNIQUE_V2.docx                         │
│                                                                      │
│  🔧 TECHNIQUE (5 docs)                                              │
│  ├─ DOC-TECH-001_DATABASE_SCHEMA.md                                │
│  ├─ DOC-TECH-002_API_CONTRACTS.md                                  │
│  ├─ DOC-TECH-003_ADR.md                                            │
│  ├─ DOC-TECH-004_AGENT_PROMPTS.md                                  │
│  └─ DOC-TECH-005_TEST_PLAN.md                                      │
│                                                                      │
│  📁 STRUCTURE (3 docs)                                              │
│  ├─ DOC-STRUCT-001_MONOREPO.md                                     │
│  ├─ DOC-STRUCT-002_CLAUDE_MD.md                                    │
│  └─ DOC-STRUCT-003_COMMANDS.md                                     │
│                                                                      │
│  🎨 UI/UX (3 docs)                                                  │
│  ├─ DOC-UI-001_DESIGN_SYSTEM.md                                    │
│  ├─ DOC-UI-002_COMPONENTS_CATALOG.md                               │
│  └─ DOC-UI-005_COMMANDS_UIUX.md                                    │
│                                                                      │
│  💰 BUSINESS (4 docs)                                               │
│  ├─ DOC-BIZ-001_ONBOARDING_ACTIVATION.md                           │
│  ├─ DOC-BIZ-002_BILLING_SUBSCRIPTION.md                            │
│  ├─ DOC-BIZ-003_ANALYTICS_TRACKING.md                              │
│  └─ DOC-BIZ-004_CUSTOMER_SUCCESS.md                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Timeline Visuelle

```
SEMAINE   1   2   3   4   5   6   7   8   9   10  11  12
          ├───┴───┼───┴───┼───┴───┼───┴───┼───┴───┼───┴───┤
          │       │       │       │       │       │       │
PHASE 1   ████████│       │       │       │       │       │ Fondations
PHASE 2           ████████│       │       │       │       │ Agents IA
PHASE 3                   ████████│       │       │       │ Core Product
PHASE 4                           ████████│       │       │ Monétisation
PHASE 5                                   ████████│       │ Activation
PHASE 6                                           ████████│ Launch
          │       │       │       │       │       │       │
MILESTONE │   ✓   │   ✓   │   ✓   │   ✓   │   ✓   │   ✓   │
          │ Arch  │ Agent │ MVP   │Stripe │ Beta  │ LIVE  │
          │ Done  │ Works │ UI    │ Live  │ Users │       │
```

---

## 2. PRÉREQUIS & SETUP INITIAL

### 2.1 Environnement de Développement

**Avant de commencer, s'assurer d'avoir :**

```bash
# Versions requises
node >= 18.0.0
npm >= 9.0.0 (utiliser pnpm obligatoirement)
python >= 3.11
postgresql >= 15
redis >= 7.0

## Nous utiliseron et configurons une image docker qui contient ces specs pour ce projet
```

### 2.2 Comptes & API Keys Nécessaires

| Service | Usage | Lien | Priorité |
|---------|-------|------|----------|
| GitHub | Repo + CI/CD | github.com | P0 |
| Vercel | Frontend hosting | vercel.com | P0 |
| Render | Backend hosting | render.com | P0 |
| Stripe | Paiements | stripe.com | P1 |
| SendGrid | Emails | sendgrid.com | P1 |
| RocketReach | Enrichissement | rocketreach.co | P1 |
| Calendly | Booking | calendly.com | P2 |
| HubSpot | CRM | hubspot.com | P2 |
| Segment | Analytics | segment.com | P2 |
| PostHog | Product analytics | posthog.com | P2 |
| Sentry | Error tracking | sentry.io | P2 |

### 2.3 Setup Claude Code

```bash
# 1. Installer Claude Code CLI
npm install -g @anthropic/claude-code

# 2. Authentifier
claude auth login

# 3. Créer le projet
mkdir vectra && cd vectra
claude init

# 4. Copier le fichier CLAUDE.md à la racine
# (contenu dans DOC-STRUCT-002_CLAUDE_MD.md)

# 5. Créer les commandes personnalisées
mkdir -p .claude/commands
# Copier les fichiers depuis DOC-STRUCT-003_COMMANDS.md
```

---

## 3. PHASE 1: FONDATIONS (Semaines 1-2)

### 3.1 Objectifs

```
✓ Repository monorepo structuré
✓ CI/CD fonctionnel
✓ Base de données PostgreSQL configurée
✓ Architecture backend FastAPI
✓ Architecture frontend Next.js
✓ Authentification JWT
```

### 3.2 Documents de Référence

| Document | Section | Usage |
|----------|---------|-------|
| `DOC-STRUCT-001_MONOREPO.md` | Tout | Structure des dossiers |
| `DOC-STRUCT-002_CLAUDE_MD.md` | Tout | Configuration Claude Code |
| `DOC-TECH-001_DATABASE_SCHEMA.md` | Tables core | Schema initial |
| `DOC-TECH-003_ADR.md` | ADR-001 à 003 | Décisions architecture |
| `VECTRA_SPECIFICATION_TECHNIQUE_V2.docx` | Section 3 | Architecture système |

### 3.3 Étapes Détaillées

#### ÉTAPE 1.1 : Créer le Monorepo (Jour 1)

**Prompt Claude Code :**

```
@workspace Je vais créer le monorepo Vectra. Utilise la structure définie dans 
DOC-STRUCT-001_MONOREPO.md. Crée:

1. Structure racine avec /backend et /frontend
2. Backend Python avec FastAPI (voir pyproject.toml du doc)
3. Frontend Next.js 14 avec App Router
4. Fichiers de configuration (tsconfig, .env.example, etc.)
5. README.md avec instructions setup

Réfère-toi à CLAUDE.md pour les conventions de code.
```

**Commande personnalisée :**

```bash
/setup-monorepo
```

**Validation :**
```bash
# Structure attendue
vectra/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/
│   │   ├── models/
│   │   └── services/
│   ├── pyproject.toml
│   └── alembic.ini
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
├── .github/workflows/
├── CLAUDE.md
└── README.md
```

#### ÉTAPE 1.2 : Setup CI/CD (Jour 1-2)

**Prompt Claude Code :**

```
@workspace Configure le CI/CD GitHub Actions:

1. Workflow pour backend (Python):
   - Lint avec ruff
   - Tests avec pytest
   - Build Docker image
   - Deploy sur Render (si main branch)

2. Workflow pour frontend (Next.js):
   - Lint avec eslint
   - Type check avec tsc
   - Build
   - Deploy sur Vercel (si main branch)

Réfère-toi à DOC-STRUCT-001_MONOREPO.md section CI/CD.
```

**Fichier attendu : `.github/workflows/ci.yml`**

#### ÉTAPE 1.3 : Database Schema (Jour 2-3)

**Prompt Claude Code :**

```
@workspace Crée le schéma de base de données PostgreSQL:

Utilise DOC-TECH-001_DATABASE_SCHEMA.md comme référence.

Crée les migrations Alembic pour ces tables dans l'ordre:
1. organizations (multi-tenant root)
2. users (avec rôles RBAC)
3. campaigns
4. leads
5. emails
6. meetings

Assure-toi que:
- Tous les IDs sont UUID
- Timestamps created_at/updated_at sur chaque table
- Foreign keys correctes
- Indexes pour les queries fréquentes
```

**Commande personnalisée :**

```bash
/db-migrate "Initial schema with core tables"
```

**Validation :**
```bash
cd backend
alembic upgrade head
# Vérifier les tables créées
psql -d vectra -c "\dt"
```

#### ÉTAPE 1.4 : Auth JWT (Jour 3-4)

**Prompt Claude Code :**

```
@workspace Implémente l'authentification JWT:

Réfère-toi à:
- DOC-TECH-002_API_CONTRACTS.md (section Auth)
- VECTRA_SPECIFICATION_TECHNIQUE_V2.docx (section 9.1)

Crée:
1. /api/v1/auth/register - Inscription
2. /api/v1/auth/login - Connexion (retourne access + refresh token)
3. /api/v1/auth/refresh - Refresh token
4. /api/v1/auth/logout - Déconnexion
5. /api/v1/user/me - Profil utilisateur courant

Middleware:
- Vérification JWT sur routes protégées
- Extraction user + organization du token
- RBAC basé sur le rôle

Sécurité:
- Passwords hashés avec bcrypt (cost 12)
- Access token expire 15min
- Refresh token expire 7 jours
```

**Tests à écrire :**
```bash
/test auth
```

---

## 4. PHASE 2: AGENTS IA (Semaines 3-4)

### 4.1 Objectifs

```
✓ CrewAI intégré et configuré
✓ Agent Prospector fonctionnel
✓ Agent BANT fonctionnel
✓ Agent Scheduler fonctionnel
✓ State machine orchestration
✓ Intégration RocketReach
```

### 4.2 Documents de Référence

| Document | Section | Usage |
|----------|---------|-------|
| `DOC-TECH-004_AGENT_PROMPTS.md` | Tout | Prompts des 3 agents |
| `TECH_REVIEW_SPECIFICATION_DOCUMENT.docx` | Section 1.A | Décision CrewAI |
| `REALISATION_TECHNIQUE.docx` | Blocs 1-3 | Specs fonctionnelles agents |
| `VECTRA_SPECIFICATION_TECHNIQUE_V2.docx` | Section 4 | Specs détaillées agents |
| `GUIDE_COMPLET_DEPLOYER_AGENTS_IA.docx` | Section 2 | Exemples conversations |

### 4.3 Étapes Détaillées

#### ÉTAPE 2.1 : Setup CrewAI (Jour 1)

**Prompt Claude Code :**

```
@workspace Configure CrewAI pour Vectra:

Réfère-toi à:
- TECH_REVIEW_SPECIFICATION_DOCUMENT.docx (Section 1.A - décision CrewAI)
- DOC-TECH-004_AGENT_PROMPTS.md (structure des agents)

Crée:
1. backend/app/agents/__init__.py
2. backend/app/agents/base.py - Classe de base Agent
3. backend/app/agents/crew.py - Configuration CrewAI
4. backend/app/agents/tools/ - Outils partagés

Configure:
- LLM: Llama 2 70B via Ollama (local) ou API
- Fallback: Claude API si besoin
- Memory: Redis pour contexte entre runs
- Logging: Structured logging pour debug
```

#### ÉTAPE 2.2 : Agent Prospector (Jour 2-3)

**Prompt Claude Code :**

```
@workspace Crée l'Agent Prospector:

Réfère-toi à:
- DOC-TECH-004_AGENT_PROMPTS.md (Section Prospector)
- REALISATION_TECHNIQUE.docx (Bloc 1)
- VECTRA_SPECIFICATION_TECHNIQUE_V2.docx (Section 4.1)

L'agent doit:
1. Recevoir des critères de recherche (job titles, geo, company size)
2. Appeler RocketReach API pour trouver des prospects
3. Enrichir les données (email, phone, company info)
4. Vérifier les doublons dans la DB
5. Scorer par priorité firmographique
6. Retourner une liste de prospects triée

Crée:
- backend/app/agents/prospector.py
- backend/app/services/rocketreach.py
- backend/app/services/enrichment.py

Prompt système exact (copier depuis DOC-TECH-004):
[Insérer le prompt du document]
```

**Commande personnalisée :**

```bash
/create-agent prospector
```

**Test manuel :**
```python
# backend/tests/agents/test_prospector.py
async def test_prospector_finds_leads():
    agent = ProspectorAgent()
    results = await agent.run({
        "job_titles": ["VP Sales", "Sales Director"],
        "geography": ["France"],
        "company_size": "50-200",
        "limit": 10
    })
    assert len(results) >= 5
    assert all(r.email for r in results)
```

#### ÉTAPE 2.3 : Agent BANT (Jour 4-5)

**Prompt Claude Code :**

```
@workspace Crée l'Agent BANT Qualifier:

Réfère-toi à:
- DOC-TECH-004_AGENT_PROMPTS.md (Section BANT)
- REALISATION_TECHNIQUE.docx (Bloc 2)
- VECTRA_SPECIFICATION_TECHNIQUE_V2.docx (Section 4.2)

L'agent doit:
1. Recevoir un prospect avec ses données enrichies
2. Analyser le profil LinkedIn (si disponible)
3. Évaluer les 4 critères BANT:
   - Budget: Taille entreprise > 50 personnes? (0-25 pts)
   - Authority: Manager/VP/C-level? (0-25 pts)
   - Need: Indicateurs de besoin? (0-25 pts)
   - Timeline: Activité récente? (0-25 pts)
4. Calculer score total 0-100
5. Décider: score >= 60 → qualified, sinon → nurture/reject

Crée:
- backend/app/agents/bant.py
- backend/app/services/linkedin.py (scraping léger)
- backend/app/services/scoring.py

Latence cible: < 30 secondes par lead
```

**Validation scoring :**
```python
# Test avec des cas connus
test_cases = [
    {"company_size": 150, "title": "VP Sales", "recent_posts": 5, "expected_score_min": 70},
    {"company_size": 10, "title": "Intern", "recent_posts": 0, "expected_score_max": 30},
]
```

#### ÉTAPE 2.4 : Agent Scheduler (Jour 6-7)

**Prompt Claude Code :**

```
@workspace Crée l'Agent Meeting Scheduler:

Réfère-toi à:
- DOC-TECH-004_AGENT_PROMPTS.md (Section Scheduler)
- REALISATION_TECHNIQUE.docx (Bloc 3)
- VECTRA_SPECIFICATION_TECHNIQUE_V2.docx (Section 4.3)

L'agent doit:
1. Recevoir un lead qualifié (score >= 60)
2. Générer un email personnalisé:
   - Sujet accrocheur
   - Corps avec contexte personnel
   - Value prop claire en 1 ligne
   - CTA avec proposition de créneau
3. Créer un lien Calendly pré-rempli
4. Envoyer via SendGrid
5. Logger l'envoi

Crée:
- backend/app/agents/scheduler.py
- backend/app/services/email_generator.py
- backend/app/services/sendgrid.py
- backend/app/services/calendly.py

Templates emails dans: backend/app/templates/emails/
```

#### ÉTAPE 2.5 : State Machine & Orchestration (Jour 8-10)

**Prompt Claude Code :**

```
@workspace Crée le State Machine pour orchestrer les 3 agents:

Réfère-toi à:
- VECTRA_SPECIFICATION_TECHNIQUE_V2.docx (Section 3.2)
- TECH_REVIEW_SPECIFICATION_DOCUMENT.docx (Risque #1)

Flow:
PROSPECTING → QUALIFYING → SCHEDULING → COMPLETED

Implémente:
1. backend/app/orchestrator/state_machine.py
2. backend/app/orchestrator/campaign_runner.py
3. Celery tasks pour exécution async
4. Redis pour état des campagnes

États d'un lead:
- new → Agent Prospector trouve
- enriched → données complètes
- scoring → Agent BANT évalue
- qualified → score >= 60
- contacted → email envoyé
- meeting_scheduled → RDV booké
- completed → flow terminé

Gestion erreurs:
- Retry avec exponential backoff
- Dead letter queue pour échecs
- Alertes si trop d'échecs
```

**Commande personnalisée :**

```bash
/run-campaign <campaign_id>
```

---

## 5. PHASE 3: CORE PRODUCT (Semaines 5-6)

### 5.1 Objectifs

```
✓ Dashboard principal
✓ CRUD Campaigns
✓ Liste et détail Leads
✓ Queue d'approbation Emails
✓ Vue Meetings
✓ Navigation complète
```

### 5.2 Documents de Référence

| Document | Section | Usage |
|----------|---------|-------|
| `DOC-UI-001_DESIGN_SYSTEM.md` | Tout | Tokens, couleurs, typo |
| `DOC-UI-002_COMPONENTS_CATALOG.md` | Tout | Composants React |
| `DOC-UI-005_COMMANDS_UIUX.md` | Tout | Commandes création UI |
| `REALISATION_TECHNIQUE.docx` | Partie 2 | Specs 4 écrans MVP |
| `DECISIONS_PRODUIT_VERROUILLEES.docx` | Tout | Mobile-first, dark mode |
| `Guide_UI_UX_Design_System_SaaS.docx` | Section 4 | Cartographie écrans |

### 5.3 Étapes Détaillées

#### ÉTAPE 3.1 : Setup Design System (Jour 1)

**Prompt Claude Code :**

```
@workspace Configure le Design System frontend:

Réfère-toi à DOC-UI-001_DESIGN_SYSTEM.md.

Crée:
1. frontend/app/globals.css - CSS variables (tokens)
2. frontend/tailwind.config.ts - Extension Tailwind
3. frontend/lib/utils.ts - Fonction cn() pour classes
4. frontend/components/ui/ - Composants Shadcn

Tokens à configurer:
- Couleurs: primary #2E5BFF, accent #FF9F43, etc.
- Spacing: système 8px
- Typography: Inter
- Shadows, radius, transitions

Dark mode:
- Natif avec CSS variables
- Toggle dans les settings
- Persister en localStorage
```

**Commande personnalisée :**

```bash
/style-guide
```

#### ÉTAPE 3.2 : Layout Principal (Jour 1-2)

**Prompt Claude Code :**

```
@workspace Crée le layout principal de l'application:

Réfère-toi à:
- DOC-UI-002_COMPONENTS_CATALOG.md (Section Navigation)
- DECISIONS_PRODUIT_VERROUILLEES.docx (Mobile-first)

Crée:
1. frontend/app/(dashboard)/layout.tsx
2. frontend/components/layout/sidebar.tsx
3. frontend/components/layout/topbar.tsx
4. frontend/components/layout/mobile-nav.tsx

Responsive:
- Mobile (<768px): Sidebar cachée, bottom nav
- Tablet (768-1024px): Mini sidebar 64px
- Desktop (>1024px): Full sidebar 256px

Navigation items:
- Dashboard (home icon)
- Campaigns (target icon)
- Leads (users icon)
- Emails (mail icon)
- Meetings (calendar icon)
- Analytics (chart icon)
- Settings (cog icon)
```

**Commande personnalisée :**

```bash
/create-component layout/sidebar
/create-component layout/topbar
```

#### ÉTAPE 3.3 : Dashboard (Jour 2-3)

**Prompt Claude Code :**

```
@workspace Crée la page Dashboard:

Réfère-toi à:
- REALISATION_TECHNIQUE.docx (Écran 1: Dashboard)
- DOC-UI-002_COMPONENTS_CATALOG.md (StatsCard, ChartCard)
- DECISIONS_PRODUIT_VERROUILLEES.docx (Section 1 - System Status)

URL: /dashboard (page d'accueil après login)

Sections:
1. Header avec titre "Dashboard" et période selector
2. Stats row (4 cards):
   - Total Leads (avec trend)
   - Qualified (score >= 60)
   - Emails Sent
   - Meetings Booked
3. Charts row:
   - Pipeline Performance (AreaChart)
   - Recent Activity (liste)
4. Quick Actions:
   - "Create Campaign" button
   - "Pending Approvals" si emails en attente

API calls:
- GET /api/v1/dashboard/stats
- GET /api/v1/dashboard/activity

L'utilisateur doit comprendre en 10 secondes:
- Le système tourne-t-il?
- Produit-il des résultats?
- Dois-je agir?
```

**Commande personnalisée :**

```bash
/create-page dashboard
```

#### ÉTAPE 3.4 : Campaigns (Jour 3-4)

**Prompt Claude Code :**

```
@workspace Crée le module Campaigns:

Réfère-toi à:
- REALISATION_TECHNIQUE.docx (Écran 2: Campaign Setup)
- DOC-UI-002_COMPONENTS_CATALOG.md (CampaignCard, WizardPattern)

Pages à créer:
1. /campaigns - Liste des campagnes
2. /campaigns/new - Wizard création (5 steps)
3. /campaigns/[id] - Détail campagne

Liste (/campaigns):
- Search bar
- Filter par status (draft, active, paused, completed)
- Grid de CampaignCard
- Button "New Campaign"

Wizard création (5 steps):
- Step 1: Nom + Secteur
- Step 2: Target Profile (job titles, company size, geo)
- Step 3: Email Template Review (MUST approve)
- Step 4: Meeting Availability (jours + heures)
- Step 5: Review & Launch

Détail (/campaigns/[id]):
- Tabs: Overview, Leads, Emails, Settings
- Stats: leads found, qualified, emails sent, meetings
- Performance chart
- Actions: Pause/Resume, Edit, Delete

API:
- GET /api/v1/campaigns
- POST /api/v1/campaigns
- GET /api/v1/campaigns/{id}
- PATCH /api/v1/campaigns/{id}
- POST /api/v1/campaigns/{id}/launch
- POST /api/v1/campaigns/{id}/pause
```

**Commandes personnalisées :**

```bash
/create-page campaigns
/create-page campaigns/new
/create-page campaigns/[id]
/create-form campaign-create
```

#### ÉTAPE 3.5 : Leads (Jour 5-6)

**Prompt Claude Code :**

```
@workspace Crée le module Leads:

Réfère-toi à:
- DOC-UI-002_COMPONENTS_CATALOG.md (DataTable, LeadDetailPanel, BANTScoreDisplay)
- VECTRA_SPECIFICATION_TECHNIQUE_V2.docx (Section 5.4 - Table leads)

Pages:
1. /leads - Liste avec DataTable
2. Panel détail (slide-in, pas nouvelle page)

Liste (/leads):
- Search bar (nom, email, company)
- Filters: campaign, status, score range
- DataTable columns:
  - Checkbox (select)
  - Name + Company
  - BANT Score (badge coloré)
  - Status (badge)
  - Actions (menu)
- Pagination
- Bulk actions (export, delete)

Panel Détail (LeadDetailPanel):
- Header: nom, job title, close button
- Quick actions: Send Email, Schedule Meeting
- Tabs: Details, BANT Score, Activity
- Contact info avec liens cliquables
- Timeline des interactions

API:
- GET /api/v1/leads?campaign_id=&status=&score_min=
- GET /api/v1/leads/{id}
- PATCH /api/v1/leads/{id}
- DELETE /api/v1/leads/{id}
- POST /api/v1/leads/export
```

**Commandes personnalisées :**

```bash
/create-page leads
/create-component features/leads/lead-detail-panel
```

#### ÉTAPE 3.6 : Emails (Jour 7-8)

**Prompt Claude Code :**

```
@workspace Crée le module Emails:

Réfère-toi à:
- REALISATION_TECHNIQUE.docx (Écran 3: Email Review)
- DOC-UI-002_COMPONENTS_CATALOG.md (EmailPreviewCard)

Pages:
1. /emails - Queue d'approbation

Liste (/emails):
- Tabs: Pending, Approved, Sent, All
- Liste de EmailPreviewCard
- Chaque card affiche:
  - Recipient (avatar, name, company)
  - Subject line
  - Body preview (expandable)
  - BANT score badge
  - Generated timestamp
  - Actions: Approve, Edit, Reject, Regenerate

Modal Edit:
- To (read-only)
- Subject (editable)
- Body (textarea)
- Preview mode
- Save / Save & Approve

Bulk actions:
- Approve selected
- Reject selected

API:
- GET /api/v1/emails?status=pending
- PATCH /api/v1/emails/{id}/approve
- PATCH /api/v1/emails/{id}/reject
- PATCH /api/v1/emails/{id} (edit)
- POST /api/v1/emails/{id}/regenerate
```

**Commandes personnalisées :**

```bash
/create-page emails
/create-modal email-editor
```

#### ÉTAPE 3.7 : Meetings (Jour 9-10)

**Prompt Claude Code :**

```
@workspace Crée le module Meetings:

Réfère-toi à:
- DOC-UI-002_COMPONENTS_CATALOG.md (Composants données)

Page /meetings:
- Tabs: Upcoming, Past, All
- Grouped by date (Today, Tomorrow, This Week, Later)
- Meeting cards:
  - Time slot
  - Lead name + company
  - Duration
  - Zoom link
  - Actions: Join, Reschedule, Cancel
- Calendar view option (bonus)

API:
- GET /api/v1/meetings?status=upcoming
- PATCH /api/v1/meetings/{id}/reschedule
- PATCH /api/v1/meetings/{id}/cancel
- POST /api/v1/meetings/{id}/complete
```

---

## 6. PHASE 4: MONÉTISATION (Semaines 7-8)

### 6.1 Objectifs

```
✓ Intégration Stripe complète
✓ 3 plans configurés (Starter, Growth, Scale)
✓ Checkout flow
✓ Customer Portal
✓ Webhooks fonctionnels
✓ Rate limiting par plan
✓ Dunning sequence
```

### 6.2 Documents de Référence

| Document | Section | Usage |
|----------|---------|-------|
| `DOC-BIZ-002_BILLING_SUBSCRIPTION.md` | Tout | Référence principale |
| `VECTRA_SPECIFICATION_TECHNIQUE_V2.docx` | Section 8 | Intégrations |
| `CAHIER_DE_CHARGES_ULTIME.docx` | Section 13 | Pricing strategy |

### 6.3 Étapes Détaillées

#### ÉTAPE 4.1 : Setup Stripe (Jour 1-2)

**Prompt Claude Code :**

```
@workspace Configure l'intégration Stripe:

Réfère-toi à DOC-BIZ-002_BILLING_SUBSCRIPTION.md (Sections 2-4).

1. Créer les Products dans Stripe Dashboard:
   - Vectra Starter (prod_starter)
   - Vectra Growth (prod_growth)
   - Vectra Scale (prod_scale)

2. Créer les Prices:
   - price_starter_monthly: 99€/mois
   - price_starter_yearly: 990€/an
   - price_growth_monthly: 299€/mois
   - price_growth_yearly: 2990€/an
   - price_scale_monthly: 799€/mois
   - price_scale_yearly: 7990€/an

3. Backend:
   - backend/app/services/stripe.py
   - backend/app/api/v1/billing.py

4. Endpoints:
   - POST /api/v1/billing/checkout - Créer session
   - POST /api/v1/billing/portal - Lien Customer Portal
   - GET /api/v1/billing/subscription - Status actuel
   - POST /api/webhooks/stripe - Webhook handler
```

**Config Stripe Dashboard :**
```
Settings > Billing > Customer Portal:
✓ Allow customers to update payment methods
✓ Allow customers to view invoices
✓ Allow customers to cancel subscriptions
✓ Allow customers to update subscriptions
```

#### ÉTAPE 4.2 : Webhook Handler (Jour 2-3)

**Prompt Claude Code :**

```
@workspace Implémente le handler de webhooks Stripe:

Réfère-toi à DOC-BIZ-002_BILLING_SUBSCRIPTION.md (Section 4.2).

Events à gérer:
1. checkout.session.completed
   → Activer l'abonnement
   → Mettre à jour organization.plan
   → Envoyer email bienvenue

2. customer.subscription.updated
   → Mettre à jour status, plan, période
   → Si upgrade: activer nouvelles limites immédiatement
   → Si downgrade: planifier pour fin de période

3. customer.subscription.deleted
   → Marquer comme canceled
   → Déclencher séquence win-back
   → Planifier suppression données (30j)

4. invoice.paid
   → Logger le paiement
   → Reset quotas mensuels

5. invoice.payment_failed
   → Marquer past_due
   → Déclencher séquence dunning
   → Notifier l'utilisateur

Sécurité:
- Vérifier signature webhook
- Idempotency (ne pas traiter 2x le même event)
```

#### ÉTAPE 4.3 : Rate Limiting par Plan (Jour 3-4)

**Prompt Claude Code :**

```
@workspace Implémente le rate limiting par plan:

Réfère-toi à DOC-BIZ-002_BILLING_SUBSCRIPTION.md (Section 3).

Middleware backend:
1. backend/app/middleware/quota.py
2. backend/app/middleware/rate_limit.py

Limites par plan:
```python
PLAN_LIMITS = {
    "starter": {
        "leads_per_month": 500,
        "campaigns_active": 2,
        "users": 2,
        "emails_per_day": 50,
    },
    "growth": {
        "leads_per_month": 2000,
        "campaigns_active": 5,
        "users": 5,
        "emails_per_day": 200,
    },
    "scale": {
        "leads_per_month": 10000,
        "campaigns_active": -1,  # unlimited
        "users": 15,
        "emails_per_day": 500,
    },
}
```

Comportement:
- 80% quota: Warning in-app
- 100% quota: Soft block + upsell prompt
- 120% quota: Hard block

API endpoint:
- GET /api/v1/usage - Usage actuel vs limites
```

#### ÉTAPE 4.4 : UI Billing (Jour 5-6)

**Prompt Claude Code :**

```
@workspace Crée les pages billing frontend:

Réfère-toi à DOC-BIZ-002_BILLING_SUBSCRIPTION.md (Section 8.4).

Pages:
1. /settings/billing - Vue principale
2. /pricing - Page publique des plans

/settings/billing:
- Current plan card
- Usage meters (leads, campaigns, users)
- Billing history (invoices)
- Payment method
- Buttons: Upgrade, Manage (→ Stripe Portal)

/pricing:
- Toggle Monthly/Yearly
- 3 plan cards avec features
- CTA: "Start Free Trial" ou "Upgrade"
- FAQ section

Composants:
- PricingTable
- PlanCard
- UsageMeter
- InvoiceList
```

**Commandes personnalisées :**

```bash
/create-page settings/billing
/create-page pricing
/create-component features/billing/pricing-table
```

#### ÉTAPE 4.5 : Dunning Sequence (Jour 7-8)

**Prompt Claude Code :**

```
@workspace Implémente la séquence de dunning:

Réfère-toi à DOC-BIZ-002_BILLING_SUBSCRIPTION.md (Section 6).

Timeline:
- J0: Paiement échoué → Email automatique
- J1: 1er retry Stripe
- J3: 2ème retry + Email "Action requise"
- J5: 3ème retry + Email "Compte à risque"
- J7: Passage past_due, warning permanent
- J10: Email "Dernière chance" avec -20%
- J14: Passage unpaid, accès read-only
- J30: Annulation

Crée:
- backend/app/services/dunning.py
- backend/app/tasks/dunning_tasks.py (Celery)
- Templates emails dans /templates/emails/dunning/

Configurer Stripe:
- Smart retries activé
- Invoice emails activés
```

---

## 7. PHASE 5: ACTIVATION & ANALYTICS (Semaines 9-10)

### 7.1 Objectifs

```
✓ Onboarding wizard
✓ Empty states guidés
✓ Checklist d'activation
✓ Emails lifecycle
✓ Analytics tracking (Segment + PostHog)
✓ Dashboards internes
```

### 7.2 Documents de Référence

| Document | Section | Usage |
|----------|---------|-------|
| `DOC-BIZ-001_ONBOARDING_ACTIVATION.md` | Tout | Référence onboarding |
| `DOC-BIZ-003_ANALYTICS_TRACKING.md` | Tout | Event tracking |
| `DECISIONS_PRODUIT_VERROUILLEES.docx` | UX Philosophy | Guidelines |

### 7.3 Étapes Détaillées

#### ÉTAPE 5.1 : Onboarding Wizard (Jour 1-3)

**Prompt Claude Code :**

```
@workspace Crée le parcours d'onboarding:

Réfère-toi à DOC-BIZ-001_ONBOARDING_ACTIVATION.md (Section 3).

Pages:
1. /onboarding - Welcome screen
2. /onboarding/setup - Wizard 3 steps

Wizard:
- Step 1: Company Info (secteur, taille équipe, rôle)
- Step 2: Connect Integration (HubSpot ou Calendly, skippable)
- Step 3: First Campaign (création rapide)

Post-wizard:
- Redirect vers /dashboard
- Afficher données de démo (10 leads fictifs)
- Afficher checklist flottante

Backend:
- POST /api/v1/onboarding/start
- POST /api/v1/onboarding/step/{step}/complete
- GET /api/v1/onboarding/status

Time-to-value cible: < 5 minutes
```

**Commandes personnalisées :**

```bash
/create-page onboarding
/create-page onboarding/setup
/create-component features/onboarding/wizard
```

#### ÉTAPE 5.2 : Checklist Activation (Jour 3-4)

**Prompt Claude Code :**

```
@workspace Crée la checklist d'activation:

Réfère-toi à DOC-BIZ-001_ONBOARDING_ACTIVATION.md (Section 2 & 7).

Composant: ActivationChecklist (widget flottant bottom-right)

Items:
1. ✅ Créer votre compte (toujours done)
2. ○ Créer votre première campagne → /campaigns/new
3. ○ Connecter une intégration → /settings/integrations
4. ○ Approuver votre premier email → /emails
5. ○ Obtenir votre premier RDV → (auto-complété)

Comportement:
- Apparaît après onboarding wizard
- Reste visible jusqu'à 5/5 complété
- Peut être minimisé (pas fermé)
- Chaque item cliquable
- Progress indicator (2/5)

Backend:
- GET /api/v1/activation/status
- POST /api/v1/activation/check
```

#### ÉTAPE 5.3 : Empty States (Jour 4-5)

**Prompt Claude Code :**

```
@workspace Crée les empty states pour toutes les pages:

Réfère-toi à DOC-BIZ-001_ONBOARDING_ACTIVATION.md (Section 4).

Composant générique: EmptyState

Props:
- icon: LucideIcon
- title: string
- description: string
- action: { label: string, href: string }
- secondaryAction?: { label: string, href: string }

Empty states à créer:

1. Dashboard (no campaigns):
   - "Votre dashboard attend des données"
   - CTA: "Créer ma première campagne"

2. Leads (no leads):
   - "Aucun lead pour le moment"
   - Progress bar si campagne en cours
   - CTA: "Voir le statut des agents"

3. Emails (no pending):
   - "Tout est à jour !"
   - "Aucun email en attente"

4. Meetings (no meetings):
   - "Vos premiers RDV arrivent bientôt"
   - Afficher pipeline stats

5. Campaigns (no campaigns):
   - "Lancez votre première campagne"
   - CTA: "Créer une campagne"
```

**Commande personnalisée :**

```bash
/create-component shared/empty-state
```

#### ÉTAPE 5.4 : Analytics Setup (Jour 5-7)

**Prompt Claude Code :**

```
@workspace Configure le tracking analytics:

Réfère-toi à DOC-BIZ-003_ANALYTICS_TRACKING.md.

1. Setup Segment:
   - frontend/lib/analytics.ts
   - Fonctions: identify, track, page

2. Setup PostHog (via Segment destination)

3. Implémenter les events critiques:

Account:
- account_created
- account_verified

Onboarding:
- onboarding_started
- onboarding_step_completed
- onboarding_completed
- activation_achieved

Campaigns:
- campaign_created
- campaign_launched
- campaign_paused

Leads:
- lead_found
- lead_qualified
- lead_exported

Emails:
- email_approved
- email_sent
- email_opened

Billing:
- checkout_started
- checkout_completed
- subscription_canceled

4. Hook useTrack() pour faciliter le tracking

5. Automatic page views avec usePageView()
```

#### ÉTAPE 5.5 : Emails Lifecycle (Jour 8-10)

**Prompt Claude Code :**

```
@workspace Configure les emails lifecycle:

Réfère-toi à DOC-BIZ-001_ONBOARDING_ACTIVATION.md (Section 5).

Service: Customer.io ou SendGrid

Séquence onboarding:
- J0: Welcome email
- J0+2h: Getting Started (si wizard non complété)
- J1: First Results (si leads trouvés)
- J3: Activation Nudge (si non activé)
- J5: Success Story (social proof)
- J7: Last Chance (urgence fin trial)

Templates à créer:
- backend/app/templates/emails/welcome.html
- backend/app/templates/emails/getting_started.html
- backend/app/templates/emails/activation_nudge.html
- backend/app/templates/emails/trial_ending.html

Backend:
- backend/app/services/email_lifecycle.py
- backend/app/tasks/email_tasks.py (Celery scheduled)

Triggers:
- account_created → welcome
- J+3 && !activated → nudge
- J+7 && !converted → last_chance
```

---

## 8. PHASE 6: POLISH & LAUNCH (Semaines 11-12)

### 8.1 Objectifs

```
✓ Tests E2E complets
✓ Security audit (OWASP)
✓ Performance optimization
✓ Documentation utilisateur
✓ 10-15 beta users
✓ NPS > 50
✓ GO LIVE
```

### 8.2 Documents de Référence

| Document | Section | Usage |
|----------|---------|-------|
| `DOC-TECH-005_TEST_PLAN.md` | Tout | Plan de tests |
| `DOC-BIZ-004_CUSTOMER_SUCCESS.md` | Tout | CS ready |
| `SPRINT_PLANNING_USER_STORIES.docx` | Sprint 6 | Go-live requirements |

### 8.3 Étapes Détaillées

#### ÉTAPE 6.1 : Tests E2E (Jour 1-3)

**Prompt Claude Code :**

```
@workspace Écris les tests E2E avec Playwright:

Réfère-toi à DOC-TECH-005_TEST_PLAN.md.

Flows critiques à tester:

1. Auth flow:
   - Signup → Email verification → Login → Logout
   - Password reset

2. Onboarding flow:
   - New user → Wizard complet → Dashboard avec données

3. Campaign flow:
   - Create campaign → Launch → View leads → Approve emails

4. Billing flow:
   - View pricing → Checkout → Success → Access features

5. Settings flow:
   - Update profile → Connect integration → View billing

Fichiers:
- frontend/e2e/auth.spec.ts
- frontend/e2e/onboarding.spec.ts
- frontend/e2e/campaigns.spec.ts
- frontend/e2e/billing.spec.ts

Config:
- frontend/playwright.config.ts
- Test sur 3 viewports: mobile, tablet, desktop
```

**Commande :**

```bash
npm run test:e2e
```

#### ÉTAPE 6.2 : Security Audit (Jour 3-4)

**Prompt Claude Code :**

```
@workspace Effectue un audit de sécurité OWASP:

Vérifie et corrige:

1. Injection (SQL, NoSQL, Command)
   - Parameterized queries partout
   - Input validation

2. Broken Authentication
   - JWT secure (HS256 minimum)
   - Rate limiting sur login
   - Password policy

3. Sensitive Data Exposure
   - HTTPS only
   - Passwords hashés (bcrypt)
   - PII chiffrées at-rest

4. XML External Entities (XXE)
   - Pas de parsing XML non sécurisé

5. Broken Access Control
   - RBAC vérifié à chaque endpoint
   - Multi-tenant isolation

6. Security Misconfiguration
   - Headers de sécurité (CSP, HSTS, etc.)
   - Pas de debug en prod
   - Secrets dans env vars

7. XSS
   - Escape output
   - CSP strict

8. Insecure Deserialization
   - Validation des payloads

9. Using Components with Known Vulnerabilities
   - npm audit / pip audit
   - Dépendances à jour

10. Insufficient Logging
    - Tous les auth events loggés
    - Alertes sur comportements suspects

Output: Rapport avec issues et fixes
```

#### ÉTAPE 6.3 : Performance Optimization (Jour 4-5)

**Prompt Claude Code :**

```
@workspace Optimise les performances:

Cibles:
- Page load: < 2s
- API response: < 500ms (P95)
- Time to Interactive: < 3s

Frontend:
1. Code splitting (dynamic imports)
2. Image optimization (next/image)
3. Lazy loading des composants lourds
4. Bundle analysis (supprimer dead code)
5. Service worker pour caching

Backend:
1. Database indexes review
2. Query optimization (N+1 queries)
3. Redis caching pour données fréquentes
4. Pagination sur toutes les listes
5. Compression gzip

Monitoring:
1. Setup Web Vitals tracking
2. API latency monitoring
3. Error rate alerting
```

#### ÉTAPE 6.4 : Beta Testing (Jour 6-8)

**Checklist Beta :**

```
□ Recruter 10-15 beta users (ICP)
□ Créer Slack/Discord channel pour feedback
□ Setup Intercom pour support live
□ Préparer onboarding call template
□ Créer feedback survey (Typeform)
□ Définir métriques success:
  - Activation rate > 40%
  - NPS > 50
  - 0 bugs critiques
  - Time-to-value < 24h
```

**Prompt pour créer le feedback survey :**

```
@workspace Crée le questionnaire de feedback beta:

Questions:
1. Comment avez-vous trouvé l'onboarding? (1-10)
2. Avez-vous réussi à créer votre première campagne? (Oui/Non)
3. Combien de temps cela a-t-il pris? (<5min, 5-15min, 15-30min, >30min)
4. Qu'est-ce qui vous a le plus frustré?
5. Qu'est-ce qui vous a le plus plu?
6. Recommanderiez-vous Vectra? (0-10 NPS)
7. Quelles features manquent?
8. À quel prix achèteriez-vous? (<99€, 99€, 199€, 299€, >299€)
```

#### ÉTAPE 6.5 : Documentation Utilisateur (Jour 8-9)

**Prompt Claude Code :**

```
@workspace Crée la documentation utilisateur:

Structure (docs.vectra.io ou /help):

1. Getting Started
   - Quick start guide
   - First campaign in 5 minutes
   - Video walkthrough

2. Campaigns
   - Creating a campaign
   - Targeting options
   - Managing campaigns

3. Leads
   - Understanding BANT scores
   - Exporting to CRM
   - Manual follow-up

4. Emails
   - Approval workflow
   - Editing templates
   - Tracking opens/clicks

5. Integrations
   - HubSpot setup
   - Calendly setup
   - Webhooks

6. Billing
   - Plans & pricing
   - Upgrading/downgrading
   - Invoices

7. FAQ
   - Common questions
   - Troubleshooting
```

#### ÉTAPE 6.6 : Go-Live Checklist (Jour 10)

**Checklist finale :**

```
TECHNIQUE
□ CI/CD green sur main
□ Staging testé (E2E pass)
□ Production environment ready
□ Database migrations applied
□ SSL certificates valid
□ DNS configured
□ CDN configured
□ Backups verified
□ Monitoring active
□ Error tracking active

BUSINESS
□ Stripe live mode enabled
□ Email domain verified
□ Support email ready
□ Intercom configured
□ Analytics tracking verified
□ Legal pages live (ToS, Privacy)

LAUNCH
□ Beta users notified
□ Landing page ready
□ Social media posts scheduled
□ Product Hunt prepared
□ Press kit ready
□ Team on standby for issues
```

---

## 9. COMMANDES CLAUDE CODE PAR PHASE

### 9.1 Commandes Système (toujours disponibles)

```bash
# Structure
/setup-monorepo          # Créer structure initiale
/create-page <path>      # Créer une page Next.js
/create-component <path> # Créer un composant React
/create-form <name>      # Créer un formulaire avec validation
/create-modal <name>     # Créer une modal/dialog

# Base de données
/db-migrate <message>    # Créer migration Alembic
/db-seed                 # Seed données de test

# Tests
/test <scope>            # Lancer tests (unit, e2e, all)
/test-coverage           # Rapport de couverture

# UI
/style-guide             # Afficher quick reference design
/check-accessibility     # Vérifier WCAG
/responsive-check        # Vérifier responsive

# Agents
/create-agent <name>     # Créer nouvel agent IA
/run-campaign <id>       # Lancer campagne manuellement

# Déploiement
/deploy staging          # Deploy sur staging
/deploy production       # Deploy sur production
```

### 9.2 Prompts Optimisés par Phase

**PHASE 1 - Fondations :**

```
@workspace [PHASE 1 - FONDATIONS]

Contexte: Je démarre le projet Vectra.
Docs de référence:
- DOC-STRUCT-001_MONOREPO.md
- DOC-STRUCT-002_CLAUDE_MD.md
- DOC-TECH-001_DATABASE_SCHEMA.md

Tâche: [DESCRIPTION SPECIFIQUE]

Contraintes:
- Suivre les conventions de CLAUDE.md
- Python 3.11 + FastAPI pour backend
- Next.js 14 App Router pour frontend
- PostgreSQL + Alembic pour DB

Output attendu: [CE QUE TU VEUX]
```

**PHASE 2 - Agents :**

```
@workspace [PHASE 2 - AGENTS IA]

Contexte: J'implémente les agents IA Vectra.
Docs de référence:
- DOC-TECH-004_AGENT_PROMPTS.md
- VECTRA_SPECIFICATION_TECHNIQUE_V2.docx (Section 4)
- REALISATION_TECHNIQUE.docx (Blocs 1-3)

Tâche: Créer l'agent [NOM] qui doit:
1. [Responsabilité 1]
2. [Responsabilité 2]
3. [Responsabilité 3]

Contraintes:
- Utiliser CrewAI framework
- LLM: Llama 2 70B (fallback Claude)
- Latence max: [X] secondes
- Logging structuré

Prompt système de l'agent:
[Copier depuis DOC-TECH-004]

Output attendu: Code complet + tests
```

**PHASE 3 - Core Product :**

```
@workspace [PHASE 3 - CORE PRODUCT]

Contexte: Je crée l'interface utilisateur Vectra.
Docs de référence:
- DOC-UI-001_DESIGN_SYSTEM.md
- DOC-UI-002_COMPONENTS_CATALOG.md
- REALISATION_TECHNIQUE.docx (Partie 2 - UI/UX)

Tâche: Créer la page [NOM] avec:
1. [Section 1]
2. [Section 2]
3. [Section 3]

Contraintes:
- Mobile-first
- Dark mode natif
- Tokens du design system
- Composants de DOC-UI-002

Output attendu: Page + composants + API calls
```

**PHASE 4 - Monétisation :**

```
@workspace [PHASE 4 - MONETISATION]

Contexte: J'implémente le billing Vectra.
Doc de référence: DOC-BIZ-002_BILLING_SUBSCRIPTION.md

Tâche: [DESCRIPTION]

Plans:
- Starter: 99€/mois, 500 leads, 2 campaigns
- Growth: 299€/mois, 2000 leads, 5 campaigns
- Scale: 799€/mois, 10000 leads, unlimited

Contraintes:
- Intégration Stripe
- Webhooks sécurisés
- Rate limiting par plan

Output attendu: [SPECIFIQUE]
```

**PHASE 5 - Activation :**

```
@workspace [PHASE 5 - ACTIVATION]

Contexte: J'implémente l'onboarding Vectra.
Docs de référence:
- DOC-BIZ-001_ONBOARDING_ACTIVATION.md
- DOC-BIZ-003_ANALYTICS_TRACKING.md

Tâche: [DESCRIPTION]

Critères d'activation:
1. Campagne créée
2. Intégration connectée
3. Email approuvé

Time-to-value cible: < 5 minutes

Output attendu: [SPECIFIQUE]
```

---

## 10. CHECKLIST FINALE GO-LIVE

### 10.1 Checklist Technique

```
INFRASTRUCTURE
□ Render (backend) configuré et déployé
□ Vercel (frontend) configuré et déployé
□ PostgreSQL provisionné
□ Redis provisionné
□ SSL/HTTPS actif
□ Domain configuré (vectra.io)
□ CDN actif

CI/CD
□ GitHub Actions fonctionnel
□ Tests automatiques passent
□ Deploy automatique sur merge

MONITORING
□ Sentry configuré (errors)
□ PostHog configuré (analytics)
□ Uptime monitoring actif
□ Alertes configurées

SÉCURITÉ
□ OWASP audit passé
□ Rate limiting actif
□ JWT sécurisé
□ Headers de sécurité
□ Secrets en env vars
```

### 10.2 Checklist Produit

```
CORE FEATURES
□ Auth (register, login, logout, reset)
□ Onboarding wizard (3 steps)
□ Dashboard avec stats
□ Campaigns CRUD
□ Leads list + detail
□ Email approval queue
□ Meetings view

AGENTS
□ Prospector fonctionnel
□ BANT Qualifier fonctionnel
□ Scheduler fonctionnel
□ Orchestration stable

BILLING
□ Stripe live mode
□ 3 plans configurés
□ Checkout fonctionnel
□ Webhooks actifs
□ Dunning configuré

UX
□ Empty states tous présents
□ Loading states
□ Error states
□ Mobile responsive
□ Dark mode
```

### 10.3 Checklist Business

```
LEGAL
□ Terms of Service publiés
□ Privacy Policy publiée
□ Cookie consent
□ DPA disponible

SUPPORT
□ Intercom configuré
□ Help docs publiées
□ FAQ complète
□ Email support actif

ANALYTICS
□ Segment configuré
□ Events critiques trackés
□ Funnels configurés
□ Dashboards créés

CS READY
□ Health score implémenté
□ Playbooks documentés
□ Alertes churn configurées
```

### 10.4 Go-Live Day

```
MATIN
□ Backup de staging
□ Deploy production final
□ Smoke tests manuels
□ Vérifier monitoring
□ Team en standby

MIDI
□ Activer Stripe live
□ Notifier beta users
□ Ouvrir accès public

APRÈS-MIDI
□ Monitor closely (errors, signups)
□ Répondre support immédiatement
□ Fix hotfixes si nécessaire

SOIR
□ Debrief équipe
□ Metrics du jour
□ Plan J+1
```

---

## ANNEXE: DOCUMENTS PAR PHASE

### Quick Reference

| Phase | Semaines | Documents Clés |
|-------|----------|----------------|
| **1. Fondations** | 1-2 | STRUCT-001, STRUCT-002, TECH-001, TECH-003 |
| **2. Agents** | 3-4 | TECH-004, TECH_REVIEW, REALISATION_TECHNIQUE |
| **3. Core Product** | 5-6 | UI-001, UI-002, DECISIONS_PRODUIT |
| **4. Monétisation** | 7-8 | BIZ-002, CAHIER_DE_CHARGES |
| **5. Activation** | 9-10 | BIZ-001, BIZ-003 |
| **6. Launch** | 11-12 | TECH-005, BIZ-004, SPRINT_PLANNING |

### Priorité de Lecture

Pour chaque phase, lire dans cet ordre:
1. **Spec fonctionnelle** (ce qu'on construit)
2. **Spec technique** (comment on le construit)
3. **Design/UI** (à quoi ça ressemble)
4. **Business** (pourquoi c'est important)

---

**- FIN DU DOCUMENT -**

*Master Execution Plan - Vectra v1.0*
*15 Janvier 2026*

---

**RAPPEL IMPORTANT**

Ce document est ton **GPS pour les 12 prochaines semaines**.

À chaque étape:
1. Lis les documents de référence listés
2. Utilise le prompt optimisé fourni
3. Lance la commande Claude Code appropriée
4. Valide avec la checklist de l'étape
5. Passe à l'étape suivante

**Bonne construction !** 🚀
