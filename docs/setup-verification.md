# VECTRA - VÉRIFICATION DU SETUP

## ✅ Corrections Appliquées

### 1. Erreur Python - psycopg2-binary

**Problème :** `psycopg2-binary` nécessite `pg_config` sur Windows, ce qui cause des erreurs d'installation.

**Solution :** 
- Retiré `psycopg2-binary` de `requirements.txt`
- Utilisation d'`asyncpg` pour les opérations asynchrones (recommandé pour FastAPI)
- SQLAlchemy fonctionne avec asyncpg pour les connexions async

**Note :** Si vous avez besoin de `psycopg2-binary` plus tard, installez-le séparément :
```bash
pip install psycopg2-binary
```

### 2. Erreur Next.js - next/babel

**Problème :** ESLint ne trouvait pas le module `next/babel`.

**Solution :**
- Supprimé `.babelrc.json` (Next.js 14 utilise SWC par défaut, pas Babel)
- Retiré les dépendances Babel inutiles de `package.json`
- Next.js 14 gère automatiquement la compilation avec SWC

## 🧪 Tests de Vérification

### Frontend

```bash
cd frontend

# Linter
npm run lint
# ✅ Résultat attendu: "✔ No ESLint warnings or errors"

# Type check
npm run type-check
# ✅ Résultat attendu: Aucune erreur

# Build
npm run build
# ✅ Résultat attendu: Build réussi
```

### Backend

```bash
cd backend

# Créer venv si nécessaire
python -m venv venv

# Activer venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installer dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Tester les imports
python -c "import fastapi; import sqlalchemy; import asyncpg; print('OK')"
# ✅ Résultat attendu: "OK"
```

## ⚠️ Notes Importantes

1. **Python 3.11 requis** : Certaines dépendances (comme pydantic-core) peuvent nécessiter Rust avec Python 3.13+. Utilisez Python 3.11 comme spécifié dans les prérequis.

2. **asyncpg vs psycopg2** : 
   - `asyncpg` est recommandé pour FastAPI (async/await)
   - `psycopg2-binary` est optionnel et peut être installé séparément si nécessaire

3. **Next.js 14** : 
   - Utilise SWC par défaut (plus rapide que Babel)
   - Pas besoin de configuration Babel personnalisée
   - ESLint fonctionne avec `eslint-config-next`

## 📝 Commandes de Test Complètes

```bash
# Frontend
cd frontend
npm install
npm run lint
npm run type-check
npm run build

# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -c "import fastapi; print('FastAPI OK')"
python -c "import sqlalchemy; print('SQLAlchemy OK')"
python -c "import asyncpg; print('asyncpg OK')"
```

---

*Dernière mise à jour : 15 Janvier 2026*
