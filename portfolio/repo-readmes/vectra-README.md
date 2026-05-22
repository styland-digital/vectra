# Vectra — AI Sales Agents Platform

> SaaS platform with 3 AI agents (CrewAI + Llama 2) that automate the entire B2B sales pipeline: prospect discovery → BANT qualification → personalized outreach → meeting scheduling.

[![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js_14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

---

## Overview

Vectra automates B2B outbound sales by deploying three specialized AI agents that work in sequence. Instead of spending hours on manual prospecting and email writing, sales teams define their ICP (Ideal Customer Profile) once — and Vectra handles everything from finding prospects to scheduling meetings.

Built as a multi-tenant SaaS with strict organization-level data isolation.

---

## The 3 AI Agents

```
┌─────────────────────────────────────────────────────────────┐
│                        VECTRA PIPELINE                       │
├─────────────┬───────────────────┬───────────────────────────┤
│  PROSPECTOR │       BANT        │        SCHEDULER          │
│             │                   │                           │
│ Finds leads │ Qualifies leads   │ Writes emails + books     │
│ via         │ Score: 0-100      │ meetings via Calendly     │
│ RocketReach │ ≥60 → qualified   │                           │
│ API         │ 40-59 → nurture   │                           │
│             │ <40 → rejected    │                           │
└─────────────┴───────────────────┴───────────────────────────┘
```

**BANT Scoring:** Budget (0-25) + Authority (0-25) + Need (0-25) + Timeline (0-25)

---

## Key Features

- **Multi-tenant SaaS** — Strict data isolation per organization
- **Role-based access** — Owner / Admin / Manager / Operator / Viewer
- **Campaign management** — Create, configure, and monitor outreach campaigns
- **Real-time job tracking** — Live status updates for agent processing jobs
- **Email automation** — Personalized emails via SendGrid with rate limiting
- **Meeting scheduling** — Calendly integration for automated booking
- **Audit logs** — Immutable history of all actions
- **REST API** — Fully documented OpenAPI spec

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.11 + FastAPI |
| AI Agents | CrewAI + Llama 2 70B |
| Frontend | Next.js 14 + React 18 + Shadcn/ui |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy + Alembic |
| Queue | Redis 7 + Celery 5.3 |
| Container | Docker + Docker Compose |
| Auth | JWT (15min access + 7d refresh) |

---

## Architecture

```
vectra/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── auth/       # Public auth endpoints
│   │   │   ├── user/       # Multi-tenant user endpoints
│   │   │   └── admin/      # Platform admin endpoints
│   │   ├── agents/
│   │   │   ├── prospector/ # Lead discovery agent
│   │   │   ├── bant/       # Qualification agent
│   │   │   └── scheduler/  # Email/meeting agent
│   │   ├── db/             # SQLAlchemy models + repositories
│   │   ├── services/       # Business logic
│   │   └── tasks/          # Celery async tasks
│   └── tests/
├── frontend/
│   ├── app/                # Next.js App Router
│   ├── components/         # React + Shadcn/ui
│   └── lib/                # API client, utils
└── docs/                   # Architecture docs, API contracts
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose

### Quick Start

```bash
git clone https://github.com/styland-digital/vectra.git
cd vectra

# Start all services (DB, Redis, API, Frontend)
make install
make docker-up
make migrate
make dev
```

Services:
- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Environment Variables

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env.local
```

---

## API Routes

| Prefix | Description | Auth |
|--------|-------------|------|
| `POST /api/v1/auth/login` | User login | Public |
| `POST /api/v1/auth/register` | Registration | Public |
| `GET /api/v1/user/campaigns` | List campaigns | JWT + org isolation |
| `POST /api/v1/user/campaigns` | Create campaign | JWT + org isolation |
| `GET /api/v1/admin/overview` | Platform stats | Platform Admin only |

Full API documentation: [`docs/tech/DOC-TECH-002_API_CONTRACTS.md`](docs/tech/DOC-TECH-002_API_CONTRACTS.md)

---

## Testing

```bash
# All tests
make test

# Backend with coverage
cd backend && pytest --cov=app

# Frontend
cd frontend && npm run test
```

---

## Author

**Alfred Landry Talom** — Full Stack Developer & Product Designer

[![Dribbble](https://img.shields.io/badge/Dribbble-EA4C89?style=flat-square&logo=dribbble&logoColor=white)](https://dribbble.com/TFAL237)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:alfredlandrytalom2004@gmail.com)

---

## License

[MIT](LICENSE) © 2026 Alfred Landry Talom
