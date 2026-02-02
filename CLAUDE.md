# VECTRA - Agent IA SaaS pour Ventes B2B

> *Powering your pipeline, simply.*

## 🎯 Vision Produit

Plateforme SaaS d'agents IA autonomes qui automatisent le cycle de vente B2B complet:
**Prospection → Qualification BANT → Prise de RDV**

**Objectifs:**
- Réduire le CAC de 35-45%
- Augmenter le volume de leads de 120%
- ROI client: 6-9 mois
- TCO < $3,000/mois

---

## 🏗️ Architecture Technique

### Stack
| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11 + FastAPI + CrewAI |
| **Frontend** | Next.js 14 + Tailwind + Shadcn/ui |
| **Database** | PostgreSQL 15 + pgvector |
| **Cache/Queue** | Redis 7 + Celery |
| **Agents IA** | CrewAI + Llama 2 70B |
| **Hosting** | Render (API) + Vercel (Web) |
| **UI** | Tailwind + Shadcn/ui | 3.4 |

### Structure Monorepo

```
vectra/
├── backend/                    # Python FastAPI
│   ├── app/
│   │   ├── api/v1/            # REST endpoints
│   │   │   ├── auth.py
│   │   │   ├── campaigns.py
│   │   │   ├── leads.py
│   │   │   ├── emails.py
│   │   │   └── meetings.py
│   │   ├── agents/            # CrewAI agents
│   │   │   ├── prospector.py
│   │   │   ├── bant.py
│   │   │   └── scheduler.py
│   │   ├── core/              # Config, security
│   │   ├── models/            # SQLAlchemy
│   │   ├── schemas/           # Pydantic
│   │   ├── services/          # Business logic
│   │   └── tasks/             # Celery tasks
│   ├── tests/
│   ├── alembic/               # Migrations
│   └── pyproject.toml
│
├── frontend/                   # Next.js 14
│   ├── app/                   # App Router
│   │   ├── (auth)/
│   │   ├── (dashboard)/
│   │   └── api/
│   ├── components/
│   │   ├── ui/                # Shadcn
│   │   └── features/          # Domain
│   ├── lib/
│   └── package.json
│
├── docs/                       # Documentation
│   ├── tech/
│   ├── api/
│   └── decisions/
│
├── .claude/                    # Claude Code config
├── CLAUDE.md                   # This file
└── .mcp.json                   # MCP servers
```

---

## 📊 Modèle de Données

### Entités Principales

```
organizations (Multi-tenant root)
├── users (RBAC: owner|admin|manager|operator|viewer)
├── campaigns
│   ├── leads (BANT score 0-100)
│   │   ├── emails (pending|approved|sent|opened|clicked)
│   │   └── meetings (scheduled|completed|no_show)
│   └── agent_runs
├── subscriptions (Stripe)
└── integrations (HubSpot, Calendly)
```

### Relations Clés
- `organizations` 1:N `users`, `campaigns`, `subscriptions`
- `campaigns` 1:N `leads`, `agent_runs`
- `leads` 1:N `emails`, 1:1 `meetings`

---

## 🤖 Les 3 Agents IA

### 1. Agent Prospector
- **Rôle**: Recherche + enrichissement leads
- **Input**: Critères de ciblage (job titles, geo, taille)
- **Output**: Liste de prospects enrichis
- **API**: RocketReach
- **Exécution**: Asynchrone (Celery)

### 2. Agent BANT Qualifier
- **Rôle**: Score BANT 0-100
- **Critères**:
  - Budget (0-25): Taille entreprise
  - Authority (0-25): Niveau décisionnel
  - Need (0-25): Signaux de besoin
  - Timeline (0-25): Activité récente
- **Règle**: Score ≥ 60 → Qualified
- **Exécution**: Synchrone (<30s)

### 3. Agent Scheduler
- **Rôle**: Email personnalisé + booking
- **Output**: Email draft + lien Calendly
- **API**: SendGrid + Calendly
- **Exécution**: Asynchrone

---

## 📋 Conventions de Code

### Backend (Python)

```python
# ✅ Type hints obligatoires
async def create_campaign(data: CampaignCreate) -> Campaign:
    ...

# Nommage
class LeadService:        # PascalCase pour classes
def get_qualified_leads(): # snake_case pour fonctions
MAX_RETRIES = 3           # UPPER_SNAKE pour constantes

# Imports (ordre)
import os                          # stdlib
from fastapi import APIRouter      # third-party
from app.services import LeadService # local

# ✅ Docstrings Google style
def calculate_bant_score(lead: Lead) -> int:
    """Calculate BANT score for a lead.
    
    Args:
        lead: Lead object with enrichment data.
        
    Returns:
        BANT score between 0 and 100.
    """
    ...

# ✅ Multi-tenant filter TOUJOURS
stmt = select(Campaign).where(
    Campaign.organization_id == current_user.organization_id
)

# ✅ Service layer pattern
class LeadService:
    def __init__(self, db: AsyncSession, org_id: UUID):
        self.db = db
        self.org_id = org_id
```

### Frontend (TypeScript)

```typescript
// ✅ Strict mode, interfaces
interface CampaignProps {
  campaign: Campaign
  onSelect: (id: string) => void
}

// ✅ Functional components
export function CampaignCard({ campaign, onSelect }: CampaignProps) {
  return (...)
}

// ✅ React Query for data
const { data, isLoading } = useCampaigns()

// ✅ Zod for validation
const schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
})
```

### SQL

```sql
-- Tables: snake_case, pluriel
CREATE TABLE leads (...);

-- Index: idx_{table}_{columns}
CREATE INDEX idx_leads_campaign_id ON leads(campaign_id);
```

---

## 🔧 Commandes Utiles

### Backend
```bash
cd backend

# Run dev server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest -v --cov=app

# Lint & format
uv run ruff check . --fix
uv run ruff format .

# Migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend
```bash
cd frontend

# Run dev server
npm run dev

# Build
npm run build

# Tests
npm run test

# Lint
npm run lint
```

### Tests

```bash
# Tous les tests
make test

# Backend avec coverage
cd backend && pytest --cov=app

# Frontend
cd frontend && npm run test

# E2E
cd frontend && npm run test:e2e
```

### Linting

```bash
# Tout
make lint

# Backend
cd backend && black . && ruff check .

# Frontend
cd frontend && npm run lint
```

### Git
```bash
# Create feature branch
git checkout -b feature/my-feature

# Commit (conventional commits)
git commit -m "feat: add campaign creation"
git commit -m "fix: resolve BANT scoring bug"
git commit -m "docs: update API documentation"
```

---

## 🚨 Règles Critiques

### OBLIGATOIRE ✅
1. Créer branche `feature/*` avant toute modification
2. Écrire tests AVANT le code (TDD)
3. Type hints sur toutes les fonctions
4. Multi-tenant filter sur TOUTES les queries
5. Documenter les nouveaux endpoints

### INTERDIT ❌
1. Commit directement sur `main`
2. Hardcoder des secrets
3. Utiliser `any` en TypeScript
4. Queries sans filtre `organization_id`
5. Code sans tests

---

## 🎨 Design System

### Couleurs (Dark mode par défaut)
| Token | Valeur | Usage |
|-------|--------|-------|
| `primary` | `#2E5BFF` | Actions principales |
| `accent` | `#FF9F43` | Accents (parcimonieux) |
| `bg-dark` | `#0E1117` | Background |
| `success` | `#22C55E` | Validation |
| `error` | `#EF4444` | Erreurs |

### Spacing
Système 8px: `4, 8, 12, 16, 24, 32, 48, 64`

### Composants
- Utiliser Shadcn/ui
- Tailwind pour styling
- Mobile-first

---

## 📁 Fichiers Importants à Lire

| Besoin | Fichier |
|--------|---------|
| Architecture | `docs/tech/SPECIFICATION_TECHNIQUE.md` |
| API specs | `docs/api/openapi.yaml` |
| DB schema | `docs/tech/DATABASE_SCHEMA.md` |
| Agent prompts | `backend/app/agents/*.py` |
| Design tokens | `frontend/app/globals.css` |
| Décisions | `docs/decisions/ADR-*.md` |

---

## 🤖 AGENTS IA - RÈGLES

### Agent BANT - Scoring

```
Score = Budget(0-25) + Authority(0-25) + Need(0-25) + Timeline(0-25)
Total: 0-100

- Score ≥ 60 → Qualifié → Créer email
- Score 40-59 → Nurture
- Score < 40 → Rejeté
```

### Prompts

Les prompts sont dans `backend/app/agents/{agent}/prompts.py`.
Ne jamais modifier les prompts sans A/B test préalable.

### Rate Limiting

- RocketReach: 50 req/min
- SendGrid: 50 emails/jour/campagne
- LLM: pas de limite mais surveiller les coûts

---

## 🔐 SÉCURITÉ

### Règles Critiques

1. **TOUJOURS** filtrer par `organization_id` dans les queries (endpoints `/user/*`)
2. **JAMAIS** de secrets dans le code (utiliser .env)
3. **TOUJOURS** valider les inputs avec Pydantic
4. JWT expire après 15 min, refresh après 7 jours
5. **Isolation multi-tenant:** Tous les endpoints `/user/*` DOIVENT filtrer par `organization_id`
6. **Platform Admin:** Seuls les utilisateurs avec `role=PLATFORM_ADMIN` et `organization_id=NULL` peuvent accéder à `/admin/*`

### Patterns de Sécurité

```python
# Bon: filtrage multi-tenant
leads = await repo.list(organization_id=current_user.organization_id)

# Mauvais: pas de filtrage
leads = await repo.list()  # DANGER!

# Bon: Platform Admin (pas de filtrage multi-tenant)
if current_user.role == UserRole.PLATFORM_ADMIN:
    orgs = await repo.list_all_organizations()  # OK pour /admin/*
```

### Structure des Routes

**Routes Public (`/api/v1/auth/*`):**
- `POST /auth/login` - Connexion
- `POST /auth/register` - Inscription (peut créer PLATFORM_ADMIN si email correspond)
- `POST /auth/invite/accept` - Accepter invitation avec OTP

**Routes Utilisateur (`/api/v1/user/*`):**
- **Isolation stricte:** TOUJOURS filtrer par `organization_id` de l'utilisateur connecté
- `GET /user/me` - Profil utilisateur
- `GET /user/organizations/me` - Organisation de l'utilisateur
- `PATCH /user/organizations/me` - Modifier organisation (Owner/Admin)
- `GET /user/organizations/me/users` - Lister utilisateurs (Owner/Admin/Manager)
- `POST /user/organizations/me/users/invite` - Inviter utilisateur (Owner/Admin)
- `POST /user/organizations/me/users/create` - Créer utilisateur directement (Owner/Admin)
- `PATCH /user/organizations/me/users/{id}/role` - Modifier rôle (Owner/Admin)
- `DELETE /user/organizations/me/users/{id}` - Retirer utilisateur (Owner/Admin)
- `GET /user/campaigns` - Lister campagnes (filtré par org)
- `POST /user/campaigns` - Créer campagne (filtré par org)
- `POST /user/notifications/send` - Envoyer notification (org)

**Routes Platform Admin (`/api/v1/admin/*`):**
- **Pas d'isolation:** Accès à toutes les données de la plateforme
- **Permission:** Uniquement `PLATFORM_ADMIN` (vérifier avec `get_platform_admin`)
- `GET /admin/overview` - Vue d'ensemble plateforme
- `GET /admin/organizations` - Lister toutes les organisations
- `POST /admin/organizations` - Créer organisation
- `GET /admin/users` - Lister tous les utilisateurs
- `GET /admin/system/metrics` - Métriques système
- `POST /admin/notifications/send` - Envoyer notification (plateforme)

---

## 💡 Tips pour Claude Code

### Utiliser les Skills
```
# Les skills s'activent automatiquement quand pertinents
# Mais tu peux aussi les invoquer explicitement:
/vectra-patterns
/fastapi-backend
/nextjs-frontend
```

### Utiliser les Subagents
```
# Demander une review
"Spawn code-reviewer to review my changes"

# Recherche
/research <topic>

# Architecture
"Consult architect agent about caching strategy"
```

### Commandes Rapides
```
/implement <feature>     # Implémenter avec TDD
/review                  # Code review
/create-endpoint <name>  # Nouveau endpoint API
/create-component <name> # Nouveau composant React
```

---

## ⚠️ PIÈGES À ÉVITER

1. **Ne pas** créer de routes sans vérifier l'organization_id (pour `/user/*`)
2. **Ne pas** utiliser `/admin/*` pour les fonctionnalités utilisateur (utiliser `/user/*`)
3. **Ne pas** oublier le workflow: créer un log AVANT de commencer à coder
4. **Ne pas** appeler les APIs externes sans rate limiting
5. **Ne pas** modifier les prompts sans documenter
6. **Ne pas** merger sans tests passants
7. **Ne pas** utiliser de `print()`, utiliser `logger`
8. **Ne pas** créer d'endpoints sans documentation dans `DOC-TECH-002_API_CONTRACTS.md`

---

## 🚀 COMMANDES CLAUDE CODE

Utilise `/nom` pour les commandes personnalisées:

- `/create-agent` - Créer un nouvel agent IA
- `/create-endpoint` - Créer un endpoint API
- `/create-migration` - Créer une migration DB
- `/write-test` - Écrire des tests (unit, integration, e2e, component)
- `/run-tests` - Lancer les tests
- `/deploy` - Déployer en staging/prod
- `/debug` - Aide au debugging

**Workflow complet:** Voir `docs/workflow/WORKFLOW_ORCHESTRATION.md` pour le processus de développement structuré.

**⚠️ IMPORTANT:** Suivre TOUJOURS le workflow dans `docs/workflow/WORKFLOW_ORCHESTRATION.md`:
1. **Créer un log d'activité** avant de commencer (`docs/workflow/logs/{type}/YYYY-MM-DD_{type}_{nom}.md`)
2. **Documenter** toutes les modifications dans le log
3. **Mettre à jour** `docs/workflow/STATUS.md` après chaque étape importante
4. **Créer des tests** pour toute nouvelle fonctionnalité
5. **Documenter** les endpoints dans `docs/tech/DOC-TECH-002_API_CONTRACTS.md`

---

## 📞 EN CAS DE DOUTE

1. Consulter les docs dans `/docs/`
2. Regarder les patterns existants dans le code
3. Si décision d'architecture → créer un ADR
4. Si bug critique → voir `RUNBOOK.md`

---

---

## 📋 WORKFLOW OBLIGATOIRE

**TOUJOURS suivre** `docs/workflow/WORKFLOW_ORCHESTRATION.md` pour toute modification:

1. **Avant de coder:**
   - Identifier le type de travail (feature, component, API, etc.)
   - Créer le log dans `docs/workflow/logs/{type}/YYYY-MM-DD_{type}_{nom}.md`
   - Consulter les docs de référence

2. **Pendant le développement:**
   - Documenter chaque étape dans le log
   - Créer les tests (unit, integration, E2E selon le cas)
   - Mettre à jour la documentation API si nécessaire

3. **Après le développement:**
   - Mettre à jour le log avec statut `completed`
   - Mettre à jour `docs/workflow/STATUS.md`
   - Vérifier que tous les tests passent

**Règle d'or:** Créer le log AVANT de commencer à coder.

---

*Dernière mise à jour: Janvier 2026*
