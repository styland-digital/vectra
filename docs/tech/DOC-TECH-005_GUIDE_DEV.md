# VECTRA - GUIDE DÉVELOPPEUR

## Developer Handbook

### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-005  
**Statut:** APPROUVÉ  
**Objectif:** Onboarding rapide des développeurs et standardisation des pratiques  

---

## TABLE DES MATIERES

1. Setup Environnement Local
2. Structure du Projet
3. Conventions de Code
4. Git Workflow
5. Tests
6. CI/CD Pipeline
7. Déploiement
8. Debugging
9. Comment Ajouter un Agent
10. FAQ Développeurs

---

## 1. SETUP ENVIRONNEMENT LOCAL

### 1.1 Prérequis

| Outil | Version | Installation |
|-------|---------|--------------|
| Python | 3.11+ | `pyenv install 3.11` |
| Node.js | 20+ | `nvm install 20` |
| Docker | 24+ | docker.com |
| PostgreSQL | 15+ | Via Docker |
| Redis | 7+ | Via Docker |

### 1.2 Clone et Setup

```bash
# Clone
git clone git@github.com:vectra-ai/vectra.git
cd vectra

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Frontend
cd ../frontend
npm install

# Environment
cp .env.example .env
```

### 1.3 Variables d'Environnement Backend

```bash
DATABASE_URL=postgresql://vectra:vectra@localhost:5432/vectra
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-secret-key
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=https://api.ollama.com
ROCKETREACH_API_KEY=
SENDGRID_API_KEY=
ENVIRONMENT=development
DEBUG=true
```

### 1.4 Démarrer les Services

```bash
# Terminal 1: DB + Redis
docker-compose up -d postgres redis

# Terminal 2: Backend
uvicorn app.main:app --reload --port 8000

# Terminal 3: Celery
celery -A app.worker worker --loglevel=INFO

# Terminal 4: Frontend
npm run dev

# Terminal 5: Ollama
ollama serve
```

---

## 2. STRUCTURE DU PROJET

```
vectra/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Routes API
│   │   ├── agents/          # Agents IA
│   │   ├── core/            # Config, security
│   │   ├── db/models/       # SQLAlchemy models
│   │   ├── services/        # Business logic
│   │   ├── tasks/           # Celery tasks
│   │   └── schemas/         # Pydantic
│   ├── tests/
│   ├── alembic/
│   └── requirements.txt
├── frontend/
│   ├── app/                 # Next.js App Router
│   ├── components/
│   ├── lib/
│   └── package.json
└── docker-compose.yml
```

---

## 3. CONVENTIONS DE CODE

### Python

- PEP 8 + Black (line 88)
- Type hints obligatoires
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE

### TypeScript

- ESLint + Prettier
- Components: PascalCase
- Functions: camelCase
- Strict mode

### SQL

- Tables: snake_case, plural
- Columns: snake_case
- Index: idx_{table}_{columns}

---

## 4. GIT WORKFLOW

### Branches

```
main ← production
  └── develop ← integration
        ├── feature/VECTRA-123-description
        ├── bugfix/VECTRA-456-description
        └── hotfix/VECTRA-789-description
```

### Commits

```
feat(agents): add BANT scoring logic

Description détaillée...

Closes VECTRA-123
```

Types: feat, fix, docs, style, refactor, test, chore

### Pull Requests

- 1 approval minimum
- Tests passent
- Linting OK
- Documentation à jour

---

## 5. TESTS

### Structure

```
tests/
├── unit/           # Tests unitaires
├── integration/    # Tests API
└── e2e/           # Tests Playwright
```

### Commandes

```bash
# Backend
pytest                    # Tous
pytest --cov=app         # Avec coverage
pytest -k "test_bant"    # Filtrer

# Frontend
npm run test             # Jest
npm run test:e2e         # Playwright
```

### Coverage Cibles

- Services: 90%
- Agents: 85%
- API Routes: 80%
- Components: 70%

---

## 6. CI/CD PIPELINE

### GitHub Actions

- Push sur develop → Deploy staging
- Push sur main → Deploy production

### Checks

1. Lint (black, ruff, eslint)
2. Type check (mypy, tsc)
3. Tests (pytest, jest)
4. Build
5. Deploy

---

## 7. DÉPLOIEMENT

| Env | URL | Branch | Deploy |
|-----|-----|--------|--------|
| Dev | localhost | - | Manual |
| Staging | staging.vectra.io | develop | Auto |
| Prod | app.vectra.io | main | Auto |

### Rollback

```bash
git revert <commit>
git push origin main
```

---

## 8. DEBUGGING

### Logs

```bash
docker-compose logs -f backend
celery -A app.worker inspect active
```

### Database

```bash
docker exec -it vectra-postgres psql -U vectra
```

### Celery

```bash
celery -A app.worker flower  # http://localhost:5555
```

---

## 9. COMMENT AJOUTER UN AGENT

### 1. Créer l'agent

```python
# app/agents/new_agent/agent.py
from crewai import Agent, Task
from app.agents.base import BaseVectraAgent

class NewAgent(BaseVectraAgent):
    def __init__(self, config):
        super().__init__(config)
        self.agent = Agent(
            role="...",
            goal="...",
            backstory="...",
            tools=[...],
            llm=self.llm
        )
    
    async def execute(self, input_data: dict) -> AgentResult:
        task = Task(
            description=self._build_prompt(input_data),
            agent=self.agent
        )
        result = await self._execute_task(task)
        return self._parse_result(result)
```

### 2. Enregistrer

```python
# app/agents/__init__.py
AGENTS = {
    "new_agent": NewAgent,
}
```

### 3. Créer la task Celery

```python
# app/tasks/new_agent_tasks.py
@shared_task(bind=True, max_retries=3)
def run_new_agent(self, job_id, input_data):
    agent = AGENTS["new_agent"](config)
    return agent.execute(input_data)
```

### 4. Ajouter les tests

```python
# tests/unit/agents/test_new_agent.py
class TestNewAgent:
    async def test_execute_success(self, agent):
        result = await agent.execute({"key": "value"})
        assert result.success == True
```

---

## 10. FAQ DÉVELOPPEURS

**Q: Comment régénérer les migrations?**

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

**Q: Comment vider la DB locale?**

```bash
docker-compose down -v
docker-compose up -d postgres redis
alembic upgrade head
python -m app.scripts.seed_database
```

**Q: Comment tester les webhooks localement?**

```bash
ngrok http 8000
# Utiliser l'URL ngrok comme endpoint
```

**Q: Comment forcer un redéploiement?**

```bash
git commit --allow-empty -m "chore: trigger deploy"
git push origin develop
```

---

## COMMANDES UTILES

### Backend

```bash
uvicorn app.main:app --reload --port 8000
celery -A app.worker worker --loglevel=INFO
alembic upgrade head
pytest --cov=app
black . && ruff check .
```

### Frontend

```bash
npm run dev
npm run build
npm run test
npm run lint
```

### Docker

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down -v
```

---

**- FIN DU DOCUMENT -**

*14 Janvier 2026*
