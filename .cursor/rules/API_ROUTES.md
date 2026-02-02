# VECTRA - Règles de Routage API

## Structure des Routes

### Préfixes

- `/api/v1/auth/*` - Authentification (public, pas d'isolation)
- `/api/v1/user/*` - Utilisateurs et organisations (authentifié, **isolation multi-tenant obligatoire**)
- `/api/v1/admin/*` - Administration plateforme (PLATFORM_ADMIN uniquement, **pas d'isolation**)

### Règles par Préfixe

#### `/api/v1/auth/*`

- **Public:** Pas d'authentification requise
- **Isolation:** Aucune (endpoints publics)
- **Exemples:**
  - `POST /auth/login`
  - `POST /auth/register`
  - `POST /auth/invite/accept`

#### `/api/v1/user/*`

- **Authentification:** Requise (JWT Bearer token)
- **Isolation:** OBLIGATOIRE - TOUJOURS filtrer par `organization_id`
- **Permissions:** Respecter les rôles (Owner > Admin > Manager > Operator > Viewer)
- **Dépendance:** `get_organization_user` (utilisateur doit avoir une organisation)
- **Exemples:**
  - `GET /user/me`
  - `GET /user/organizations/me`
  - `GET /user/campaigns`
  - `POST /user/organizations/me/users/invite`

**Pattern obligatoire:**

```python
@router.get("/some-resource")
def list_resources(
    current_user: User = Depends(get_organization_user),  # Filtre automatique par org
    db: Session = Depends(get_db),
):
    # TOUJOURS filtrer par organization_id
    resources = db.query(Resource).filter(
        Resource.organization_id == current_user.organization_id
    ).all()
    return resources
```

#### `/api/v1/admin/*`

- **Authentification:** Requise (JWT Bearer token)
- **Isolation:** AUCUNE (accès global à toutes les données)
- **Permission:** Uniquement `PLATFORM_ADMIN` (rôle `PLATFORM_ADMIN` et `organization_id` NULL)
- **Dépendance:** `get_platform_admin` (vérifie le rôle)
- **Exemples:**
  - `GET /admin/overview`
  - `GET /admin/organizations`
  - `POST /admin/organizations`

**Pattern obligatoire:**

```python
@router.get("/some-resource")
def list_all_resources(
    current_user: User = Depends(get_platform_admin),  # Vérifie PLATFORM_ADMIN
    db: Session = Depends(get_db),
):
    # Pas de filtrage multi-tenant (accès global)
    resources = db.query(Resource).all()
    return resources
```

## Règles de Sécurité

### Pour `/user/*`

1. **TOUJOURS** utiliser `get_organization_user` comme dépendance
2. **TOUJOURS** filtrer par `current_user.organization_id` dans les queries
3. **NE JAMAIS** exposer les données d'autres organisations
4. **Valider les permissions** selon le rôle (Owner/Admin pour certaines actions)

### Pour `/admin/*`

1. **TOUJOURS** utiliser `get_platform_admin` comme dépendance
2. **NE JAMAIS** filtrer par `organization_id` (accès global)
3. **Vérifier** que l'utilisateur a bien `role=PLATFORM_ADMIN` et `organization_id=NULL`

## Dependencies FastAPI

```python
# Pour /user/*
from app.api.deps import get_organization_user

# Pour /admin/*
from app.api.deps import get_platform_admin

# Pour /auth/*
# Pas de dépendance spéciale (public ou get_current_user pour certains)
```

## Validation des Rôles

### Hiérarchie des Rôles (Organisation)

1. **OWNER** - Propriétaire (tout)
2. **ADMIN** - Administrateur (presque tout sauf supprimer l'org)
3. **MANAGER** - Manager (gestion opérationnelle)
4. **OPERATOR** - Opérateur (actions limitées)
5. **VIEWER** - Observateur (lecture seule)

### Rôle Platform Admin

- **PLATFORM_ADMIN** - Administrateur de la plateforme (accès global, pas d'organisation)

## Exemples de Fichiers

### `backend/app/api/v1/user.py`

```python
from app.api.deps import get_organization_user

router = APIRouter()

@router.get("/me")
def get_me(
    current_user: User = Depends(get_organization_user),
):
    return current_user
```

### `backend/app/api/v1/admin.py`

```python
from app.api.deps import get_platform_admin

router = APIRouter()

@router.get("/overview")
def get_overview(
    current_user: User = Depends(get_platform_admin),
    db: Session = Depends(get_db),
):
    # Accès global
    return {"total_organizations": db.query(Organization).count()}
```

### `backend/app/api/v1/router.py`

```python
from app.api.v1 import auth, user, admin

api_router = APIRouter(prefix="/api/v1")

# Public
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# User/Organization (multi-tenant)
api_router.include_router(user.router, prefix="/user", tags=["user"])

# Platform Admin (global)
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
```
