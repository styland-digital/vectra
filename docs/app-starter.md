# VECTRA - GUIDE DE DÉMARRAGE COMPLET

## Instructions pour lancer l'application (première fois et suivantes)

### Version 1.0 | 15 Janvier 2026

---

## 📋 PRÉREQUIS EXACTS

### Logiciels Requis

| Logiciel | Version Minimum | Vérification | Installation |
|----------|----------------|--------------|--------------|
| **Python** | 3.11+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 20+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | `npm --version` | Inclus avec Node.js |
| **Docker** | 24+ | `docker --version` | [docker.com](https://www.docker.com/get-started) |
| **Docker Compose** | 2.20+ | `docker compose version` | Inclus avec Docker Desktop |
| **Git** | 2.30+ | `git --version` | [git-scm.com](https://git-scm.com/) |

### Vérification des Prérequis

```bash
# Vérifier Python
python --version
# Doit afficher: Python 3.11.x ou supérieur

# Vérifier Node.js
node --version
# Doit afficher: v20.x.x ou supérieur

# Vérifier npm
npm --version
# Doit afficher: 9.x.x ou supérieur

# Vérifier Docker
docker --version
# Doit afficher: Docker version 24.x.x ou supérieur

# Vérifier Docker Compose
docker compose version
# Doit afficher: Docker Compose version 2.20.x ou supérieur

# Vérifier Git
git --version
# Doit afficher: git version 2.30.x ou supérieur
```

### Ports Disponibles

Assurez-vous que ces ports sont libres :

- **5432** : PostgreSQL
- **6379** : Redis
- **8000** : Backend API
- **3000** : Frontend Next.js

---

## 🚀 PREMIÈRE FOIS - SETUP COMPLET

### Étape 1 : Cloner le Repository (si nécessaire)

```bash
# Si vous n'avez pas encore cloné le repo
git clone <repository-url>
cd vectra
```

### Étape 2 : Vérifier la Structure

```bash
# Vérifier que la structure est correcte
ls -la
# Doit afficher: backend/, frontend/, docs/, docker-compose.yml, Makefile, README.md

# Vérifier backend
ls backend/
# Doit afficher: app/, tests/, alembic/, requirements.txt, Dockerfile

# Vérifier frontend
ls frontend/
# Doit afficher: app/, components/, package.json, next.config.js
```

### Étape 3 : Configurer les Variables d'Environnement

#### Backend

```bash
# Aller dans le dossier backend
cd backend

# Copier le fichier .env.example vers .env
cp .env.example .env

# Éditer le fichier .env (utiliser votre éditeur préféré)
# Sur Windows: notepad .env
# Sur Mac/Linux: nano .env ou vim .env
```

**Contenu minimum du fichier `backend/.env` :**

```bash
# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
SECRET_KEY=change-me-in-production-use-a-strong-random-key

# Database (ne pas modifier si vous utilisez Docker Compose)
DATABASE_URL=postgresql://vectra:vectra@localhost:5432/vectra

# Redis (ne pas modifier si vous utilisez Docker Compose)
REDIS_URL=redis://localhost:6379/0

# JWT - GÉNÉRER UNE CLÉ SÉCURISÉE
JWT_SECRET=your-jwt-secret-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# LLM
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=https://api.ollama.com
OLLAMA_MODEL=llama2:70b

# External APIs (optionnel pour le démarrage)
ROCKETREACH_API_KEY=
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=noreply@vectra.io
CALENDLY_API_KEY=
HUBSPOT_API_KEY=
```

**Pour générer une clé JWT_SECRET sécurisée :**

```bash
# Sur Linux/Mac
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Sur Windows PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Frontend

```bash
# Retourner à la racine
cd ..

# Aller dans le dossier frontend
cd frontend

# Copier le fichier .env.example vers .env
cp .env.example .env

# Éditer le fichier .env
# Sur Windows: notepad .env
# Sur Mac/Linux: nano .env ou vim .env
```

**Contenu du fichier `frontend/.env` :**

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Auth - GÉNÉRER UNE CLÉ SÉCURISÉE
NEXTAUTH_SECRET=your-nextauth-secret-change-this-in-production
NEXTAUTH_URL=http://localhost:3000
```

**Pour générer une clé NEXTAUTH_SECRET sécurisée :**

```bash
# Sur Linux/Mac
openssl rand -base64 32

# Sur Windows PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Étape 4 : Installer les Dépendances Backend

```bash
# Retourner à la racine
cd ..

# Aller dans backend
cd backend

# Créer un environnement virtuel Python
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Vérifier l'installation
python -c "import fastapi; print('FastAPI installé')"
python -c "import sqlalchemy; print('SQLAlchemy installé')"
```

### Étape 5 : Installer les Dépendances Frontend

```bash
# Retourner à la racine
cd ..

# Aller dans frontend
cd frontend

# Installer les dépendances npm
npm install

# Vérifier l'installation
npm list --depth=0
```

### Étape 6 : Démarrer les Services Docker

```bash
# Retourner à la racine
cd ..

# Démarrer PostgreSQL et Redis avec Docker Compose
docker compose up -d postgres redis

# Vérifier que les services sont démarrés
docker compose ps

# Attendre 5-10 secondes que les services soient prêts
# Vérifier les logs
docker compose logs postgres
docker compose logs redis
```

**Vérification manuelle :**

```bash
# Tester la connexion PostgreSQL
docker exec -it vectra-postgres psql -U vectra -d vectra -c "SELECT version();"

# Tester Redis
docker exec -it vectra-redis redis-cli ping
# Doit répondre: PONG
```

### Étape 7 : Appliquer les Migrations de Base de Données

```bash
# Aller dans backend
cd backend

# Activer l'environnement virtuel si ce n'est pas déjà fait
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Appliquer les migrations
alembic upgrade head

# Vérifier que les tables sont créées
# Sur Windows PowerShell:
docker exec -it vectra-postgres psql -U vectra -d vectra -c "\dt"
# Sur Mac/Linux:
docker exec -it vectra-postgres psql -U vectra -d vectra -c "\dt"
```

### Étape 8 : Démarrer l'Application

#### Option A : Avec Docker Compose (Recommandé)

```bash
# Retourner à la racine
cd ..

# Démarrer tous les services (backend, frontend, celery)
docker compose up -d

# Voir les logs
docker compose logs -f

# Pour arrêter
docker compose down
```

#### Option B : Développement Local (Recommandé pour le développement)

**Terminal 1 - Backend :**

```bash
cd backend

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Démarrer le serveur FastAPI
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

**Terminal 2 - Celery Worker :**

```bash
cd backend

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Démarrer Celery worker
celery -A app.tasks.celery_app worker --loglevel=INFO
```

**Terminal 3 - Frontend :**

```bash
cd frontend

# Démarrer le serveur Next.js
npm run dev
```

### Étape 9 : Vérifier que Tout Fonctionne

1. **Backend API :**
   - Ouvrir : <http://localhost:8000>
   - Doit afficher : `{"message":"Vectra API","version":"1.0.0","status":"running"}`
   - Documentation API : <http://localhost:8000/docs>

2. **Health Check Backend :**
   - Ouvrir : <http://localhost:8000/health>
   - Doit afficher : `{"status":"healthy","service":"vectra-backend"}`

3. **Frontend :**
   - Ouvrir : <http://localhost:3000>
   - Doit afficher la page d'accueil Vectra

4. **Health Check Frontend :**
   - Ouvrir : <http://localhost:3000/api/health>
   - Doit afficher : `{"status":"healthy","service":"vectra-frontend","timestamp":"..."}`

---

## 🔄 FOIS SUIVANTES - DÉMARRAGE RAPIDE

### Méthode 1 : Avec Docker Compose (Rapide)

```bash
# Aller à la racine du projet
cd vectra

# Démarrer les services Docker
docker compose up -d postgres redis

# Attendre 5 secondes
sleep 5

# Démarrer backend et frontend localement
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Mac/Linux
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Celery
cd backend
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Mac/Linux
celery -A app.tasks.celery_app worker --loglevel=INFO

# Terminal 3 - Frontend
cd frontend
npm run dev
```

### Méthode 2 : Tout avec Docker Compose

```bash
# Aller à la racine du projet
cd vectra

# Démarrer tous les services
docker compose up -d

# Voir les logs
docker compose logs -f

# Arrêter tous les services
docker compose down
```

### Méthode 3 : Avec Makefile

```bash
# Aller à la racine du projet
cd vectra

# Démarrer Docker services
make docker-up

# Démarrer le développement (nécessite 3 terminaux)
# Le Makefile ne démarre pas automatiquement les serveurs
# Utiliser les commandes de la Méthode 1
```

---

## 🛠️ COMMANDES UTILES

### Docker

```bash
# Démarrer les services
docker compose up -d postgres redis

# Voir les logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
docker compose logs -f redis

# Arrêter les services
docker compose down

# Arrêter et supprimer les volumes (⚠️ supprime les données)
docker compose down -v

# Redémarrer un service
docker compose restart backend
docker compose restart frontend

# Voir le statut
docker compose ps
```

### Base de Données

```bash
# Appliquer les migrations
cd backend
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Mac/Linux
alembic upgrade head

# Créer une nouvelle migration
alembic revision --autogenerate -m "description de la migration"

# Se connecter à PostgreSQL
docker exec -it vectra-postgres psql -U vectra -d vectra

# Lister les tables
\dt

# Quitter PostgreSQL
\q
```

### Backend

```bash
cd backend

# Activer l'environnement virtuel
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Mac/Linux

# Démarrer le serveur
uvicorn app.main:app --reload --port 8000

# Lancer les tests
pytest

# Lancer les tests avec coverage
pytest --cov=app

# Linter
black .
ruff check .

# Formater le code
black .
```

### Frontend

```bash
cd frontend

# Démarrer le serveur de développement
npm run dev

# Build pour production
npm run build

# Lancer les tests
npm run test

# Lancer les tests E2E
npm run test:e2e

# Linter
npm run lint

# Type check
npm run type-check
```

---

## 🐛 DÉPANNAGE

### Problème : Port déjà utilisé

```bash
# Trouver le processus utilisant le port
# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :5432
netstat -ano | findstr :6379

# Mac/Linux:
lsof -i :8000
lsof -i :3000
lsof -i :5432
lsof -i :6379

# Arrêter le processus (remplacer PID par le numéro trouvé)
# Windows:
taskkill /PID <PID> /F

# Mac/Linux:
kill -9 <PID>
```

### Problème : Docker ne démarre pas

```bash
# Vérifier que Docker est démarré
docker ps

# Redémarrer Docker Desktop (Windows/Mac)
# Ou redémarrer le service Docker (Linux)
sudo systemctl restart docker
```

### Problème : Erreur de connexion à la base de données

```bash
# Vérifier que PostgreSQL est démarré
docker compose ps postgres

# Vérifier les logs
docker compose logs postgres

# Redémarrer PostgreSQL
docker compose restart postgres

# Vérifier la connexion
docker exec -it vectra-postgres psql -U vectra -d vectra -c "SELECT 1;"
```

### Problème : Erreur de dépendances Python

```bash
cd backend

# Recréer l'environnement virtuel
rm -rf venv  # Mac/Linux
# ou rmdir /s venv  # Windows

python -m venv venv
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Mac/Linux

pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Problème : Erreur de dépendances Node.js

```bash
cd frontend

# Supprimer node_modules et package-lock.json
rm -rf node_modules package-lock.json  # Mac/Linux
# ou rmdir /s node_modules & del package-lock.json  # Windows

# Réinstaller
npm install
```

### Problème : Migrations ne s'appliquent pas

```bash
cd backend

# Vérifier l'état des migrations
alembic current

# Voir l'historique
alembic history

# Forcer la mise à jour
alembic upgrade head

# Si problème, réinitialiser (⚠️ supprime les données)
docker compose down -v
docker compose up -d postgres redis
sleep 5
alembic upgrade head
```

---

## ✅ CHECKLIST DE VÉRIFICATION

Avant de commencer à développer, vérifiez :

- [ ] Tous les prérequis sont installés et aux bonnes versions
- [ ] Les fichiers `.env` sont créés dans `backend/` et `frontend/`
- [ ] Les clés `JWT_SECRET` et `NEXTAUTH_SECRET` sont générées et sécurisées
- [ ] Les dépendances backend sont installées (`pip list`)
- [ ] Les dépendances frontend sont installées (`npm list`)
- [ ] Docker Compose démarre PostgreSQL et Redis sans erreur
- [ ] Les migrations sont appliquées (`alembic current`)
- [ ] Le backend démarre sur <http://localhost:8000>
- [ ] Le frontend démarre sur <http://localhost:3000>
- [ ] Les health checks répondent correctement
- [ ] La documentation API est accessible sur <http://localhost:8000/docs>

---

## 📚 RESSOURCES

- **Documentation API** : <http://localhost:8000/docs>
- **Documentation complète** : `/docs/`
- **Guide d'exécution** : `/docs/MASTER-EXEC-001_GUIDE_EXECUTION.md`
- **Schéma de base de données** : `/docs/tech/DOC-TECH-001_DATABASE_SCHEMA.md`
- **Contrats API** : `/docs/tech/DOC-TECH-002_API_CONTRACTS.md`

---

**Dernière mise à jour : 15 Janvier 2026**

*En cas de problème, consultez la section Dépannage ou créez une issue.*
