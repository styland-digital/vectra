# VECTRA - Instructions pour Claude Code

> Ce fichier est lu automatiquement par Claude Code au démarrage.
> Il contient toutes les informations nécessaires pour travailler sur ce projet.

---

## 🎯 PROJET EN UN MOT

**Vectra** = Plateforme SaaS d'agents IA pour automatiser la prospection B2B (prospection → qualification BANT → emails personnalisés → rendez-vous).

---

## 🏗️ ARCHITECTURE

### Stack Technique

| Layer | Technologie | Version |
|-------|-------------|---------|
| **Backend** | Python + FastAPI | 3.11 / 0.109 |
| **Frontend** | Next.js + React | 14 / 18 |
| **Database** | PostgreSQL | 15 |
| **Cache/Queue** | Redis + Celery | 7 / 5.3 |
| **Agents IA** | CrewAI + Llama 2 | - |
| **UI** | Tailwind + Shadcn/ui | 3.4 |

### Les 3 Agents IA

1. **Prospector** - Trouve des prospects selon critères (RocketReach API)
2. **BANT** - Qualifie chaque prospect (score 0-100)
3. **Scheduler** - Génère emails personnalisés + Calendly

### Architecture Multi-Tenant

- Chaque client = une `Organization`
- Isolation stricte des données via `organization_id`
- Rôles: Owner > Admin > Manager > Operator > Viewer
- **Route Structure:**
  - `/api/v1/auth/*` - Authentification (public)
  - `/api/v1/user/*` - Utilisateurs et organisations (authentifié, multi-tenant)
  - `/api/v1/admin/*` - Administration plateforme (PLATFORM_ADMIN uniquement)

---

## 📁 STRUCTURE DU PROJET

```
vectra/
├── backend/           # API FastAPI + Agents CrewAI
│   ├── app/
│   │   ├── api/v1/   # Routes REST
│   │   ├── agents/   # Prospector, BANT, Scheduler
│   │   ├── db/       # Models SQLAlchemy + Repositories
│   │   ├── services/ # Business logic
│   │   └── tasks/    # Celery tasks
│   └── tests/
├── frontend/          # Next.js Dashboard
│   ├── app/          # App Router
│   ├── components/   # React + Shadcn/ui
│   └── lib/          # Utils, API client
└── docs/             # Documentation
```

---

## 🎨 CONVENTIONS DE CODE

### Python (Backend)

```python
# Nommage
class LeadService:        # PascalCase pour classes
def get_qualified_leads(): # snake_case pour fonctions
MAX_RETRIES = 3           # UPPER_SNAKE pour constantes

# Imports (ordre)
import os                          # stdlib
from fastapi import APIRouter      # third-party
from app.services import LeadService # local

# Type hints obligatoires
def score_lead(lead_id: UUID) -> BANTScore:
    ...
```

### TypeScript (Frontend)

```typescript
// Components: PascalCase
function LeadCard({ lead }: LeadCardProps) { }

// Hooks: useXxx
function useLeads() { }

// Types: PascalCase
interface Lead { }
type LeadStatus = 'new' | 'qualified';
```

### SQL

```sql
-- Tables: snake_case, pluriel
CREATE TABLE leads (...);

-- Index: idx_{table}_{columns}
CREATE INDEX idx_leads_campaign_id ON leads(campaign_id);
```

---

## 🔧 COMMANDES UTILES

### Développement

```bash
# Démarrer l'environnement
make dev

# Backend seul
cd backend && uvicorn app.main:app --reload

# Frontend seul
cd frontend && npm run dev

# Celery worker
cd backend && celery -A app.tasks.celery_app worker --loglevel=INFO
```

### Base de données

```bash
# Créer une migration
make migrate-new msg="add_new_field"

# Appliquer les migrations
make migrate

# Seed data
make seed
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

---

## 📊 BASE DE DONNÉES

### Tables Principales

| Table | Description |
|-------|-------------|
| `organizations` | Entreprises clientes (multi-tenant) |
| `users` | Utilisateurs par org |
| `campaigns` | Campagnes de prospection |
| `leads` | Prospects trouvés et qualifiés |
| `interactions` | Historique actions (immutable) |
| `emails` | Emails générés et envoyés |
| `meetings` | RDVs Calendly |
| `agent_jobs` | Jobs des agents IA |
| `audit_logs` | Logs d'audit |

### ENUMs Importants

```python
lead_status = ['new', 'enriched', 'qualified', 'contacted', 'responded', 'meeting', 'converted', 'rejected', 'bounced']
lead_intent = ['interested_now', 'interested_later', 'objection_price', 'polite_decline', 'not_interested', ...]
campaign_status = ['draft', 'pending', 'active', 'paused', 'completed', 'cancelled']
user_role = ['owner', 'admin', 'manager', 'operator', 'viewer']
```

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

## 📝 DOCUMENTATION DE RÉFÉRENCE

Tous les documents sont dans `/docs/`:

| Document | Contenu |
|----------|---------|
| `SPECIFICATION_TECHNIQUE_V2.md` | Architecture complète |
| `SCHEMA_DATABASE.md` | Tables, ENUMs, index |
| `CONTRATS_API.md` | Endpoints OpenAPI |
| `ADR/` | Décisions d'architecture |
| `PROMPTS_TEMPLATES.md` | Prompts des agents |
| `PLAN_TESTS.md` | Stratégie de test |

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

*Dernière mise à jour: 18 Janvier 2026*
