# VECTRA - STRUCTURE MONOREPO & CONFIGURATION

## Architecture du Code Source

### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-011  
**Statut:** RÉFÉRENCE TECHNIQUE  
**Usage:** Structure à respecter pour tout le développement  

---

## 1. STRUCTURE COMPLÈTE DU MONOREPO

```
vectra/
├── .claude/                      # Configuration Claude Code
│   ├── CLAUDE.md                # Instructions principales
│   ├── commands/                # Commandes personnalisées
│   │   ├── create-agent.md
│   │   ├── create-endpoint.md
│   │   ├── create-migration.md
│   │   ├── run-tests.md
│   │   ├── deploy.md
│   │   └── debug.md
│   └── context/                 # Contexte additionnel
│       ├── architecture.md
│       ├── conventions.md
│       └── stack.md
│
├── backend/                     # API FastAPI + Agents
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # Entry point FastAPI
│   │   ├── config.py           # Settings Pydantic
│   │   │
│   │   ├── api/                # Routes API
│   │   │   ├── __init__.py
│   │   │   ├── deps.py         # Dependencies (auth, db)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py   # Router principal
│   │   │       ├── auth.py
│   │   │       ├── campaigns.py
│   │   │       ├── leads.py
│   │   │       ├── emails.py
│   │   │       ├── meetings.py
│   │   │       ├── analytics.py
│   │   │       └── webhooks.py
│   │   │
│   │   ├── agents/             # Agents IA CrewAI
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # BaseVectraAgent
│   │   │   ├── prospector/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── tools.py
│   │   │   │   └── prompts.py
│   │   │   ├── bant/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── scorer.py
│   │   │   │   └── prompts.py
│   │   │   ├── scheduler/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── email_generator.py
│   │   │   │   └── prompts.py
│   │   │   └── intent/
│   │   │       ├── __init__.py
│   │   │       ├── classifier.py
│   │   │       └── prompts.py
│   │   │
│   │   ├── core/               # Config, security, exceptions
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   │
│   │   ├── db/                 # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── session.py      # SQLAlchemy session
│   │   │   ├── base.py         # Base model
│   │   │   ├── models/         # SQLAlchemy models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── organization.py
│   │   │   │   ├── user.py
│   │   │   │   ├── campaign.py
│   │   │   │   ├── lead.py
│   │   │   │   ├── interaction.py
│   │   │   │   ├── email.py
│   │   │   │   ├── meeting.py
│   │   │   │   ├── agent_job.py
│   │   │   │   └── audit_log.py
│   │   │   └── repositories/   # Data access layer
│   │   │       ├── __init__.py
│   │   │       ├── base.py
│   │   │       ├── organization.py
│   │   │       ├── user.py
│   │   │       ├── campaign.py
│   │   │       └── lead.py
│   │   │
│   │   ├── services/           # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── campaign.py
│   │   │   ├── lead.py
│   │   │   ├── bant.py
│   │   │   ├── email.py
│   │   │   └── analytics.py
│   │   │
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── organization.py
│   │   │   ├── user.py
│   │   │   ├── campaign.py
│   │   │   ├── lead.py
│   │   │   ├── email.py
│   │   │   └── common.py
│   │   │
│   │   ├── tasks/              # Celery tasks
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   ├── prospector.py
│   │   │   ├── bant.py
│   │   │   ├── scheduler.py
│   │   │   └── email.py
│   │   │
│   │   └── utils/              # Utilities
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       ├── formatters.py
│   │       └── crypto.py
│   │
│   ├── tests/                  # Tests backend
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── services/
│   │   │   ├── agents/
│   │   │   └── utils/
│   │   ├── integration/
│   │   │   ├── api/
│   │   │   └── db/
│   │   └── e2e/
│   │
│   ├── alembic/                # Database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   │
│   ├── scripts/                # Utility scripts
│   │   ├── seed_database.py
│   │   └── create_admin.py
│   │
│   ├── pyproject.toml          # Python config
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── alembic.ini
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # Next.js Dashboard
│   ├── app/                    # App Router (Next.js 14)
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── (auth)/             # Auth group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   └── forgot-password/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/        # Dashboard group
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx        # Dashboard home
│   │   │   ├── campaigns/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── new/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   ├── leads/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   ├── emails/
│   │   │   │   └── page.tsx
│   │   │   ├── meetings/
│   │   │   │   └── page.tsx
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   └── api/                # API routes Next.js
│   │       └── health/
│   │           └── route.ts
│   │
│   ├── components/             # React components
│   │   ├── ui/                 # Shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── table.tsx
│   │   │   └── ...
│   │   ├── layout/             # Layout components
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── footer.tsx
│   │   └── features/           # Feature components
│   │       ├── campaigns/
│   │       │   ├── campaign-card.tsx
│   │       │   ├── campaign-form.tsx
│   │       │   └── campaign-wizard.tsx
│   │       ├── leads/
│   │       │   ├── lead-card.tsx
│   │       │   ├── lead-table.tsx
│   │       │   └── bant-score.tsx
│   │       └── emails/
│   │           ├── email-preview.tsx
│   │           └── email-approval.tsx
│   │
│   ├── lib/                    # Utilities
│   │   ├── api.ts              # API client
│   │   ├── auth.ts             # Auth helpers
│   │   ├── utils.ts            # General utils
│   │   └── validations.ts
│   │
│   ├── hooks/                  # Custom hooks
│   │   ├── use-auth.ts
│   │   ├── use-campaigns.ts
│   │   ├── use-leads.ts
│   │   └── use-toast.ts
│   │
│   ├── stores/                 # Zustand stores
│   │   ├── auth-store.ts
│   │   └── ui-store.ts
│   │
│   ├── types/                  # TypeScript types
│   │   ├── index.ts
│   │   ├── api.ts
│   │   ├── campaign.ts
│   │   └── lead.ts
│   │
│   ├── __tests__/              # Frontend tests
│   │   └── components/
│   │
│   ├── e2e/                    # Playwright E2E
│   │   ├── campaigns.spec.ts
│   │   └── leads.spec.ts
│   │
│   ├── public/                 # Static files
│   │   └── logo.svg
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── postcss.config.js
│   ├── playwright.config.ts
│   ├── Dockerfile
│   └── .env.example
│
├── docs/                       # Documentation
│   ├── specs/                  # Specifications
│   │   ├── VECTRA_SPECIFICATION_TECHNIQUE_V2.md
│   │   ├── SCHEMA_DATABASE.md
│   │   └── CONTRATS_API.md
│   ├── guides/                 # Guides
│   │   ├── GUIDE_DEVELOPPEUR.md
│   │   └── DOCUMENTATION_UTILISATEUR.md
│   ├── adr/                    # Architecture Decision Records
│   │   ├── ADR-001-crewai.md
│   │   ├── ADR-002-llama2.md
│   │   └── ...
│   └── operations/             # Ops docs
│       ├── RUNBOOK.md
│       └── PLAYBOOK_COMMERCIAL.md
│
├── scripts/                    # Scripts globaux
│   ├── setup.sh               # Setup initial
│   ├── dev.sh                 # Lancer dev
│   └── deploy.sh              # Déploiement
│
├── .github/                    # GitHub config
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── deploy.yml
│   └── PULL_REQUEST_TEMPLATE.md
│
├── docker-compose.yml          # Dev environment
├── docker-compose.prod.yml     # Production
├── Makefile                    # Commandes make
├── README.md
├── LICENSE
└── .gitignore
```

---

## 2. FICHIERS DE CONFIGURATION

### 2.1 docker-compose.yml (Développement)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: vectra-postgres
    environment:
      POSTGRES_USER: vectra
      POSTGRES_PASSWORD: vectra
      POSTGRES_DB: vectra
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vectra"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: vectra-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: vectra-backend
    environment:
      - DATABASE_URL=postgresql://vectra:vectra@postgres:5432/vectra
      - REDIS_URL=redis://redis:6379/0
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: vectra-celery
    environment:
      - DATABASE_URL=postgresql://vectra:vectra@postgres:5432/vectra
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./backend:/app
    depends_on:
      - backend
    command: celery -A app.tasks.celery_app worker --loglevel=INFO

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: vectra-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/v1
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
```

### 2.2 backend/pyproject.toml

```toml
[project]
name = "vectra-backend"
version = "1.0.0"
description = "Vectra AI Sales Agents - Backend API"
requires-python = ">=3.11"

[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
asyncio_mode = "auto"
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
fail_under = 80
```

### 2.3 backend/requirements.txt

```
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1
psycopg2-binary==2.9.9

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Task Queue
celery==5.3.6
redis==5.0.1

# AI/LLM
crewai==0.1.0
langchain==0.1.0
ollama==0.1.0

# External APIs
httpx==0.26.0
sendgrid==6.11.0

# Utils
python-dotenv==1.0.0
tenacity==8.2.3

# Monitoring
opentelemetry-api==1.22.0
opentelemetry-sdk==1.22.0
opentelemetry-instrumentation-fastapi==0.43b0
structlog==24.1.0
```

### 2.4 backend/requirements-dev.txt

```
-r requirements.txt

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
httpx==0.26.0
factory-boy==3.3.0

# Code Quality
black==24.1.0
ruff==0.1.14
mypy==1.8.0
pre-commit==3.6.0

# Debug
ipython==8.20.0
rich==13.7.0
```

### 2.5 frontend/package.json

```json
{
  "name": "vectra-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-query": "^5.17.0",
    "zustand": "^4.5.0",
    "zod": "^3.22.4",
    "react-hook-form": "^7.49.3",
    "@hookform/resolvers": "^3.3.4",
    "axios": "^1.6.5",
    "date-fns": "^3.2.0",
    "lucide-react": "^0.312.0",
    "recharts": "^2.10.4",
    "tailwindcss-animate": "^1.0.7",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "eslint": "^8.56.0",
    "eslint-config-next": "14.1.0",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.2.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "@playwright/test": "^1.41.0"
  }
}
```

### 2.6 Makefile

```makefile
.PHONY: help install dev test lint build deploy

help:
 @echo "Vectra - Available commands:"
 @echo "  make install    - Install all dependencies"
 @echo "  make dev        - Start development environment"
 @echo "  make test       - Run all tests"
 @echo "  make lint       - Run linters"
 @echo "  make build      - Build for production"
 @echo "  make migrate    - Run database migrations"
 @echo "  make seed       - Seed database with test data"

install:
 cd backend && pip install -r requirements-dev.txt
 cd frontend && npm install

dev:
 docker-compose up -d postgres redis
 @echo "Starting backend..."
 cd backend && uvicorn app.main:app --reload --port 8000 &
 @echo "Starting frontend..."
 cd frontend && npm run dev

test:
 cd backend && pytest --cov=app
 cd frontend && npm run test

test-e2e:
 cd frontend && npm run test:e2e

lint:
 cd backend && black . && ruff check .
 cd frontend && npm run lint

build:
 cd backend && docker build -t vectra-backend .
 cd frontend && npm run build

migrate:
 cd backend && alembic upgrade head

migrate-new:
 cd backend && alembic revision --autogenerate -m "$(msg)"

seed:
 cd backend && python -m scripts.seed_database

clean:
 docker-compose down -v
 find . -type d -name __pycache__ -exec rm -rf {} +
 find . -type d -name .pytest_cache -exec rm -rf {} +
```

---

## 3. FICHIERS D'ENVIRONNEMENT

### 3.1 backend/.env.example

```bash
# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
SECRET_KEY=change-me-in-production

# Database
DATABASE_URL=postgresql://vectra:vectra@localhost:5432/vectra

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# LLM
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=https://api.ollama.com
OLLAMA_MODEL=llama2:70b
# Fallback Claude (if needed)
CLAUDE_API_KEY=

# External APIs
ROCKETREACH_API_KEY=
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=noreply@vectra.io
CALENDLY_API_KEY=
HUBSPOT_API_KEY=

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
EMAIL_DAILY_LIMIT=50

# Monitoring
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
SENTRY_DSN=
```

### 3.2 frontend/.env.example

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Auth
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000

# Analytics (optional)
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=
```

---

## 4. ORDRE D'IMPLÉMENTATION

### Phase 1: Fondation (Semaine 1-2)

```
1. [ ] Créer la structure du monorepo
2. [ ] Configurer Docker Compose
3. [ ] Setup backend FastAPI basique
4. [ ] Setup frontend Next.js basique
5. [ ] Configurer la base de données
6. [ ] Créer les migrations initiales
7. [ ] Setup CI/CD GitHub Actions
```

### Phase 2: Backend Core (Semaine 3-4)

```
1. [ ] Implémenter les models SQLAlchemy
2. [ ] Créer les repositories
3. [ ] Implémenter auth (JWT)
4. [ ] Créer les endpoints API CRUD
5. [ ] Setup Celery + Redis
6. [ ] Tests unitaires services
```

### Phase 3: Agents (Semaine 5-6)

```
1. [ ] Setup CrewAI
2. [ ] Implémenter Agent Prospector
3. [ ] Implémenter Agent BANT
4. [ ] Implémenter Agent Scheduler
5. [ ] Créer les tasks Celery
6. [ ] Tests agents
```

### Phase 4: Frontend (Semaine 7-8)

```
1. [ ] Layout et navigation
2. [ ] Pages auth (login, register)
3. [ ] Dashboard
4. [ ] Campaigns (list, create, detail)
5. [ ] Leads (list, detail)
6. [ ] Email approval
7. [ ] Analytics
```

### Phase 5: Intégrations (Semaine 9-10)

```
1. [ ] RocketReach API
2. [ ] SendGrid email
3. [ ] Calendly
4. [ ] HubSpot sync
5. [ ] Tests E2E
```

### Phase 6: Polish (Semaine 11-12)

```
1. [ ] Security audit
2. [ ] Performance optimization
3. [ ] Documentation finale
4. [ ] Beta testing
5. [ ] Production deployment
```

---

**- FIN DU DOCUMENT -**

*14 Janvier 2026*
