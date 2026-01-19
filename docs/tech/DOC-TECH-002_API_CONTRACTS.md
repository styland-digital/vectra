# VECTRA - CONTRATS API

## OpenAPI 3.0 Specification

### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-003  
**Statut:** PRET POUR IMPLEMENTATION  
**Base URL:** `https://api.vectra.io/v1`  
**Format:** OpenAPI 3.0.3  

---

## TABLE DES MATIERES

1. Vue d'Ensemble
2. Authentification
3. Conventions et Standards
4. Endpoints - Authentication
5. Endpoints - Organizations
6. Endpoints - Users
7. Endpoints - Campaigns
8. Endpoints - Leads
9. Endpoints - Emails
10. Endpoints - Meetings
11. Endpoints - Analytics
12. Webhooks
13. Schemas
14. Codes d'Erreur
15. Rate Limiting

---

## 1. VUE D'ENSEMBLE

### 1.1 Introduction

L'API Vectra permet d'interagir programmatiquement avec la plateforme de prospection IA. Elle suit les principes REST et utilise JSON pour les échanges de données.

### 1.2 Base URLs

| Environnement | URL |
|---------------|-----|
| Production | `https://api.vectra.io/v1` |
| Staging | `https://api.staging.vectra.io/v1` |
| Development | `http://localhost:8000/v1` |

### 1.3 Résumé des Endpoints

| Ressource | Description | Méthodes | Préfixe |
|-----------|-------------|----------|---------|
| `/auth` | Authentification | POST | `/api/v1` |
| `/user` | Endpoints utilisateurs/organisation | GET, POST, PATCH, DELETE | `/api/v1` |
| `/admin` | Endpoints administrateur plateforme | GET, POST, PATCH, DELETE | `/api/v1` |
| `/user/campaigns` | Gestion des campagnes | GET, POST, PATCH, DELETE | `/api/v1` |
| `/leads` | Gestion des leads | GET, POST, PATCH | `/api/v1` |
| `/emails` | Gestion des emails | GET, POST, PATCH | `/api/v1` |
| `/meetings` | Gestion des meetings | GET, POST, PATCH | `/api/v1` |
| `/analytics` | Métriques et rapports | GET | `/api/v1` |
| `/webhooks` | Configuration webhooks | GET, POST, DELETE | `/api/v1` |

**Structure des routes:**

- `/api/v1/auth/*` - Authentification (public)
- `/api/v1/user/*` - Utilisateurs et organisations (authentifié)
- `/api/v1/admin/*` - Administration plateforme (PLATFORM_ADMIN uniquement)

---

## 2. AUTHENTIFICATION

### 2.1 Méthode

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

**Header requis:**

```
Authorization: Bearer <access_token>
```

### 2.2 Flux d'authentification

1. L'utilisateur s'authentifie via `POST /auth/login`
2. L'API retourne `access_token` (15 min) et `refresh_token` (7 jours)
3. L'access token est inclus dans chaque requête
4. Quand l'access token expire, utiliser `POST /auth/refresh`

### 2.3 Exemple

```json
// Request: POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword123"
}

// Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "admin"
  }
}
```

---

## 3. CONVENTIONS ET STANDARDS

### 3.1 Format des requêtes

- **Content-Type:** `application/json`
- **Encoding:** UTF-8
- **Dates:** ISO 8601 (`2026-01-14T10:30:00Z`)
- **UUIDs:** Format standard (ex: `550e8400-e29b-41d4-a716-446655440000`)

### 3.2 Pagination

Toutes les listes supportent la pagination via query parameters:

| Paramètre | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | integer | 1 | - | Numéro de page |
| `per_page` | integer | 20 | 100 | Éléments par page |
| `sort` | string | `created_at` | - | Champ de tri |
| `order` | string | `desc` | - | `asc` ou `desc` |

**Response pagination:**

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

### 3.3 Filtrage

Les endpoints de liste supportent le filtrage via query parameters:

```
GET /leads?status=qualified&bant_score_min=60&created_after=2026-01-01
```

### 3.4 Format des réponses

**Succès (2xx):**

```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-01-14T10:30:00Z"
  }
}
```

**Erreur (4xx/5xx):**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-01-14T10:30:00Z"
  }
}
```

---

## 4. ENDPOINTS - AUTHENTICATION

### POST /auth/login

Authentifie un utilisateur et retourne les tokens.

**Request:**

```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response: 200 OK**

```json
{
  "data": {
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "id": "uuid",
      "email": "string",
      "first_name": "string",
      "last_name": "string",
      "role": "owner|admin|manager|operator|viewer",
      "organization": {
        "id": "uuid",
        "name": "string",
        "slug": "string"
      }
    }
  }
}
```

**Errors:**

- `401 INVALID_CREDENTIALS` - Email ou mot de passe incorrect
- `403 ACCOUNT_LOCKED` - Compte verrouillé après trop de tentatives
- `403 EMAIL_NOT_VERIFIED` - Email non vérifié

---

### POST /auth/refresh

Renouvelle l'access token.

**Request:**

```json
{
  "refresh_token": "string (required)"
}
```

**Response: 200 OK**

```json
{
  "data": {
    "access_token": "string",
    "expires_in": 900
  }
}
```

**Errors:**

- `401 INVALID_TOKEN` - Refresh token invalide ou expiré

---

### POST /auth/logout

Révoque les tokens de l'utilisateur.

**Headers:** `Authorization: Bearer <access_token>`

**Response: 204 No Content**

---

### POST /auth/forgot-password

Envoie un email de réinitialisation de mot de passe.

**Request:**

```json
{
  "email": "string (required)"
}
```

**Response: 200 OK**

```json
{
  "data": {
    "message": "Password reset email sent"
  }
}
```

---

### POST /auth/reset-password

Réinitialise le mot de passe.

**Request:**

```json
{
  "token": "string (required)",
  "password": "string (required, min 8 chars)",
  "password_confirmation": "string (required)"
}
```

**Response: 200 OK**

```json
{
  "data": {
    "message": "Password reset successful"
  }
}
```

---

### POST /auth/invite/accept

Accepte une invitation avec OTP et crée le compte utilisateur.

**Request:**

```json
{
  "email": "string (required)",
  "otp": "string (required, 6 digits)",
  "password": "string (required, min 8 chars)",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

**Response: 200 OK**

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "Bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "role": "operator",
    "organization": {
      "id": "uuid",
      "name": "string",
      "slug": "string"
    }
  }
}
```

**Errors:**

- `401 INVALID_OTP` - OTP invalide ou expiré
- `400 EMAIL_EXISTS` - L'email existe déjà

---

## 5. ENDPOINTS - USER (Organisation Users)

### GET /organizations/me

Retourne l'organisation de l'utilisateur connecté.

**Headers:** `Authorization: Bearer <access_token>`

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "name": "Acme Corp",
    "slug": "acme-corp",
    "plan": "growth",
    "limits": {
      "leads": 2000,
      "campaigns": 10,
      "users": 10
    },
    "usage": {
      "leads_this_month": 450,
      "campaigns_active": 3,
      "users_count": 5
    },
    "settings": {
      "dark_mode": true,
      "timezone": "Europe/Paris",
      "language": "fr",
      "bant_threshold": 60,
      "email_daily_limit": 50
    },
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

---

### PATCH /organizations/me

Met à jour les paramètres de l'organisation.

**Headers:** `Authorization: Bearer <access_token>`  
**Permissions:** `owner`, `admin`

**Request:**

```json
{
  "name": "string (optional)",
  "settings": {
    "dark_mode": "boolean (optional)",
    "timezone": "string (optional)",
    "language": "string (optional)",
    "bant_threshold": "integer 0-100 (optional)",
    "email_daily_limit": "integer (optional)"
  }
}
```

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "name": "Updated Name",
    "settings": { ... },
    "updated_at": "2026-01-14T10:30:00Z"
  }
}
```

---

## 6. ENDPOINTS - USERS

### GET /users

Liste les utilisateurs de l'organisation.

**Headers:** `Authorization: Bearer <access_token>`  
**Permissions:** `owner`, `admin`, `manager`

**Query Parameters:**

- `role` - Filtrer par rôle
- `search` - Recherche par nom ou email

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "operator",
      "avatar_url": "https://...",
      "last_login_at": "2026-01-14T09:00:00Z",
      "created_at": "2026-01-01T00:00:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

### POST /users

Crée un nouvel utilisateur (invitation).

**Headers:** `Authorization: Bearer <access_token>`  
**Permissions:** `owner`, `admin`

**Request:**

```json
{
  "email": "string (required)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "role": "admin|manager|operator|viewer (required)"
}
```

**Response: 201 Created**

```json
{
  "data": {
    "id": "uuid",
    "email": "newuser@example.com",
    "role": "operator",
    "invitation_sent": true,
    "created_at": "2026-01-14T10:30:00Z"
  }
}
```

---

### GET /users/{id}

Retourne un utilisateur spécifique.

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "operator",
    "permissions": {
      "can_create_campaigns": true,
      "can_approve_emails": true,
      "can_view_billing": false
    },
    "preferences": {
      "dark_mode": true,
      "notifications_email": true
    },
    "last_login_at": "2026-01-14T09:00:00Z",
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

---

### PATCH /users/{id}

Met à jour un utilisateur.

**Permissions:** `owner`, `admin` (ou soi-même pour certains champs)

**Request:**

```json
{
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "role": "string (optional, owner/admin only)",
  "permissions": { ... },
  "preferences": { ... }
}
```

---

### DELETE /users/{id}

Supprime (désactive) un utilisateur.

**Permissions:** `owner`, `admin`

**Response: 204 No Content**

---

## 6. ENDPOINTS - ADMIN (Platform Admin)

**Préfixe:** `/api/v1/admin`  
**Authentification:** Requise (JWT Bearer token)  
**Permissions:** `PLATFORM_ADMIN` uniquement

### GET /admin/overview

Retourne les statistiques globales de la plateforme.

**Headers:** `Authorization: Bearer <access_token>`

**Response: 200 OK**

```json
{
  "total_organizations": 150,
  "total_users": 1250,
  "total_campaigns": 340,
  "total_leads": 12500,
  "active_campaigns": 120,
  "organizations_by_plan": {
    "starter": 50,
    "growth": 70,
    "scale": 25,
    "enterprise": 5
  }
}
```

---

### GET /admin/organizations

Liste toutes les organisations de la plateforme.

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**

- `skip` - Nombre d'éléments à sauter (default: 0)
- `limit` - Nombre d'éléments à retourner (default: 100, max: 100)
- `plan` - Filtrer par plan (`starter`, `growth`, `scale`, `enterprise`)

**Response: 200 OK**

```json
[
  {
    "id": "uuid",
    "name": "Acme Corp",
    "slug": "acme-corp",
    "plan": "growth",
    "settings": { ... },
    "user_count": 5,
    "campaign_count": 3,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-14T10:30:00Z"
  }
]
```

---

### GET /admin/organizations/{org_id}

Retourne les détails d'une organisation.

**Response: 200 OK**

```json
{
  "id": "uuid",
  "name": "Acme Corp",
  "slug": "acme-corp",
  "plan": "growth",
  "settings": { ... },
  "user_count": 5,
  "campaign_count": 3,
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-14T10:30:00Z"
}
```

---

### POST /admin/organizations

Crée une nouvelle organisation.

**Request:**

```json
{
  "name": "string (required)",
  "plan": "starter|growth|scale|enterprise (required)",
  "settings": {
    "timezone": "string (optional)",
    "language": "string (optional)",
    "bant_threshold": "integer (optional)",
    "email_daily_limit": "integer (optional)"
  }
}
```

**Response: 201 Created**

```json
{
  "id": "uuid",
  "name": "New Organization",
  "slug": "new-organization",
  "plan": "starter",
  "settings": { ... },
  "user_count": 0,
  "campaign_count": 0,
  "created_at": "2026-01-14T10:30:00Z",
  "updated_at": "2026-01-14T10:30:00Z"
}
```

---

### PATCH /admin/organizations/{org_id}

Met à jour une organisation.

**Request:**

```json
{
  "name": "string (optional)",
  "plan": "starter|growth|scale|enterprise (optional)",
  "settings": { ... }
}
```

**Response: 200 OK**

```json
{
  "id": "uuid",
  "name": "Updated Name",
  "slug": "acme-corp",
  "plan": "scale",
  "settings": { ... },
  ...
}
```

---

### DELETE /admin/organizations/{org_id}

Supprime une organisation (hard delete).

**Response: 204 No Content**

---

### GET /admin/users

Liste tous les utilisateurs de la plateforme.

**Query Parameters:**

- `skip` - Nombre d'éléments à sauter (default: 0)
- `limit` - Nombre d'éléments à retourner (default: 100, max: 100)
- `organization_id` - Filtrer par organisation
- `role` - Filtrer par rôle
- `is_active` - Filtrer par statut actif

**Response: 200 OK**

```json
[
  {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "owner",
    "organization_id": "uuid",
    "organization_name": "Acme Corp",
    "is_active": true,
    "email_verified_at": "2026-01-01T00:00:00Z",
    "last_login_at": "2026-01-14T09:00:00Z",
    "created_at": "2026-01-01T00:00:00Z"
  }
]
```

**Note:** Les platform admins (`organization_id: null`) sont également inclus.

---

### GET /admin/system/metrics

Retourne les métriques système (performance, latence, erreurs).

**Response: 200 OK**

```json
{
  "api_latency_ms": 125.5,
  "database_latency_ms": 45.2,
  "error_rate": 0.05,
  "requests_per_minute": 450,
  "active_connections": 23,
  "memory_usage_mb": 512,
  "cpu_usage_percent": 35.2
}
```

---

### POST /admin/notifications/send

Envoie une notification (platform admin).

**Request:**

```json
{
  "type": "vectra_to_users|vectra_to_org_owner|system_alerts (required)",
  "recipients": ["email1@example.com", "email2@example.com"],
  "subject": "string (required)",
  "body": "string (optional)",
  "body_html": "string (optional)",
  "action_url": "string (optional)",
  "action_text": "string (optional)"
}
```

**Response: 200 OK**

```json
{
  "id": "uuid",
  "type": "vectra_to_users",
  "recipients_count": 1250,
  "sent_at": "2026-01-14T10:30:00Z"
}
```

---

## 7. ENDPOINTS - CAMPAIGNS

**Préfixe:** `/api/v1/user/campaigns`  
**Authentification:** Requise (JWT Bearer token)

### GET /user/campaigns

Liste les campagnes de l'organisation.

**Query Parameters:**

- `status` - Filtrer par statut (`draft`, `active`, `paused`, `completed`)
- `created_by` - Filtrer par créateur (user_id)
- `search` - Recherche par nom

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": "uuid",
      "name": "VP Sales France Q1",
      "description": "Campagne ciblant les VP Sales...",
      "status": "active",
      "target_criteria": {
        "job_titles": ["VP Sales", "Director of Sales"],
        "locations": ["France"],
        "company_sizes": ["50-200"]
      },
      "bant_threshold": 60,
      "stats": {
        "leads_found": 245,
        "leads_qualified": 98,
        "emails_sent": 75,
        "emails_opened": 32,
        "meetings_booked": 8
      },
      "created_by": {
        "id": "uuid",
        "name": "John Doe"
      },
      "started_at": "2026-01-10T00:00:00Z",
      "created_at": "2026-01-05T00:00:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

### POST /user/campaigns

Crée une nouvelle campagne.

**Permissions:** `owner`, `admin`, `manager`, `operator` (si permission)

**Request:**

```json
{
  "name": "string (required, max 255)",
  "description": "string (optional)",
  "target_criteria": {
    "job_titles": ["string"],
    "industries": ["string"],
    "company_sizes": ["string"],
    "locations": ["string"],
    "keywords": ["string"]
  },
  "bant_threshold": "integer 0-100 (optional, default 60)",
  "bant_criteria": {
    "budget_weight": "integer 0-100",
    "authority_weight": "integer 0-100",
    "need_weight": "integer 0-100",
    "timeline_weight": "integer 0-100"
  },
  "email_template": "string (optional)",
  "email_subject": "string (optional)",
  "email_from_name": "string (optional)",
  "calendly_link": "string URL (optional)",
  "meeting_duration": "integer minutes (optional, default 30)",
  "available_days": "[1,2,3,4,5] (optional)",
  "available_hours": {
    "start": "HH:MM",
    "end": "HH:MM"
  },
  "daily_email_limit": "integer (optional, default 50)",
  "total_leads_target": "integer (optional)"
}
```

**Response: 201 Created**

```json
{
  "data": {
    "id": "uuid",
    "name": "New Campaign",
    "status": "draft",
    ...
  }
}
```

---

### GET /user/campaigns/{id}

Retourne les détails d'une campagne.

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "name": "VP Sales France Q1",
    "description": "...",
    "status": "active",
    "target_criteria": { ... },
    "bant_threshold": 60,
    "bant_criteria": { ... },
    "email_template": "...",
    "email_subject": "...",
    "calendly_link": "https://calendly.com/...",
    "meeting_duration": 30,
    "available_days": [1,2,3,4,5],
    "available_hours": { "start": "09:00", "end": "18:00" },
    "daily_email_limit": 50,
    "total_leads_target": 500,
    "stats": {
      "leads_found": 245,
      "leads_qualified": 98,
      "leads_contacted": 75,
      "leads_responded": 25,
      "emails_sent": 75,
      "emails_opened": 32,
      "emails_clicked": 18,
      "meetings_booked": 8,
      "meetings_completed": 5
    },
    "created_by": { ... },
    "started_at": "2026-01-10T00:00:00Z",
    "paused_at": null,
    "completed_at": null,
    "created_at": "2026-01-05T00:00:00Z",
    "updated_at": "2026-01-14T10:00:00Z"
  }
}
```

---

### PATCH /user/campaigns/{id}

Met à jour une campagne (seulement en statut DRAFT).

**Request:** (mêmes champs que POST, tous optionnels)

**Errors:**

- `400 INVALID_STATUS` - Ne peut modifier que les campagnes en DRAFT

---

### POST /user/campaigns/{id}/launch

Lance une campagne (passe de `draft` ou `paused` à `active`).

**Permissions:** `owner`, `admin`, `manager`

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "status": "active",
    "started_at": "2026-01-14T10:30:00Z"
  }
}
```

**Errors:**

- `400 INVALID_STATUS` - La campagne n'est pas en draft ou paused
- `400 MISSING_CONFIGURATION` - Configuration incomplète (email_template, etc.)

---

### POST /user/campaigns/{id}/pause

Met en pause une campagne active.

**Response: 200 OK**

```json
{
  "id": "uuid",
  "status": "paused",
  "paused_at": "2026-01-14T10:30:00Z"
}
```

---

### POST /user/campaigns/{id}/resume

Reprend une campagne en pause.

**Response: 200 OK**

```json
{
  "id": "uuid",
  "status": "active",
  "resumed_at": "2026-01-14T10:30:00Z"
}
```

---

### DELETE /user/campaigns/{id}

Supprime (soft delete) une campagne.

**Permissions:** `owner`, `admin`

**Response: 204 No Content**

---

## 8. ENDPOINTS - LEADS

### GET /leads

Liste les leads.

**Query Parameters:**

- `campaign_id` - Filtrer par campagne (required ou all)
- `status` - Filtrer par statut
- `intent` - Filtrer par intent
- `bant_score_min` - Score BANT minimum
- `bant_score_max` - Score BANT maximum
- `email_status` - Filtrer par statut email
- `search` - Recherche par nom, email, entreprise
- `created_after` - Créés après cette date
- `created_before` - Créés avant cette date

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": "uuid",
      "campaign_id": "uuid",
      "email": "prospect@company.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "phone": "+33612345678",
      "linkedin_url": "https://linkedin.com/in/janesmith",
      "company": {
        "name": "Tech Corp",
        "domain": "techcorp.com",
        "size": "50-200",
        "industry": "SaaS",
        "location": "Paris, France"
      },
      "job": {
        "title": "VP Sales",
        "department": "Sales",
        "seniority": "VP"
      },
      "bant": {
        "score": 75,
        "budget": 20,
        "authority": 22,
        "need": 18,
        "timeline": 15,
        "notes": "Budget confirmé, décideur identifié"
      },
      "intent": "interested_now",
      "intent_confidence": 0.85,
      "status": "qualified",
      "email_status": "sent",
      "email_sent_at": "2026-01-12T14:00:00Z",
      "email_opened_at": "2026-01-12T15:30:00Z",
      "enriched_at": "2026-01-10T10:00:00Z",
      "qualified_at": "2026-01-11T09:00:00Z",
      "created_at": "2026-01-10T08:00:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

### GET /leads/{id}

Retourne les détails complets d'un lead.

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    ... // Tous les champs du lead
    "interactions": [
      {
        "id": "uuid",
        "type": "bant_scored",
        "agent_type": "bant",
        "data": { ... },
        "created_at": "2026-01-11T09:00:00Z"
      },
      {
        "id": "uuid",
        "type": "email_sent",
        "data": {
          "subject": "...",
          "body_preview": "..."
        },
        "created_at": "2026-01-12T14:00:00Z"
      }
    ],
    "emails": [
      {
        "id": "uuid",
        "subject": "...",
        "status": "sent",
        "sent_at": "...",
        "opened_count": 2
      }
    ],
    "meetings": [
      {
        "id": "uuid",
        "scheduled_at": "2026-01-20T10:00:00Z",
        "status": "scheduled"
      }
    ]
  }
}
```

---

### GET /leads/{id}/interactions

Retourne l'historique des interactions d'un lead.

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": "uuid",
      "type": "prospector_found",
      "agent_type": "prospector",
      "data": {
        "source": "rocketreach",
        "confidence": 0.95
      },
      "created_at": "2026-01-10T08:00:00Z"
    },
    {
      "id": "uuid",
      "type": "bant_scored",
      "agent_type": "bant",
      "data": {
        "score": 75,
        "budget": 20,
        "authority": 22,
        "need": 18,
        "timeline": 15
      },
      "created_at": "2026-01-11T09:00:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

### PATCH /leads/{id}

Met à jour un lead (manuel).

**Request:**

```json
{
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "phone": "string (optional)",
  "company_name": "string (optional)",
  "job_title": "string (optional)",
  "status": "string (optional)",
  "notes": "string (optional)"
}
```

---

## 9. ENDPOINTS - EMAILS

### GET /emails

Liste les emails.

**Query Parameters:**

- `campaign_id` - Filtrer par campagne
- `lead_id` - Filtrer par lead
- `status` - Filtrer par statut (`pending`, `approved`, `rejected`, `sent`, `failed`)

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": "uuid",
      "lead_id": "uuid",
      "campaign_id": "uuid",
      "lead": {
        "email": "prospect@company.com",
        "name": "Jane Smith",
        "company": "Tech Corp"
      },
      "subject": "Quick question about your sales process",
      "body_preview": "Hi Jane, I noticed Tech Corp has been...",
      "status": "pending",
      "generated_by": "scheduler",
      "created_at": "2026-01-14T08:00:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

### GET /emails/{id}

Retourne les détails complets d'un email.

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "lead_id": "uuid",
    "campaign_id": "uuid",
    "subject": "Quick question about your sales process",
    "body_html": "<p>Hi Jane,</p><p>I noticed Tech Corp...</p>",
    "body_text": "Hi Jane,\n\nI noticed Tech Corp...",
    "from_email": "john@company.com",
    "from_name": "John Doe",
    "to_email": "prospect@company.com",
    "status": "sent",
    "generated_by": "scheduler",
    "generation_model": "llama2-70b",
    "approved_by": {
      "id": "uuid",
      "name": "John Doe"
    },
    "approved_at": "2026-01-14T09:00:00Z",
    "sent_at": "2026-01-14T10:00:00Z",
    "tracking": {
      "opened_count": 2,
      "first_opened_at": "2026-01-14T11:30:00Z",
      "last_opened_at": "2026-01-14T15:00:00Z",
      "clicked_count": 1,
      "first_clicked_at": "2026-01-14T11:35:00Z"
    },
    "created_at": "2026-01-14T08:00:00Z"
  }
}
```

---

### POST /emails/{id}/approve

Approuve un email pour envoi.

**Permissions:** `owner`, `admin`, `manager`, `operator` (si permission)

**Request:**

```json
{
  "modifications": {
    "subject": "string (optional, pour modifier)",
    "body_html": "string (optional, pour modifier)"
  }
}
```

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "status": "approved",
    "approved_at": "2026-01-14T10:30:00Z",
    "scheduled_send_at": "2026-01-14T11:00:00Z"
  }
}
```

---

### POST /emails/{id}/reject

Rejette un email.

**Request:**

```json
{
  "reason": "string (required)"
}
```

**Response: 200 OK**

```json
{
  "data": {
    "id": "uuid",
    "status": "rejected",
    "rejection_reason": "Tonalité inappropriée"
  }
}
```

---

### POST /emails/{id}/regenerate

Demande une nouvelle génération de l'email.

**Request:**

```json
{
  "instructions": "string (optional, instructions pour la nouvelle génération)"
}
```

**Response: 202 Accepted**

```json
{
  "data": {
    "id": "uuid",
    "status": "pending",
    "message": "Email regeneration queued"
  }
}
```

---

## 10. ENDPOINTS - MEETINGS

### GET /meetings

Liste les meetings.

**Query Parameters:**

- `campaign_id` - Filtrer par campagne
- `lead_id` - Filtrer par lead
- `status` - Filtrer par statut
- `scheduled_after` - Planifiés après cette date
- `scheduled_before` - Planifiés avant cette date

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": "uuid",
      "lead_id": "uuid",
      "campaign_id": "uuid",
      "lead": {
        "name": "Jane Smith",
        "company": "Tech Corp",
        "email": "jane@techcorp.com"
      },
      "scheduled_at": "2026-01-20T10:00:00Z",
      "duration_minutes": 30,
      "timezone": "Europe/Paris",
      "location": {
        "type": "zoom",
        "url": "https://zoom.us/j/123456789"
      },
      "host": {
        "email": "john@company.com",
        "name": "John Doe"
      },
      "status": "scheduled",
      "created_at": "2026-01-14T11:00:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

### GET /meetings/{id}

Retourne les détails d'un meeting.

---

### PATCH /meetings/{id}

Met à jour un meeting (notes, outcome).

**Request:**

```json
{
  "status": "completed|cancelled|noshow (optional)",
  "outcome": "qualified|not_qualified|follow_up|closed_won|closed_lost (optional)",
  "notes": "string (optional)",
  "cancellation_reason": "string (optional, si cancelled)"
}
```

---

## 11. ENDPOINTS - ANALYTICS

### GET /analytics/dashboard

Retourne les métriques du dashboard.

**Query Parameters:**

- `campaign_id` - Filtrer par campagne (optional, sinon toutes)
- `period` - `today`, `7d`, `30d`, `90d`, `all` (default: `30d`)

**Response: 200 OK**

```json
{
  "data": {
    "period": {
      "start": "2025-12-15T00:00:00Z",
      "end": "2026-01-14T23:59:59Z"
    },
    "summary": {
      "leads_found": 1250,
      "leads_qualified": 485,
      "leads_contacted": 320,
      "emails_sent": 320,
      "emails_opened": 145,
      "emails_clicked": 78,
      "meetings_booked": 32,
      "meetings_completed": 25
    },
    "rates": {
      "qualification_rate": 38.8,
      "open_rate": 45.3,
      "click_rate": 24.4,
      "meeting_rate": 10.0,
      "show_rate": 78.1
    },
    "trends": {
      "leads_found": [
        { "date": "2025-12-15", "value": 45 },
        { "date": "2025-12-16", "value": 52 },
        ...
      ],
      "meetings_booked": [ ... ]
    },
    "top_campaigns": [
      {
        "id": "uuid",
        "name": "VP Sales France",
        "meetings_booked": 12,
        "conversion_rate": 15.4
      }
    ]
  }
}
```

---

### GET /analytics/campaigns/{id}

Retourne les analytics détaillées d'une campagne.

---

### GET /analytics/agents

Retourne les métriques des agents IA.

**Response: 200 OK**

```json
{
  "data": {
    "prospector": {
      "jobs_completed": 150,
      "jobs_failed": 3,
      "success_rate": 98.0,
      "avg_duration_ms": 2500,
      "leads_found": 1250,
      "cost_usd": 12.50
    },
    "bant": {
      "jobs_completed": 1250,
      "jobs_failed": 5,
      "success_rate": 99.6,
      "avg_duration_ms": 3200,
      "avg_score": 52.3,
      "qualification_rate": 38.8,
      "cost_usd": 45.00
    },
    "scheduler": {
      "jobs_completed": 320,
      "jobs_failed": 2,
      "success_rate": 99.4,
      "avg_duration_ms": 4500,
      "emails_generated": 320,
      "cost_usd": 18.00
    }
  }
}
```

---

## 12. WEBHOOKS

### GET /webhooks

Liste les webhooks configurés.

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": "uuid",
      "url": "https://example.com/webhook",
      "events": ["lead.qualified", "meeting.scheduled"],
      "active": true,
      "secret": "whsec_****abcd",
      "created_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

---

### POST /webhooks

Crée un nouveau webhook.

**Request:**

```json
{
  "url": "string URL (required)",
  "events": ["string"] // Liste des événements
}
```

**Événements disponibles:**

- `lead.created`
- `lead.enriched`
- `lead.qualified`
- `lead.contacted`
- `email.sent`
- `email.opened`
- `email.clicked`
- `email.replied`
- `meeting.scheduled`
- `meeting.completed`
- `meeting.cancelled`
- `campaign.started`
- `campaign.paused`
- `campaign.completed`

**Response: 201 Created**

```json
{
  "data": {
    "id": "uuid",
    "url": "https://example.com/webhook",
    "events": ["lead.qualified", "meeting.scheduled"],
    "active": true,
    "secret": "whsec_1234567890abcdef"
  }
}
```

---

### DELETE /webhooks/{id}

Supprime un webhook.

**Response: 204 No Content**

---

### Payload des Webhooks

Tous les webhooks envoient un payload avec cette structure:

```json
{
  "id": "evt_uuid",
  "type": "lead.qualified",
  "created_at": "2026-01-14T10:30:00Z",
  "data": {
    // Données de l'objet concerné
  }
}
```

**Headers envoyés:**

- `X-Vectra-Signature`: HMAC-SHA256 du body avec le secret
- `X-Vectra-Event`: Type d'événement
- `X-Vectra-Delivery`: ID unique de la livraison

---

## 13. SCHEMAS

### Organization

```json
{
  "id": "uuid",
  "name": "string",
  "slug": "string",
  "plan": "starter|growth|scale|enterprise",
  "limits": {
    "leads": "integer",
    "campaigns": "integer",
    "users": "integer"
  },
  "usage": {
    "leads_this_month": "integer",
    "campaigns_active": "integer",
    "users_count": "integer"
  },
  "settings": {
    "dark_mode": "boolean",
    "timezone": "string",
    "language": "string",
    "bant_threshold": "integer",
    "email_daily_limit": "integer"
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### User

```json
{
  "id": "uuid",
  "organization_id": "uuid",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "owner|admin|manager|operator|viewer",
  "avatar_url": "string",
  "permissions": "object",
  "preferences": "object",
  "last_login_at": "datetime",
  "created_at": "datetime"
}
```

### Campaign

```json
{
  "id": "uuid",
  "organization_id": "uuid",
  "name": "string",
  "description": "string",
  "status": "draft|pending|active|paused|completed|cancelled",
  "target_criteria": "object",
  "bant_threshold": "integer",
  "bant_criteria": "object",
  "email_template": "string",
  "email_subject": "string",
  "calendly_link": "string",
  "meeting_duration": "integer",
  "daily_email_limit": "integer",
  "stats": "object",
  "created_by": "uuid",
  "started_at": "datetime",
  "created_at": "datetime"
}
```

### Lead

```json
{
  "id": "uuid",
  "campaign_id": "uuid",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "linkedin_url": "string",
  "company_name": "string",
  "company_domain": "string",
  "company_size": "string",
  "company_industry": "string",
  "job_title": "string",
  "seniority_level": "string",
  "bant_score": "integer",
  "bant_budget": "integer",
  "bant_authority": "integer",
  "bant_need": "integer",
  "bant_timeline": "integer",
  "intent": "string",
  "status": "string",
  "email_status": "string",
  "created_at": "datetime"
}
```

---

## 14. CODES D'ERREUR

### Codes HTTP

| Code | Signification |
|------|---------------|
| 200 | OK - Requête réussie |
| 201 | Created - Ressource créée |
| 204 | No Content - Suppression réussie |
| 400 | Bad Request - Requête invalide |
| 401 | Unauthorized - Non authentifié |
| 403 | Forbidden - Non autorisé |
| 404 | Not Found - Ressource non trouvée |
| 409 | Conflict - Conflit (ex: doublon) |
| 422 | Unprocessable Entity - Validation échouée |
| 429 | Too Many Requests - Rate limit atteint |
| 500 | Internal Server Error - Erreur serveur |

### Codes d'erreur applicatifs

| Code | Description |
|------|-------------|
| `INVALID_CREDENTIALS` | Email ou mot de passe incorrect |
| `ACCOUNT_LOCKED` | Compte verrouillé |
| `EMAIL_NOT_VERIFIED` | Email non vérifié |
| `INVALID_TOKEN` | Token invalide ou expiré |
| `VALIDATION_ERROR` | Erreur de validation des données |
| `RESOURCE_NOT_FOUND` | Ressource non trouvée |
| `PERMISSION_DENIED` | Permission refusée |
| `RATE_LIMIT_EXCEEDED` | Limite de requêtes dépassée |
| `QUOTA_EXCEEDED` | Quota du plan dépassé |
| `DUPLICATE_RESOURCE` | Ressource déjà existante |
| `INVALID_STATUS` | Transition de statut invalide |
| `MISSING_CONFIGURATION` | Configuration incomplète |

---

## 15. RATE LIMITING

### Limites par défaut

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| Authentication | 10 req | 1 minute |
| API (général) | 100 req | 1 minute |
| Webhooks | 1000 req | 1 minute |
| Analytics | 30 req | 1 minute |

### Headers de réponse

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705234800
```

### Réponse 429

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please retry after 45 seconds.",
    "retry_after": 45
  }
}
```

---

**- FIN DU DOCUMENT -**

*Document prêt pour implémentation*  
*14 Janvier 2026*
