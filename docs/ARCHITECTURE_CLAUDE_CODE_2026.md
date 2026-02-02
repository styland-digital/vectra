# ARCHITECTURE .CLAUDE OPTIMISÉE POUR VECTRA
## Claude Code 2.1+ | Janvier 2026
### Guide Complet: Skills, Agents, Hooks, MCP, Commands

---

## 🔄 NOUVEAUTÉS CLAUDE CODE 2025-2026

### Évolution Majeure (176 updates en 2025)

| Feature | Date | Impact |
|---------|------|--------|
| **CLAUDE.md** | Feb 2025 | Mémoire projet persistante |
| **Plan Mode** | Mid 2025 | Planification structurée |
| **Subagents** | Mid 2025 | Agents parallèles isolés |
| **/context command** | Mid 2025 | Gestion contexte |
| **Agent Skills** | Oct 2025 | Connaissances procédurales |
| **Hooks** | Late 2025 | Automatisation events |
| **Plugins** | Late 2025 | Distribution de configs |
| **Background tasks** | Dec 2025 | Subagents en arrière-plan |
| **Opus 4.5** | Dec 2025 | Modèle amélioré |
| **v2.1.0** | Jan 2026 | Hooks scoped, MCP dynamique |

---

## 📁 STRUCTURE COMPLÈTE .CLAUDE

```
vectra/
│
├── CLAUDE.md                      # 🧠 Mémoire principale (OBLIGATOIRE)
│
├── .claude/
│   │
│   ├── settings.json              # ⚙️ Configuration & Hooks
│   ├── settings.local.json        # 🔒 Settings locaux (gitignored)
│   │
│   ├── agents/                    # 🤖 Subagents spécialisés
│   │   ├── architect.md
│   │   ├── code-reviewer.md
│   │   ├── tdd-guide.md
│   │   ├── security-reviewer.md
│   │   ├── doc-updater.md
│   │   ├── api-designer.md
│   │   ├── frontend-specialist.md
│   │   ├── database-expert.md
│   │   └── devops-engineer.md
│   │
│   ├── skills/                    # 📚 Connaissances procédurales
│   │   ├── vectra-patterns/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   ├── fastapi-backend/
│   │   │   ├── SKILL.md
│   │   │   └── templates/
│   │   ├── nextjs-frontend/
│   │   │   ├── SKILL.md
│   │   │   └── components/
│   │   ├── crewai-agents/
│   │   │   ├── SKILL.md
│   │   │   └── examples/
│   │   ├── testing-patterns/
│   │   │   └── SKILL.md
│   │   └── database-migrations/
│   │       └── SKILL.md
│   │
│   ├── commands/                  # ⚡ Slash commands personnalisées
│   │   ├── implement.md           # /implement <feature>
│   │   ├── review.md              # /review
│   │   ├── test.md                # /test <scope>
│   │   ├── deploy.md              # /deploy <env>
│   │   ├── fix-issue.md           # /fix-issue <number>
│   │   ├── create-migration.md    # /create-migration <name>
│   │   ├── create-endpoint.md     # /create-endpoint <name>
│   │   ├── create-component.md    # /create-component <name>
│   │   └── research.md            # /research <topic>
│   │
│   └── hooks/                     # 🪝 Scripts d'automatisation
│       ├── pre-commit-check.sh
│       ├── post-edit-format.sh
│       ├── skill-activation.sh
│       └── test-runner.sh
│
├── .mcp.json                      # 🔌 Serveurs MCP (projet)
│
└── docs/                          # 📖 Documentation référencée
    ├── architecture/
    ├── api/
    └── decisions/
```

---

## 1️⃣ CLAUDE.md - MÉMOIRE PROJET

Le fichier le plus important. Claude le lit à chaque session.

```markdown
# VECTRA - Agent IA SaaS pour Ventes B2B

## 🎯 Vision
Plateforme SaaS d'agents IA autonomes pour automatiser prospection → qualification → RDV.

## 🏗️ Architecture

### Stack Technique
- **Backend**: Python 3.11 + FastAPI + CrewAI
- **Frontend**: Next.js 14 + Tailwind + Shadcn/ui
- **Database**: PostgreSQL 15 + pgvector + Redis 7
- **Agents**: CrewAI + Llama 2 70B (fallback Claude API)
- **Infra**: Render (backend) + Vercel (frontend)

### Structure Monorepo
```
vectra/
├── backend/           # FastAPI + CrewAI
│   ├── app/
│   │   ├── api/v1/    # Endpoints REST
│   │   ├── agents/    # 3 agents IA
│   │   ├── models/    # SQLAlchemy models
│   │   └── services/  # Business logic
│   └── tests/
├── frontend/          # Next.js 14
│   ├── app/           # App Router
│   ├── components/    # UI components
│   └── lib/           # Utils
└── docs/              # Documentation
```

## 📋 Conventions de Code

### Backend (Python)
- Type hints obligatoires
- Docstrings Google style
- Tests pytest avec coverage > 80%
- Formatter: ruff
- Async/await pour I/O

### Frontend (TypeScript)
- Strict mode activé
- Composants fonctionnels React
- Tailwind pour styling
- Zod pour validation
- React Query pour data fetching

## 🔧 Commandes Utiles

```bash
# Backend
cd backend && uv run pytest
cd backend && uv run ruff check .
cd backend && alembic upgrade head

# Frontend
cd frontend && npm run dev
cd frontend && npm run build
cd frontend && npm run test
```

## 🚨 Règles Critiques

1. **JAMAIS** modifier directement sur main
2. **TOUJOURS** créer une branche feature/*
3. **TOUJOURS** écrire des tests avant le code
4. **JAMAIS** commiter des secrets (.env)
5. **TOUJOURS** documenter les endpoints API

## 📊 Modèle de Données Clé

- `organizations` → Multi-tenant root
- `users` → Avec rôles RBAC
- `campaigns` → Campagnes de prospection
- `leads` → Prospects avec score BANT
- `emails` → Queue d'approbation
- `meetings` → RDVs bookés

## 🤖 Les 3 Agents

1. **Prospector**: Recherche + enrichissement leads
2. **BANT Qualifier**: Score 0-100 (>60 = qualified)
3. **Scheduler**: Email personnalisé + Calendly

## 📁 Fichiers Importants

- `/docs/tech/` → Spécifications techniques
- `/docs/api/` → Contrats API OpenAPI
- `/backend/app/agents/` → Prompts des agents
- `/frontend/components/ui/` → Design System
```

---

## 2️⃣ SETTINGS.JSON - CONFIGURATION & HOOKS

```json
{
  "model": "claude-sonnet-4-20250514",
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(cd *)",
      "Bash(ls *)",
      "Bash(cat *)",
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(uv *)",
      "Bash(pytest *)",
      "Bash(alembic *)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(./secrets/**)",
      "Write(.env)",
      "Bash(rm -rf *)",
      "Bash(*password*)",
      "Bash(*secret*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "[ \"$(git branch --show-current)\" != \"main\" ] || { echo '{\"block\": true, \"message\": \"❌ Cannot edit on main branch. Create a feature branch first.\"}' >&2; exit 2; }",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write(*.py)|Edit(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "cd backend && uv run ruff format $CLAUDE_FILE && uv run ruff check --fix $CLAUDE_FILE",
            "timeout": 30
          }
        ]
      },
      {
        "matcher": "Write(*.ts)|Write(*.tsx)|Edit(*.ts)|Edit(*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "cd frontend && npx prettier --write $CLAUDE_FILE && npx eslint --fix $CLAUDE_FILE",
            "timeout": 30
          }
        ]
      },
      {
        "matcher": "Write(**/test_*.py)|Edit(**/test_*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "cd backend && uv run pytest $CLAUDE_FILE -v --tb=short",
            "timeout": 120
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "echo '🚀 Vectra Dev Session Started' && git status --short"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "filesystem": {
      "autoApprove": ["list_directory", "read_file"]
    }
  }
}
```

---

## 3️⃣ AGENTS - SUBAGENTS SPÉCIALISÉS

### `.claude/agents/architect.md`

```markdown
---
name: architect
description: System architecture decisions, design patterns, and technical planning. Use for high-level design discussions.
model: opus
tools: Read, Grep, Glob, Bash(git log *)
---

You are a senior software architect specializing in SaaS B2B applications.

## Your Expertise
- Distributed systems design
- Multi-tenant architecture
- API design (REST, GraphQL)
- Database modeling
- Event-driven architecture
- Security patterns

## When Consulted
1. Analyze the current architecture in `/docs/architecture/`
2. Consider scalability, maintainability, security
3. Reference ADRs in `/docs/decisions/`
4. Propose solutions with trade-offs
5. Create or update architecture diagrams

## Output Format
- Start with executive summary
- List options with pros/cons
- Recommend with justification
- Include implementation steps
```

### `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Reviews code for quality, security, performance, and maintainability. Use after implementing features.
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash
---

You are a senior code reviewer with expertise in Python and TypeScript.

## Review Checklist

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Authentication checks

### Quality
- [ ] Type hints/types complete
- [ ] Error handling appropriate
- [ ] Logging meaningful
- [ ] No code duplication
- [ ] Functions < 50 lines

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Async where needed
- [ ] Indexes considered

### Tests
- [ ] Tests exist for new code
- [ ] Edge cases covered
- [ ] Mocks appropriate

## Output Format
Return a structured review with:
1. Summary (APPROVED / CHANGES REQUESTED)
2. Critical issues (blockers)
3. Suggestions (improvements)
4. Praise (what's done well)
```

### `.claude/agents/tdd-guide.md`

```markdown
---
name: tdd-guide
description: Test-Driven Development workflow. Use when implementing new features to write tests first.
tools: Read, Write, Edit, Bash(pytest *)
---

You are a TDD expert. You ALWAYS write tests before implementation.

## TDD Cycle

### 1. RED - Write Failing Test
```python
def test_feature_does_something():
    # Arrange
    input_data = {...}
    
    # Act
    result = feature_function(input_data)
    
    # Assert
    assert result == expected_output
```

### 2. GREEN - Minimal Implementation
Write the minimum code to make the test pass.

### 3. REFACTOR - Improve Code
Clean up while keeping tests green.

## Vectra Test Patterns

### Backend (pytest)
```python
# tests/test_services/test_lead_service.py
import pytest
from app.services.lead_service import LeadService

@pytest.fixture
def lead_service(db_session):
    return LeadService(db_session)

async def test_qualify_lead_above_threshold(lead_service):
    lead = await lead_service.create(email="test@company.com")
    result = await lead_service.qualify(lead.id)
    assert result.bant_score >= 60
    assert result.status == "qualified"
```

### Frontend (Vitest)
```typescript
import { render, screen } from '@testing-library/react'
import { LeadCard } from './LeadCard'

describe('LeadCard', () => {
  it('displays BANT score badge', () => {
    render(<LeadCard lead={mockLead} />)
    expect(screen.getByText('75')).toBeInTheDocument()
  })
})
```
```

### `.claude/agents/api-designer.md`

```markdown
---
name: api-designer
description: Design and document REST APIs following OpenAPI spec. Use when creating new endpoints.
tools: Read, Write, Grep
skills: fastapi-backend
---

You are an API design expert specializing in RESTful APIs.

## API Design Principles

### URL Structure
- Plural nouns: `/campaigns`, `/leads`
- Nested resources: `/campaigns/{id}/leads`
- Actions as sub-resources: `/campaigns/{id}/launch`

### HTTP Methods
- GET: Read (idempotent)
- POST: Create
- PUT: Full update
- PATCH: Partial update
- DELETE: Remove

### Response Format
```json
{
  "data": {...},
  "meta": {
    "page": 1,
    "total": 100
  }
}
```

### Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [...]
  }
}
```

### Status Codes
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity
- 500: Server Error

## Output
Generate:
1. OpenAPI 3.1 spec
2. FastAPI router code
3. Pydantic schemas
4. Example requests/responses
```

---

## 4️⃣ SKILLS - CONNAISSANCES PROCÉDURALES

### `.claude/skills/vectra-patterns/SKILL.md`

```markdown
---
name: vectra-patterns
description: Vectra-specific coding patterns, conventions, and best practices. Auto-activates when working on Vectra codebase.
---

# Vectra Development Patterns

## Multi-Tenant Pattern

Every query MUST filter by `organization_id`:

```python
# ✅ Correct
async def get_campaigns(org_id: UUID, db: AsyncSession):
    stmt = select(Campaign).where(Campaign.organization_id == org_id)
    return await db.scalars(stmt)

# ❌ Wrong - Missing org filter
async def get_campaigns(db: AsyncSession):
    return await db.scalars(select(Campaign))
```

## Service Layer Pattern

```python
# app/services/campaign_service.py
class CampaignService:
    def __init__(self, db: AsyncSession, org_id: UUID):
        self.db = db
        self.org_id = org_id
    
    async def create(self, data: CampaignCreate) -> Campaign:
        campaign = Campaign(
            organization_id=self.org_id,
            **data.model_dump()
        )
        self.db.add(campaign)
        await self.db.commit()
        return campaign
```

## API Endpoint Pattern

```python
# app/api/v1/campaigns.py
@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CampaignService(db, current_user.organization_id)
    return await service.create(data)
```

## React Component Pattern

```typescript
// components/features/campaigns/CampaignCard.tsx
interface CampaignCardProps {
  campaign: Campaign
  onSelect?: (id: string) => void
}

export function CampaignCard({ campaign, onSelect }: CampaignCardProps) {
  return (
    <Card className="p-4 hover:shadow-md transition-shadow">
      <CardHeader>
        <CardTitle>{campaign.name}</CardTitle>
        <Badge variant={getStatusVariant(campaign.status)}>
          {campaign.status}
        </Badge>
      </CardHeader>
      <CardContent>
        {/* ... */}
      </CardContent>
    </Card>
  )
}
```

## Error Handling Pattern

```python
from app.core.exceptions import VectraException

class LeadNotFoundError(VectraException):
    code = "LEAD_NOT_FOUND"
    status_code = 404

# In service
async def get_lead(self, lead_id: UUID) -> Lead:
    lead = await self.db.get(Lead, lead_id)
    if not lead or lead.organization_id != self.org_id:
        raise LeadNotFoundError(f"Lead {lead_id} not found")
    return lead
```

## References
- See `references/api-patterns.md` for more API examples
- See `references/agent-patterns.md` for CrewAI patterns
```

### `.claude/skills/fastapi-backend/SKILL.md`

```markdown
---
name: fastapi-backend
description: FastAPI patterns, async SQLAlchemy, Pydantic v2, and backend best practices for Vectra.
---

# FastAPI Backend Patterns

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── core/
│   │   ├── config.py        # Settings
│   │   ├── security.py      # Auth
│   │   └── exceptions.py    # Custom errors
│   ├── api/
│   │   ├── deps.py          # Dependencies
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── campaigns.py
│   │       └── leads.py
│   ├── models/              # SQLAlchemy
│   ├── schemas/             # Pydantic
│   └── services/            # Business logic
└── tests/
```

## Dependency Injection

```python
# app/api/deps.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    # Validate JWT, return user
    ...
```

## Pydantic v2 Schemas

```python
# app/schemas/campaign.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class CampaignBase(BaseModel):
    name: str
    target_criteria: dict

class CampaignCreate(CampaignBase):
    pass

class CampaignResponse(CampaignBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: str
    created_at: datetime
```

## Async SQLAlchemy 2.0

```python
# app/models/campaign.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Campaign(Base):
    __tablename__ = "campaigns"
    
    name: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"))
    
    organization: Mapped["Organization"] = relationship(back_populates="campaigns")
    leads: Mapped[list["Lead"]] = relationship(back_populates="campaign")
```

## Background Tasks with Celery

```python
# app/tasks/campaign_tasks.py
from celery import shared_task

@shared_task
def run_prospector(campaign_id: str):
    # Long-running task
    ...
```
```

### `.claude/skills/nextjs-frontend/SKILL.md`

```markdown
---
name: nextjs-frontend
description: Next.js 14 App Router, React Server Components, Tailwind, and Shadcn/ui patterns.
---

# Next.js Frontend Patterns

## App Router Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx       # Dashboard layout
│   │   ├── page.tsx         # Dashboard home
│   │   ├── campaigns/
│   │   └── leads/
│   └── api/                 # API routes (if needed)
├── components/
│   ├── ui/                  # Shadcn components
│   └── features/            # Domain components
└── lib/
    ├── api.ts               # API client
    └── utils.ts
```

## Server vs Client Components

```typescript
// Server Component (default) - app/campaigns/page.tsx
import { getCampaigns } from '@/lib/api'

export default async function CampaignsPage() {
  const campaigns = await getCampaigns()
  return <CampaignList campaigns={campaigns} />
}

// Client Component - components/CampaignList.tsx
'use client'

import { useState } from 'react'

export function CampaignList({ campaigns }: Props) {
  const [selected, setSelected] = useState<string | null>(null)
  // ...
}
```

## Data Fetching with React Query

```typescript
// lib/hooks/useCampaigns.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useCampaigns() {
  return useQuery({
    queryKey: ['campaigns'],
    queryFn: () => api.get('/campaigns'),
  })
}

export function useCreateCampaign() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CampaignCreate) => api.post('/campaigns', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] })
    },
  })
}
```

## Shadcn/ui Components

```typescript
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

// Use Tailwind classes, not custom CSS
<Card className="p-4 hover:shadow-lg transition-shadow">
  <CardHeader className="flex flex-row items-center justify-between">
    <CardTitle className="text-lg font-semibold">{title}</CardTitle>
    <Badge variant="secondary">{status}</Badge>
  </CardHeader>
</Card>
```

## Form Handling with React Hook Form + Zod

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Required'),
  email: z.string().email('Invalid email'),
})

export function CampaignForm() {
  const form = useForm({
    resolver: zodResolver(schema),
  })
  
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* ... */}
      </form>
    </Form>
  )
}
```
```

### `.claude/skills/crewai-agents/SKILL.md`

```markdown
---
name: crewai-agents
description: CrewAI multi-agent patterns for Vectra's prospection, qualification, and scheduling agents.
---

# CrewAI Agent Patterns

## Agent Structure

```python
# app/agents/prospector.py
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

class ProspectorAgent:
    def __init__(self):
        self.llm = Ollama(model="llama2:70b")
        
        self.agent = Agent(
            role="Lead Prospector",
            goal="Find and enrich qualified B2B prospects",
            backstory="""You are an expert B2B sales researcher. 
            You find decision-makers at companies matching specific criteria.""",
            llm=self.llm,
            tools=[
                RocketReachTool(),
                LinkedInTool(),
                CompanyEnrichmentTool(),
            ],
            verbose=True,
        )
    
    async def find_prospects(self, criteria: dict) -> list[dict]:
        task = Task(
            description=f"""
            Find {criteria['limit']} prospects matching:
            - Job titles: {criteria['job_titles']}
            - Company size: {criteria['company_size']}
            - Geography: {criteria['geography']}
            - Industry: {criteria['industry']}
            
            For each prospect, collect:
            - Full name
            - Email (verified)
            - Job title
            - Company name
            - LinkedIn URL
            """,
            agent=self.agent,
            expected_output="JSON array of prospect objects"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = await crew.kickoff_async()
        return self._parse_result(result)
```

## BANT Scorer

```python
# app/agents/bant.py
class BANTAgent:
    def __init__(self):
        self.agent = Agent(
            role="BANT Qualifier",
            goal="Score leads using BANT framework (0-100)",
            backstory="""You qualify B2B leads by analyzing:
            - Budget: Company size, funding, revenue indicators
            - Authority: Job title, decision-making level
            - Need: Growth signals, pain points, job postings
            - Timeline: Recent activity, urgency indicators""",
            llm=self.llm,
        )
    
    async def score_lead(self, lead: dict) -> dict:
        task = Task(
            description=f"""
            Analyze this prospect and provide BANT score:
            
            Name: {lead['name']}
            Title: {lead['job_title']}
            Company: {lead['company_name']}
            Size: {lead['company_size']}
            
            Score each dimension 0-25:
            - Budget (0-25): Based on company size and funding
            - Authority (0-25): Based on job title
            - Need (0-25): Based on company signals
            - Timeline (0-25): Based on recent activity
            
            Return JSON with scores and reasoning.
            """,
            agent=self.agent,
            expected_output="JSON with budget, authority, need, timeline scores"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = await crew.kickoff_async()
        return self._parse_score(result)
```

## Multi-Agent Orchestration

```python
# app/agents/orchestrator.py
from celery import chain

class CampaignOrchestrator:
    def __init__(self):
        self.prospector = ProspectorAgent()
        self.qualifier = BANTAgent()
        self.scheduler = SchedulerAgent()
    
    async def run_campaign(self, campaign_id: UUID):
        # Pipeline: Prospect → Qualify → Schedule
        campaign = await self.get_campaign(campaign_id)
        
        # Step 1: Find prospects
        prospects = await self.prospector.find_prospects(
            campaign.target_criteria
        )
        
        # Step 2: Qualify each
        qualified = []
        for prospect in prospects:
            score = await self.qualifier.score_lead(prospect)
            if score['total'] >= campaign.bant_threshold:
                qualified.append({**prospect, 'bant_score': score})
        
        # Step 3: Schedule outreach
        for lead in qualified:
            await self.scheduler.create_email(lead, campaign)
        
        return qualified
```

## References
- See `examples/prospector_example.py`
- See `examples/bant_example.py`
```

---

## 5️⃣ COMMANDS - SLASH COMMANDS

### `.claude/commands/implement.md`

```markdown
---
description: Implement a feature following TDD. Creates branch, writes tests first, then code.
allowed-tools: Read, Write, Edit, Bash, Task
---

# Implement Feature: $ARGUMENTS

## Instructions

1. **Create feature branch**
   ```bash
   git checkout -b feature/$ARGUMENTS
   ```

2. **Read relevant docs**
   - Check `/docs/` for specifications
   - Review existing patterns in codebase

3. **Write tests FIRST** (TDD)
   - Create test file
   - Write failing tests
   - Run tests to confirm they fail

4. **Implement minimum code**
   - Make tests pass
   - Follow patterns in `vectra-patterns` skill

5. **Refactor**
   - Clean up code
   - Ensure all tests pass

6. **Update documentation**
   - Add API docs if endpoint
   - Update CHANGELOG

7. **Commit with message**
   ```bash
   git add .
   git commit -m "feat: $ARGUMENTS"
   ```
```

### `.claude/commands/review.md`

```markdown
---
description: Code review for recent changes. Spawns code-reviewer subagent.
allowed-tools: Task, Read, Grep
---

# Code Review

## Instructions

1. Get list of changed files:
   ```bash
   git diff --name-only HEAD~1
   ```

2. Spawn code-reviewer subagent to review each file:
   - Use Task tool with subagent_type='code-reviewer'

3. Compile review results

4. Output structured review with:
   - Summary (APPROVED / CHANGES REQUESTED)
   - Critical issues
   - Suggestions
   - Praise
```

### `.claude/commands/research.md`

```markdown
---
description: Research a topic using parallel subagents for documentation, codebase, and web search.
allowed-tools: Task, WebSearch, WebFetch, Read, Grep, Glob, Write
---

# Research: $ARGUMENTS

## Instructions

Launch 3 parallel subagents:

### 1. Documentation Agent
- Search official docs for $ARGUMENTS
- Find best practices
- Locate GitHub issues

### 2. Codebase Agent (subagent_type: Explore)
- Search codebase for related patterns
- Find existing solutions
- Identify relevant files

### 3. Web Research Agent
- Search for recent articles
- Find Stack Overflow solutions
- Check for known issues

## Output

Create `docs/research/$(date +%Y-%m-%d)-$ARGUMENTS.md` with:
- Problem Statement
- Key Findings
- Codebase Patterns
- Recommended Approach
- Sources
```

### `.claude/commands/create-endpoint.md`

```markdown
---
description: Create a new API endpoint with router, schema, service, and tests.
allowed-tools: Read, Write, Edit
skills: fastapi-backend, vectra-patterns
---

# Create Endpoint: $ARGUMENTS

## Files to Create

1. **Schema** (`backend/app/schemas/$ARGUMENTS.py`)
   - Base, Create, Update, Response classes
   - Pydantic v2 with ConfigDict

2. **Service** (`backend/app/services/${ARGUMENTS}_service.py`)
   - CRUD operations
   - Business logic
   - Multi-tenant filtering

3. **Router** (`backend/app/api/v1/$ARGUMENTS.py`)
   - CRUD endpoints
   - Dependencies injection
   - OpenAPI documentation

4. **Tests** (`backend/tests/test_api/test_$ARGUMENTS.py`)
   - Test all endpoints
   - Test auth/permissions
   - Test edge cases

5. **Register router** in `backend/app/api/v1/__init__.py`

## Follow TDD
Write tests first, then implement.
```

---

## 6️⃣ MCP.JSON - SERVEURS MCP

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "autoApprove": ["list_directory", "read_file"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  },
  "disabledMcpServers": []
}
```

> ⚠️ **Important**: Ne pas activer trop de MCP servers à la fois. Le context window de 200k peut descendre à 70k avec trop d'outils.

---

## 7️⃣ WORKFLOW RECOMMANDÉ

### Démarrer une Session

```bash
# 1. Ouvrir le projet
cd vectra
claude

# 2. Claude lit automatiquement CLAUDE.md

# 3. Vérifier le contexte
/context

# 4. Commencer à travailler
/implement create-lead-export-feature
```

### Utiliser les Subagents

```
# Demander une review
Claude, spawn the code-reviewer agent to review the changes in app/services/

# Recherche parallèle
/research CrewAI error handling patterns

# Architecture decision
Claude, consult the architect agent about adding caching layer
```

### Commandes Utiles

| Commande | Description |
|----------|-------------|
| `/implement <feature>` | Implémenter une feature (TDD) |
| `/review` | Code review |
| `/test <scope>` | Lancer les tests |
| `/research <topic>` | Recherche parallèle |
| `/create-endpoint <name>` | Créer un endpoint API |
| `/create-component <name>` | Créer un composant React |
| `/compact` | Compresser le contexte |
| `/context` | Voir l'utilisation du contexte |

---

## 📋 CHECKLIST D'INSTALLATION

```bash
# 1. Créer la structure
mkdir -p .claude/{agents,skills,commands,hooks}

# 2. Copier les fichiers
# - CLAUDE.md à la racine
# - settings.json dans .claude/
# - Agents dans .claude/agents/
# - Skills dans .claude/skills/
# - Commands dans .claude/commands/
# - .mcp.json à la racine

# 3. Configurer git
echo ".claude/settings.local.json" >> .gitignore

# 4. Tester
claude
/context
```

---

## 🎯 RÉSUMÉ QUICK START

| Concept | Quoi | Où |
|---------|------|-----|
| **CLAUDE.md** | Mémoire projet | `/CLAUDE.md` |
| **Settings** | Config + Hooks | `.claude/settings.json` |
| **Agents** | Subagents spécialisés | `.claude/agents/*.md` |
| **Skills** | Connaissances procédurales | `.claude/skills/*/SKILL.md` |
| **Commands** | Slash commands | `.claude/commands/*.md` |
| **MCP** | Connexions externes | `.mcp.json` |

---

*Architecture optimisée pour Claude Code 2.1+ | Janvier 2026*
