# Guide de Mise à Jour - Collection Postman (2026-01-19)

## 📋 Résumé des Changements

La collection Postman doit être mise à jour pour inclure **27 nouveaux endpoints** :

- **1 nouveau endpoint Auth** : `/auth/invite/accept`
- **9 endpoints User** : `/user/*` (organisations, utilisateurs)
- **9 endpoints Admin** : `/admin/*` (platform admin)
- **9 endpoints Campaigns** : `/user/campaigns/*`

---

## 🔧 Structure à Ajouter

### 1. Auth - Nouveau Endpoint

Ajouter dans le dossier `Auth` existant :

#### Accept Invitation (OTP)
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/invite/accept`
- **Body:**
```json
{
    "email": "{{test_email}}",
    "otp": "123456",
    "password": "password123",
    "first_name": "New",
    "last_name": "User"
}
```
- **Response:** 200 - `LoginResponse` (access_token, refresh_token, user)
- **Tests:** Sauvegarder tokens comme dans Login

---

### 2. User - Nouvelle Section

Créer un nouveau dossier `User` avec 9 endpoints :

#### GET /user/me
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/user/me`
- **Auth:** Bearer {{access_token}}
- **Response:** 200 - User profile

#### GET /user/organizations/me
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/user/organizations/me`
- **Auth:** Bearer {{access_token}}
- **Response:** 200 - OrganizationResponse

#### PATCH /user/organizations/me
- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/user/organizations/me`
- **Auth:** Bearer {{access_token}}
- **Body:**
```json
{
    "name": "Updated Organization Name",
    "settings": {
        "timezone": "Europe/Paris",
        "bant_threshold": 65
    }
}
```

#### GET /user/organizations/me/users
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/user/organizations/me/users?skip=0&limit=100`
- **Auth:** Bearer {{access_token}}
- **Response:** 200 - List[OrganizationUserResponse]

#### POST /user/organizations/me/users/invite
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/user/organizations/me/users/invite`
- **Auth:** Bearer {{access_token}}
- **Body:**
```json
{
    "email": "newuser@example.com",
    "role": "operator",
    "first_name": "New",
    "last_name": "User"
}
```
- **Response:** 200 - MessageResponse

#### POST /user/organizations/me/users/create
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/user/organizations/me/users/create`
- **Auth:** Bearer {{access_token}}
- **Body:**
```json
{
    "email": "direct@example.com",
    "role": "operator",
    "password": "password123",
    "first_name": "Direct",
    "last_name": "User",
    "send_welcome_email": true
}
```
- **Response:** 201 - OrganizationUserResponse

#### PATCH /user/organizations/me/users/{user_id}/role
- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/user/organizations/me/users/{{user_id}}/role`
- **Auth:** Bearer {{access_token}}
- **Body:**
```json
{
    "role": "admin"
}
```

#### DELETE /user/organizations/me/users/{user_id}
- **Method:** DELETE
- **URL:** `{{base_url}}/api/v1/user/organizations/me/users/{{user_id}}`
- **Auth:** Bearer {{access_token}}
- **Response:** 204

#### POST /user/notifications/send
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/user/notifications/send`
- **Auth:** Bearer {{access_token}}
- **Body:**
```json
{
    "type": "org_to_prospects",
    "recipients": ["email1@example.com", "email2@example.com"],
    "subject": "Test Notification",
    "body": "Test body",
    "body_html": "<p>Test HTML</p>"
}
```

---

### 3. Admin - Nouvelle Section

Créer un nouveau dossier `Admin` avec 9 endpoints :

#### GET /admin/overview
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/admin/overview`
- **Auth:** Bearer {{platform_admin_token}}
- **Response:** 200 - PlatformOverviewResponse

#### GET /admin/organizations
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/admin/organizations?skip=0&limit=100&plan=growth`
- **Auth:** Bearer {{platform_admin_token}}

#### GET /admin/organizations/{org_id}
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/admin/organizations/{{organization_id}}`
- **Auth:** Bearer {{platform_admin_token}}

#### POST /admin/organizations
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/admin/organizations`
- **Auth:** Bearer {{platform_admin_token}}
- **Body:**
```json
{
    "name": "New Organization",
    "plan": "starter",
    "settings": {}
}
```

#### PATCH /admin/organizations/{org_id}
- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/admin/organizations/{{organization_id}}`
- **Auth:** Bearer {{platform_admin_token}}
- **Body:**
```json
{
    "plan": "scale",
    "settings": {}
}
```

#### DELETE /admin/organizations/{org_id}
- **Method:** DELETE
- **URL:** `{{base_url}}/api/v1/admin/organizations/{{organization_id}}`
- **Auth:** Bearer {{platform_admin_token}}
- **Response:** 204

#### GET /admin/users
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/admin/users?skip=0&limit=100&organization_id={{organization_id}}`
- **Auth:** Bearer {{platform_admin_token}}

#### GET /admin/system/metrics
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/admin/system/metrics`
- **Auth:** Bearer {{platform_admin_token}}

#### POST /admin/notifications/send
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/admin/notifications/send`
- **Auth:** Bearer {{platform_admin_token}}
- **Body:**
```json
{
    "type": "vectra_to_users",
    "recipients": [],
    "subject": "Platform Notification",
    "body": "Test notification"
}
```

---

### 4. Campaigns - Nouvelle Section

Créer un nouveau dossier `Campaigns` sous `User` ou à la racine, avec 9 endpoints :

#### GET /user/campaigns
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/user/campaigns?status=active&skip=0&limit=100`
- **Auth:** Bearer {{access_token}}

#### POST /user/campaigns
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/user/campaigns`
- **Auth:** Bearer {{access_token}}
- **Body:**
```json
{
    "name": "Q1 Sales Campaign",
    "description": "Campaign targeting VP Sales",
    "target_criteria": {
        "job_titles": ["VP Sales"],
        "locations": ["France"]
    },
    "bant_threshold": 60
}
```

#### GET /user/campaigns/{campaign_id}
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/user/campaigns/{{campaign_id}}`
- **Auth:** Bearer {{access_token}}

#### PATCH /user/campaigns/{campaign_id}
- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/user/campaigns/{{campaign_id}}`
- **Auth:** Bearer {{access_token}}
- **Body:** (mêmes champs que POST, tous optionnels)

#### POST /user/campaigns/{campaign_id}/launch
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/user/campaigns/{{campaign_id}}/launch`
- **Auth:** Bearer {{access_token}}
- **Response:** 200 - CampaignResponse

#### POST /user/campaigns/{campaign_id}/pause
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/user/campaigns/{{campaign_id}}/pause`
- **Auth:** Bearer {{access_token}}

#### POST /user/campaigns/{campaign_id}/resume
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/user/campaigns/{{campaign_id}}/resume`
- **Auth:** Bearer {{access_token}}

#### DELETE /user/campaigns/{campaign_id}
- **Method:** DELETE
- **URL:** `{{base_url}}/api/v1/user/campaigns/{{campaign_id}}`
- **Auth:** Bearer {{access_token}}
- **Response:** 204

#### GET /user/campaigns/{campaign_id}/stats
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/user/campaigns/{{campaign_id}}/stats`
- **Auth:** Bearer {{access_token}}
- **Response:** 200 - CampaignStatsResponse

---

## 🔐 Variables d'Environnement à Ajouter

Dans `Vectra_Local_Environment.json`, ajouter :

```json
{
    "key": "platform_admin_token",
    "value": "",
    "type": "default",
    "enabled": true
},
{
    "key": "campaign_id",
    "value": "",
    "type": "default",
    "enabled": true
},
{
    "key": "verification_otp",
    "value": "",
    "type": "default",
    "enabled": true
}
```

---

## ✅ Checklist de Mise à Jour

- [ ] Ajouter endpoint `/auth/invite/accept`
- [ ] Créer dossier `User` avec 9 endpoints
- [ ] Créer dossier `Admin` avec 9 endpoints
- [ ] Créer dossier `Campaigns` avec 9 endpoints
- [ ] Mettre à jour variables d'environnement
- [ ] Ajouter tests automatiques pour chaque endpoint
- [ ] Vérifier que les tokens sont sauvegardés automatiquement
- [ ] Exporter et sauvegarder la collection mise à jour

---

## 📝 Notes

- Tous les endpoints `/user/*` nécessitent un `access_token` normal (utilisateur organisation)
- Tous les endpoints `/admin/*` nécessitent un `platform_admin_token` (PLATFORM_ADMIN)
- Les variables `{{user_id}}`, `{{campaign_id}}`, `{{organization_id}}` doivent être sauvegardées automatiquement après création/récupération

---

**Date de mise à jour:** 2026-01-19  
**Version collection:** 2.0
