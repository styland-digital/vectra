# Vectra - AI Sales Agents Platform

Plateforme SaaS B2B d'agents IA pour automatiser la prospection (prospection → qualification BANT → emails personnalisés → rendez-vous).

## 🏗️ Architecture

- **Backend**: Python 3.11 + FastAPI + CrewAI
- **Frontend**: Next.js 14 + React 18 + Tailwind CSS
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7 + Celery 5.3
- **Agents IA**: CrewAI + Llama 2 70B

## 🚀 Quick Start

### Prérequis

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15 (via Docker)
- Redis 7 (via Docker)

### Installation

1. **Cloner le repository**
   ```bash
   git clone <repository-url>
   cd vectra
   ```

2. **Installer les dépendances**
   ```bash
   make install
   ```

3. **Configurer les variables d'environnement**
   ```bash
   # Backend
   cd backend
   cp .env.example .env
   # Éditer .env avec vos valeurs
   
   # Frontend
   cd ../frontend
   cp .env.example .env
   # Éditer .env avec vos valeurs
   ```

4. **Démarrer les services Docker**
   ```bash
   make docker-up
   ```

5. **Appliquer les migrations**
   ```bash
   make migrate
   ```

6. **Démarrer le développement**
   ```bash
   # Terminal 1: Backend
   cd backend
   uvicorn app.main:app --reload --port 8000
   
   # Terminal 2: Celery Worker
   cd backend
   celery -A app.tasks.celery_app worker --loglevel=INFO
   
   # Terminal 3: Frontend
   cd frontend
   npm run dev
   ```

## 📁 Structure du Projet

```
vectra/
├── backend/          # API FastAPI + Agents CrewAI
│   ├── app/
│   │   ├── api/v1/   # Routes REST
│   │   ├── agents/   # Prospector, BANT, Scheduler
│   │   ├── db/       # Models SQLAlchemy + Repositories
│   │   ├── services/ # Business logic
│   │   └── tasks/    # Celery tasks
│   └── tests/
├── frontend/         # Next.js Dashboard
│   ├── app/          # App Router
│   ├── components/   # React + Shadcn/ui
│   └── lib/          # Utils, API client
└── docs/             # Documentation
```

## 🔧 Commandes Disponibles

```bash
make help          # Afficher toutes les commandes
make install       # Installer les dépendances
make dev           # Démarrer l'environnement de développement
make docker-up     # Démarrer Docker services
make docker-down   # Arrêter Docker services
make test          # Lancer les tests
make lint          # Lancer les linters
make migrate       # Appliquer les migrations
make migrate-new   # Créer une nouvelle migration
make seed          # Seed la base de données
make clean         # Nettoyer les fichiers temporaires
```

## 🐳 Docker

### Développement avec Docker Compose

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

Services disponibles:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **API Docs**: http://localhost:8000/docs

## 🧪 Tests

```bash
# Backend
cd backend
pytest --cov=app

# Frontend
cd frontend
npm run test
npm run test:e2e
```

## 📚 Documentation

Toute la documentation est disponible dans le dossier `docs/`:

- `docs/MASTER-EXEC-001_GUIDE_EXECUTION.md` - Guide d'exécution complet
- `docs/tech/DOC-TECH-001_DATABASE_SCHEMA.md` - Schéma de base de données
- `docs/tech/DOC-TECH-002_API_CONTRACTS.md` - Contrats API
- `docs/tech/DOC-TECH-004_AGENT_PROMPTS.md` - Prompts des agents IA

## 🔐 Sécurité

- **TOUJOURS** filtrer par `organization_id` dans les queries
- **JAMAIS** de secrets dans le code (utiliser .env)
- **TOUJOURS** valider les inputs avec Pydantic
- JWT expire après 15 min, refresh après 7 jours

## 🤖 Les 3 Agents IA

1. **Prospector** - Trouve des prospects selon critères (RocketReach API)
2. **BANT** - Qualifie chaque prospect (score 0-100)
3. **Scheduler** - Génère emails personnalisés + Calendly

## 📝 License

Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

Pour toute question ou problème, consultez la documentation dans `docs/` ou créez une issue.

---

**Vectra** - Powering your pipeline, simply. 🚀
