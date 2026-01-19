---
name: Phase 3 - Architecture Multi-Tenant Complète et Notifications
overview: ""
todos: []
---

# Plan d'Action Phase 3 : Architecture Multi-Tenant Complète et Notifications

## Vue d'Ensemble

Cette phase implémente:

1. **Platform Admin (Vectra Owner)** - Rôle PLATFORM_ADMIN sans organization_id
2. **Endpoints Organisation** - CRUD complet avec gestion multi-tenant
3. **Endpoints Utilisateurs dans Organisation** - Invitation, gestion des rôles
4. **Endpoints Notifications** - 5 scénarios supportés
5. **Mise à jour Postman** - Collection complète
6. **Tests complets** - Unit, Intégration, E2E

**Nouvelle Structure de Routes:**

- `/api/v1/auth/*` - Routes partagées (login, register, refresh, verify-email, etc.)
- `/api/v1/admin/*` - Routes Platform Admin uniquement (PLATFORM_ADMIN)
- `/api/v1/user/*` - Routes utilisateurs d'organisation (déplacées depuis `/user/me`)

---

## 1. ARCHITECTURE PLATFORM ADMIN

### 1.1 Modification Base de Données

**Fichier:** `backend/alembic/versions/003_add_platform_admin.py` (nouveau)

**Actions:**

- Migration pour rendre `organization_id` nullable dans `users` table
- Migration pour ajouter `PLATFORM_ADMIN` dans l'enum `user_role`
- Migration pour ajouter index sur `organization_id` (NULL possible)

**Code clé:**

```sql
-- Rendre organization_id nullable
ALTER TABLE users ALTER COLUMN organization_id DROP NOT NULL;

-- Ajouter PLATFORM_ADMIN au type enum (via DROP/CREATE)
ALTER TYPE user_role ADD VALUE 'platform_admin';

-- Index pour queries platform_admin
CREATE INDEX idx_users_org_null ON users(organization_id) WHERE organization_id IS NULL;
```

**Fichier:** `backend/app/db/models/user.py`

**Modifications:**

- Ajouter `PLATFORM_ADMIN = "platform_admin"` dans `UserRole` enum
- Modifier `organization_id` pour `nullable=True`
- Ajouter méthode `is_platform_admin() -> bool` qui vérifie `role == PLATFORM_ADMIN and organization_id is None`

---

### 1.2 Dépendances API Platform Admin

**Fichier:** `backend/app/api/deps.py`

**Ajouter:**

```python
def get_platform_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user and verify they are platform admin."""
    if current_user.role != UserRole.PLATFORM_ADMIN or current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform admin access required",
        )
    return current_user

def get_organization_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user and verify they belong to an organization (not platform admin)."""
    if current_user.role == UserRole.PLATFORM_ADMIN or not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization user access required",
        )
    return current_user
```

---

## 2. ENDPOINTS PLATFORM ADMIN (`/api/v1/admin/*`)

### 2.1 Route Platform Admin

**Fichier:** `backend/app/api/v1/admin.py` (nouveau, au lieu de `platform.py`)

**Endpoints à implémenter:**

#### GET `/admin/overview`

- Statistiques globales: total orgs, total users, campagnes actives, leads totaux
- Métriques: taux de conversion, emails envoyés, RDVs planifiés
- Utilise `get_platform_admin`

#### GET `/admin/organizations`

- Liste toutes les organisations avec filtres (plan, statut)
- Pagination et tri
- Utilise `get_platform_admin`

#### GET `/admin/organizations/{org_id}`

- Détails d'une organisation spécifique
- Utilise `get_platform_admin`

#### POST `/admin/organizations`

- Créer une nouvelle organisation (manuelle)
- Utilise `get_platform_admin`

#### PATCH `/admin/organizations/{org_id}`

- Modifier organisation (plan, settings, suspend)
- Utilise `get_platform_admin`

#### DELETE `/admin/organizations/{org_id}`

- Supprimer organisation (soft delete ou hard delete)
- Utilise `get_platform_admin`

#### GET `/admin/users`

- Liste tous les utilisateurs de toutes les orgs
- Filtres par org, rôle, statut
- Utilise `get_platform_admin`

#### GET `/admin/system/metrics`

- Métriques système: performance API, latence agents, erreurs
- Utilise `get_platform_admin`

#### POST `/admin/notifications/send`

- Envoyer notifications (types: `vectra_to_users`, `vectra_to_org_owner`, `system_alerts`)
- Utilise `get_platform_admin`

**Fichier:** `backend/app/services/platform.py` (nouveau)

**Services à créer:**

- `PlatformService` avec méthodes: `get_overview()`, `list_organizations()`, `create_organization()`, `update_organization()`, `delete_organization()`, `list_all_users()`, `get_system_metrics()`

**Fichier:** `backend/app/schemas/platform.py` (nouveau)

**Schemas:**

- `PlatformOverviewResponse`
- `PlatformOrganizationResponse`
- `PlatformOrganizationCreate`
- `PlatformOrganizationUpdate`
- `PlatformUserResponse`
- `PlatformSystemMetricsResponse`

---

## 3. ENDPOINTS USER/ORGANISATION (`/api/v1/user/*`)

### 3.1 Route User

**Fichier:** `backend/app/api/v1/user.py` (nouveau)

**Endpoints à implémenter:**

#### GET `/user/me`

- Détails de l'utilisateur actuel (DÉPLACÉ depuis `/user/me`)
- Utilise `get_current_user` (tous les users, y compris platform admin peuvent l'utiliser)

#### GET `/user/organizations/me`

- Détails de l'organisation de l'utilisateur actuel
- Utilise `get_organization_user` (vérifie que user appartient à une org)

#### PATCH `/user/organizations/me`

- Modifier sa propre organisation (Owner/Admin uniquement)
- Utilise `get_organization_user` + `require_role([UserRole.OWNER, UserRole.ADMIN])`

#### GET `/user/organizations/me/users`

- Liste des utilisateurs de l'organisation
- Utilise `get_organization_user` + `require_role([UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER])`

#### POST `/user/organizations/me/users/invite`

- Inviter un nouvel utilisateur dans l'org
- Email d'invitation avec token/lien
- Utilise `get_organization_user` + `require_role([UserRole.OWNER, UserRole.ADMIN])`

#### PATCH `/user/organizations/me/users/{user_id}/role`

- Modifier le rôle d'un utilisateur dans l'org
- Utilise `get_organization_user` + `require_role([UserRole.OWNER, UserRole.ADMIN])`

#### DELETE `/user/organizations/me/users/{user_id}`

- Retirer un utilisateur de l'org (soft delete ou hard delete)
- Utilise `get_organization_user` + `require_role([UserRole.OWNER, UserRole.ADMIN])`

#### POST `/user/notifications/send`

- Envoyer notifications (types: `org_to_prospects`, `org_owner_to_members`)
- Utilise `get_organization_user` + vérification permissions selon type

**Fichier:** `backend/app/services/organization.py` (nouveau ou existant à étendre)

**Services:**

- `OrganizationService.get_my_organization()`
- `OrganizationService.update_my_organization()`
- `OrganizationService.list_users()`
- `OrganizationService.invite_user()`
- `OrganizationService.update_user_role()`
- `OrganizationService.remove_user()`

**Fichier:** `backend/app/schemas/organization.py` (nouveau)

**Schemas:**

- `OrganizationResponse`
- `OrganizationUpdate`
- `OrganizationUserResponse`
- `InviteUserRequest`
- `UpdateUserRoleRequest`

**Fichier:** `backend/app/services/invitation.py` (nouveau)

**Service:**

- `InvitationService` pour générer tokens d'invitation, envoyer emails d'invitation, accepter invitation

---

## 4. ENDPOINTS NOTIFICATIONS

### 4.1 Routes Notifications Séparées

**Fichier:** `backend/app/api/v1/admin.py` (notifications admin)

**Endpoint:**

#### POST `/admin/notifications/send`

- Types: `vectra_to_users`, `vectra_to_org_owner`, `system_alerts`
- Utilise `get_platform_admin`

**Fichier:** `backend/app/api/v1/user.py` (notifications user)

**Endpoint:**

#### POST `/user/notifications/send`

- Types: `org_to_prospects`, `org_owner_to_members`
- Utilise `get_organization_user` + vérification permissions

**Request Schema (commun):**

```json
{
  "type": "org_to_prospects" | "vectra_to_users" | "vectra_to_org_owner" | "system_alerts" | "org_owner_to_members",
  "recipients": ["email1@example.com", ...],  // ou organization_id, ou "all"
  "subject": "...",
  "body": "...",
  "body_html": "...",  // optionnel
  "action_url": "...",  // optionnel
  "action_text": "..."  // optionnel
}
```

**Contraintes:**

- `org_to_prospects`: Owner/Admin de l'org peut envoyer à liste de prospects (emails)
- `vectra_to_users`: Platform Admin uniquement, peut envoyer à tous les users
- `vectra_to_org_owner`: Platform Admin uniquement, peut envoyer aux owners d'orgs spécifiques
- `system_alerts`: Platform Admin uniquement
- `org_owner_to_members`: Owner/Admin de l'org peut envoyer aux membres de leur org

**Fichier:** `backend/app/services/notification.py` (nouveau)

**Service:**

- `NotificationService.send_notification()` avec logique de vérification des permissions selon le type

**Fichier:** `backend/app/schemas/notification.py` (nouveau)

**Schemas:**

- `SendNotificationRequest`
- `NotificationResponse`

---

## 5. MODIFICATIONS AUTHENTIFICATION

### 5.1 Routes Auth Partagées (inchangées)

**Fichier:** `backend/app/api/v1/auth.py`

**Routes qui restent sous `/auth/*` (partagées pour tous):**

- `POST /auth/login` - Login (tous)
- `POST /auth/register` - Register (tous)
- `POST /auth/refresh` - Refresh token (tous)
- `POST /auth/logout` - Logout (tous)
- `POST /auth/change-password` - Change password (tous)
- `POST /auth/verify-email` - Verify email (tous)
- `POST /auth/send-verification-email` - Send verification email (tous)
- `POST /auth/resend-verification-email` - Resend verification email (tous)
- `POST /auth/forgot-password` - Forgot password (tous)
- `POST /auth/reset-password` - Reset password (tous)

**Route à DÉPLACER:**

- `GET /user/me` → `GET /user/me` (déplacé vers `user.py`)

### 5.2 Enregistrement Platform Admin

**Fichier:** `backend/app/services/auth.py`

**Modification:**

- Dans `register()`, vérifier si l'email correspond à `settings.PLATFORM_ADMIN_EMAIL`
- Si oui, créer user avec `role=PLATFORM_ADMIN` et `organization_id=None`

**Fichier:** `backend/app/core/config.py`

**Ajouter:**

```python
PLATFORM_ADMIN_EMAIL: str = "admin@vectra.io"  # Configurable via env
```

---

## 6. ROUTER PRINCIPAL

**Fichier:** `backend/app/api/v1/router.py`

**Modifications:**

```python
from app.api.v1 import auth, admin, user

# Routes partagées (auth)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Routes Platform Admin
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

# Routes User/Organisation
api_router.include_router(user.router, prefix="/user", tags=["user"])
```

**Note:** Le router auth ne doit plus inclure `/me` (déplacé vers user.py)

---

## 7. TESTS

### 7.1 Tests Unitaires

**Fichiers à créer:**

- `backend/tests/unit/services/test_platform_service.py`
- `backend/tests/unit/services/test_organization_service.py`
- `backend/tests/unit/services/test_invitation_service.py`
- `backend/tests/unit/services/test_notification_service.py`

### 7.2 Tests d'Intégration API

**Fichiers à créer:**

- `backend/tests/integration/api/test_admin_api.py` (remplace test_platform_api.py)
- `backend/tests/integration/api/test_user_api.py` (remplace test_organizations_api.py)
- `backend/tests/integration/api/test_user_notifications_api.py`
- `backend/tests/integration/api/test_admin_notifications_api.py`

### 7.3 Tests E2E

**Fichiers à créer/mettre à jour:**

- `backend/tests/e2e/test_platform_admin_flow.py`
- `backend/tests/e2e/test_organization_management_flow.py`
- `backend/tests/e2e/test_notification_flow.py`

**Scénarios:**

- Platform Admin crée une org, invite des users, envoie notifications via `/admin/*`
- Owner d'org invite des membres, change des rôles, envoie notifications via `/user/*`
- Utilisateur accepte invitation et rejoint l'org
- Test `/user/me` vs `/user/me` (redirection)

---

## 8. MISE À JOUR POSTMAN

**Fichier:** `docs/postman/Vectra_API_Collection.json`

**Sections à ajouter/modifier:**

### Routes Partagées (`/auth/*`)

- ✅ Déjà présentes (login, register, refresh, etc.)
- ❌ Retirer `/user/me` (déplacé vers `/user/me`)

### Platform Admin (`/admin/*`) - 11 endpoints

- `GET /admin/overview`
- `GET /admin/organizations`
- `GET /admin/organizations/{org_id}`
- `POST /admin/organizations`
- `PATCH /admin/organizations/{org_id}`
- `DELETE /admin/organizations/{org_id}`
- `GET /admin/users`
- `GET /admin/system/metrics`
- `POST /admin/notifications/send` (types: vectra_to_users, vectra_to_org_owner, system_alerts)

### User/Organisation (`/user/*`) - 8 endpoints

- `GET /user/me` (nouveau, déplacé depuis /user/me)
- `GET /user/organizations/me`
- `PATCH /user/organizations/me`
- `GET /user/organizations/me/users`
- `POST /user/organizations/me/users/invite`
- `PATCH /user/organizations/me/users/{user_id}/role`
- `DELETE /user/organizations/me/users/{user_id}`
- `POST /user/notifications/send` (types: org_to_prospects, org_owner_to_members)

**Variables d'environnement:**

- `platform_admin_token` (token du platform admin)
- `user_token` (token d'un user d'org)
- `organization_id`
- `user_id`
- `invitation_token`

---

## 9. TEMPLATES EMAIL

**Fichiers à créer:**

- `backend/app/templates/emails/invite-user.html` - Email d'invitation utilisateur
- `backend/app/templates/emails/organization-update.html` - Notification changement org

**Modifications:**

- `backend/app/templates/emails/notification.html` - Déjà existe, vérifier qu'il supporte tous les types

---

## 10. DOCUMENTATION

**Fichiers à mettre à jour:**

- `docs/tech/DOC-TECH-002_API_CONTRACTS.md` - Ajouter tous les nouveaux endpoints avec nouvelle structure `/admin/*` et `/user/*`
- `docs/tech/DOC-TECH-001_DATABASE_SCHEMA.md` - Documenter changement organization_id nullable
- `docs/workflow/logs/planning/2026-01-18_phase3-planning.md` - Nouveau fichier de planning

---

## ORDRE D'IMPLÉMENTATION

1. **Migration DB** - Ajouter PLATFORM_ADMIN, rendre organization_id nullable
2. **Modèles** - Modifier User model, ajouter méthodes
3. **Dépendances** - Ajouter `get_platform_admin` et `get_organization_user`
4. **Modifications Auth** - Déplacer `/user/me` vers `/user/me`, support création platform admin
5. **Services Platform** - PlatformService avec logique métier
6. **Endpoints Admin** - Tous les endpoints `/admin/*`
7. **Services Organisation** - OrganizationService et InvitationService
8. **Endpoints User** - Tous les endpoints `/user/*` (dont `/user/me`)
9. **Service Notifications** - NotificationService avec logique de permissions
10. **Endpoints Notifications** - POST `/admin/notifications/send` et POST `/user/notifications/send`
11. **Templates Email** - Invitation et notifications
12. **Router Principal** - Mise à jour avec nouvelles routes
13. **Tests Unitaires** - Tous les services
14. **Tests Intégration** - Tous les endpoints (/admin/*et /user/*)
15. **Tests E2E** - Flux complets
16. **Postman** - Mise à jour collection avec nouvelle structure
17. **Documentation** - Mise à jour API contracts

---

## RÉSUMÉ DES CHANGEMENTS DE STRUCTURE

### Avant

```
/api/v1/user/me → GET utilisateur actuel
/api/v1/platform/* → Routes platform admin (à créer)
/api/v1/organizations/* → Routes organisation (à créer)
/api/v1/notifications/* → Routes notifications (à créer)
```

### Après

```
/api/v1/auth/* → Routes partagées (login, register, refresh, etc.) - SANS /me
/api/v1/admin/* → Routes Platform Admin uniquement
/api/v1/user/* → Routes utilisateurs d'organisation (dont /user/me)
/api/v1/admin/notifications/send → Notifications admin
/api/v1/user/notifications/send → Notifications user
```

---

*Plan modifié le 18 Janvier 2026 - Structure /admin et /user séparée*