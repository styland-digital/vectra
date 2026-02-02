# VECTRA - COMMANDES CLAUDE CODE
## Fichiers pour .claude/commands/
### 14 Janvier 2026

---

Ce document contient le contenu de chaque fichier de commande à placer dans `.claude/commands/`.

---

## 1. create-agent.md

```markdown
# Créer un Nouvel Agent IA

## Usage
```
/create-agent <nom_agent>
```

## Ce que cette commande fait

1. Crée la structure de fichiers dans `backend/app/agents/<nom>/`
2. Génère le squelette de l'agent avec CrewAI
3. Crée le fichier de prompts
4. Crée les tests unitaires
5. Enregistre l'agent dans `__init__.py`

## Structure créée

```
backend/app/agents/<nom>/
├── __init__.py
├── agent.py      # Logique principale
├── prompts.py    # Prompts LLM
└── tools.py      # Outils si nécessaire
```

## Template agent.py

```python
from crewai import Agent, Task
from app.agents.base import BaseVectraAgent
from app.agents.<nom>.prompts import MAIN_PROMPT

class <Nom>Agent(BaseVectraAgent):
    """
    Agent <Nom>: <description>
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        self.agent = Agent(
            role="<role>",
            goal="<goal>",
            backstory="<backstory>",
            tools=self._get_tools(),
            llm=self.llm
        )
    
    def _get_tools(self):
        return []
    
    async def execute(self, input_data: dict) -> dict:
        task = Task(
            description=MAIN_PROMPT.format(**input_data),
            agent=self.agent,
            expected_output="JSON with results"
        )
        result = await self._execute_task(task)
        return self._parse_result(result)
    
    def _parse_result(self, raw: str) -> dict:
        # Parse logic
        return {}
```

## Checklist après création

- [ ] Définir les prompts dans prompts.py
- [ ] Implémenter la logique dans agent.py
- [ ] Ajouter les tests dans tests/unit/agents/
- [ ] Créer la task Celery si async
- [ ] Mettre à jour la documentation
```

---

## 2. create-endpoint.md

```markdown
# Créer un Endpoint API

## Usage
```
/create-endpoint <resource> <method>
```

Exemples:
- `/create-endpoint campaigns GET`
- `/create-endpoint leads POST`

## Ce que cette commande fait

1. Crée ou met à jour le fichier route dans `backend/app/api/v1/`
2. Crée le schema Pydantic si nécessaire
3. Crée/met à jour le service
4. Crée les tests d'intégration
5. Met à jour le router principal

## Pattern à suivre

### Route (api/v1/<resource>.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.schemas.<resource> import <Resource>Create, <Resource>Response
from app.services.<resource> import <Resource>Service
from app.db.models import User

router = APIRouter(prefix="/<resources>", tags=["<resources>"])

@router.get("", response_model=list[<Resource>Response])
async def list_<resources>(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
):
    """List all <resources> for the current organization."""
    service = <Resource>Service(db)
    return await service.list(
        organization_id=current_user.organization_id,
        skip=skip,
        limit=limit
    )

@router.post("", response_model=<Resource>Response, status_code=status.HTTP_201_CREATED)
async def create_<resource>(
    data: <Resource>Create,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new <resource>."""
    service = <Resource>Service(db)
    return await service.create(
        organization_id=current_user.organization_id,
        created_by=current_user.id,
        **data.model_dump()
    )

@router.get("/{id}", response_model=<Resource>Response)
async def get_<resource>(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a <resource> by ID."""
    service = <Resource>Service(db)
    result = await service.get(id, organization_id=current_user.organization_id)
    if not result:
        raise HTTPException(status_code=404, detail="<Resource> not found")
    return result
```

### Schema (schemas/<resource>.py)

```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class <Resource>Base(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    # autres champs

class <Resource>Create(<Resource>Base):
    pass

class <Resource>Update(BaseModel):
    name: Optional[str] = None
    # autres champs optionnels

class <Resource>Response(<Resource>Base):
    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

## Checklist

- [ ] Route créée avec tous les CRUD nécessaires
- [ ] Schema Pydantic avec validation
- [ ] Service avec logique métier
- [ ] Tests d'intégration
- [ ] Mis à jour dans router.py
- [ ] Documentation OpenAPI correcte
```

---

## 3. create-migration.md

```markdown
# Créer une Migration de Base de Données

## Usage
```
/create-migration "<description>"
```

Exemple:
- `/create-migration "add email tracking fields"`

## Ce que cette commande fait

1. Génère une migration Alembic avec autogenerate
2. Review et ajuste le fichier généré
3. Propose les index nécessaires
4. Vérifie la cohérence avec le schema existant

## Commandes exécutées

```bash
cd backend
alembic revision --autogenerate -m "<description>"
```

## Vérifications automatiques

1. **Colonnes NOT NULL** - S'assurer qu'il y a un DEFAULT ou que la table est vide
2. **Foreign Keys** - Vérifier que les tables référencées existent
3. **Index** - Proposer les index pour les FK et colonnes fréquemment filtrées
4. **ENUMs** - Créer le type ENUM avant la colonne

## Template de migration

```python
"""<description>

Revision ID: xxx
Revises: yyy
Create Date: 2026-01-14

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'xxx'
down_revision = 'yyy'
branch_labels = None
depends_on = None

def upgrade():
    # Créer ENUM si nécessaire
    # op.execute("CREATE TYPE status_enum AS ENUM ('a', 'b', 'c')")
    
    # Ajouter colonne
    op.add_column('table_name', sa.Column(
        'new_column',
        sa.String(255),
        nullable=True
    ))
    
    # Créer index
    op.create_index('idx_table_new_column', 'table_name', ['new_column'])

def downgrade():
    op.drop_index('idx_table_new_column', 'table_name')
    op.drop_column('table_name', 'new_column')
    # op.execute("DROP TYPE status_enum")
```

## Checklist avant apply

- [ ] Le fichier de migration est correct
- [ ] Les données existantes ne seront pas perdues
- [ ] Les index sont créés pour les colonnes filtrées
- [ ] downgrade() fonctionne
- [ ] Testé sur une copie de la DB
```

---

## 4. write-test.md

```markdown
# Écrire des Tests

## Usage
```
/write-test <type> <target>
```

## Types de Tests Disponibles

| Type | Description | Cible | Framework |
|------|-------------|-------|-----------|
| `unit-service` | Test unitaire service backend | `app/services/<nom>.py` | pytest |
| `unit-agent` | Test unitaire agent IA | `app/agents/<nom>/agent.py` | pytest |
| `unit-utils` | Test unitaire utilitaire | `app/utils/<nom>.py` | pytest |
| `integration-api` | Test intégration API | `app/api/v1/<nom>.py` | pytest + httpx |
| `integration-db` | Test intégration base de données | `app/db/repositories/<nom>.py` | pytest + SQLAlchemy |
| `e2e` | Test end-to-end | Parcours utilisateur | Playwright |
| `component` | Test composant React | `components/<nom>.tsx` | Jest + React Testing Library |

Voir `.claude/commands/write-test.md` pour la documentation complète.
```

---

## 5. run-tests.md

```markdown
# Lancer les Tests

## Usage
```
/run-tests [scope]
```

Scopes disponibles:
- `all` - Tous les tests
- `unit` - Tests unitaires backend
- `integration` - Tests d'intégration API
- `e2e` - Tests end-to-end Playwright
- `frontend` - Tests frontend Jest
- `<fichier>` - Tests d'un fichier spécifique

## Commandes selon le scope

### All
```bash
cd backend && pytest --cov=app --cov-fail-under=80
cd frontend && npm run test
```

### Unit
```bash
cd backend && pytest tests/unit -v
```

### Integration
```bash
cd backend && pytest tests/integration -v
```

### E2E
```bash
cd frontend && npm run test:e2e
```

### Fichier spécifique
```bash
cd backend && pytest tests/unit/services/test_bant_service.py -v
```

## Interprétation des résultats

### Coverage minimum requis

| Couche | Minimum |
|--------|---------|
| Services | 80% |
| Agents | 75% |
| API | 70% |
| Frontend | 60% |

### Actions si échec

1. Lire le message d'erreur
2. Identifier le test qui échoue
3. Vérifier si c'est le test ou le code qui est faux
4. Fixer et relancer
```

---

## 6. deploy.md

```markdown
# Déployer

## Usage
```
/deploy <environment>
```

Environments:
- `staging` - Déployer sur staging
- `production` - Déployer sur production (⚠️ confirmation requise)

## Pré-requis

- [ ] Tous les tests passent
- [ ] Pas de changements non commités
- [ ] PR mergée dans la bonne branche

## Process Staging

```bash
git checkout develop
git pull origin develop
# Le déploiement est automatique via GitHub Actions
```

## Process Production

```bash
# 1. Créer une PR develop → main
# 2. Review et approval
# 3. Merge

# Le déploiement est automatique via GitHub Actions
```

## Vérifications post-déploiement

1. [ ] Health check OK: `curl https://api.vectra.io/health`
2. [ ] Pas d'erreurs dans les logs (5 min)
3. [ ] Métriques stables dans Grafana
4. [ ] Test smoke manuel des fonctions critiques

## Rollback si problème

```bash
# Via Render Dashboard
# Service > Deploys > Sélectionner version précédente > Rollback

# Ou via Git
git revert HEAD
git push origin main
```
```

---

## 7. debug.md

```markdown
# Aide au Debugging

## Usage
```
/debug <type>
```

Types:
- `api` - Problème API/Backend
- `db` - Problème base de données
- `agent` - Problème agent IA
- `celery` - Problème queue/workers
- `frontend` - Problème UI

## Debug API

### Vérifier les logs
```bash
# Local
docker-compose logs -f backend

# Production
# Render Dashboard > Service > Logs
```

### Tester un endpoint
```bash
# Obtenir un token
TOKEN=$(curl -s -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@vectra-demo.com","password":"demo123"}' \
  | jq -r '.data.access_token')

# Appeler l'endpoint
curl -X GET http://localhost:8000/v1/campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq
```

## Debug Database

### Connexion
```bash
docker exec -it vectra-postgres psql -U vectra
```

### Requêtes utiles
```sql
-- Voir les connexions actives
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Requêtes lentes
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity WHERE state != 'idle'
ORDER BY duration DESC LIMIT 10;

-- Taille des tables
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

## Debug Agent

### Logs agent
```bash
grep "agent" logs/app.log | tail -100
```

### Tester un agent manuellement
```python
# Dans un shell Python
from app.agents.bant import BANTAgent

agent = BANTAgent()
result = await agent.execute({
    "lead": {"job_title": "VP Sales", "company_size": "100-500"}
})
print(result)
```

## Debug Celery

### Voir les workers
```bash
celery -A app.tasks.celery_app inspect active
```

### Voir la queue
```bash
celery -A app.tasks.celery_app inspect reserved
redis-cli LLEN celery
```

### Flower dashboard
```bash
celery -A app.tasks.celery_app flower
# Ouvrir http://localhost:5555
```

## Debug Frontend

### Console browser
F12 > Console > Chercher les erreurs rouges

### Network
F12 > Network > Vérifier les requêtes API qui échouent

### React DevTools
Installer l'extension et inspecter les composants/state
```

---

## INSTALLATION

Pour installer ces commandes dans Claude Code:

1. Créer le dossier `.claude/commands/` à la racine du projet
2. Créer chaque fichier `.md` avec le contenu ci-dessus
3. Les commandes seront disponibles via `/nom-de-la-commande`

```bash
mkdir -p .claude/commands
# Créer les fichiers:
# - create-agent.md
# - create-endpoint.md
# - create-migration.md
# - write-test.md
# - run-tests.md
# - deploy.md
# - debug.md
```

---

*14 Janvier 2026*
