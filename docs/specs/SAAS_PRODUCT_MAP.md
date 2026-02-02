# VECTRA — SAAS PRODUCT MAP
## Multi-Tenant · B2B · Enterprise-Ready
### Architecture SaaS Officielle

---

## 1️⃣ ARCHITECTURE GLOBALE

```
Vectra SaaS
│
├─ Platform (Vectra Core)
│   ├─ Global Admin
│   ├─ Billing global
│   ├─ Monitoring global
│   └─ Sécurité & conformité
│
├─ Organizations (Entreprises clientes)
│   ├─ Organization A
│   ├─ Organization B
│   └─ Organization N
│
└─ Users
    ├─ Platform Users
    └─ Organization Users
```

👉 **Vectra contrôle tout.**
👉 Les entreprises n'ont accès qu'à **leur périmètre**.

---

## 2️⃣ MODÈLE MULTI-TENANT

### Entité centrale : Organization

Chaque entreprise = **Organization**

Une Organization possède :
- Ses utilisateurs
- Ses campagnes
- Ses leads
- Ses intégrations
- Sa facturation
- Ses métriques

❌ Aucune donnée partagée entre orgs
✔ Isolation stricte

---

## 3️⃣ SYSTÈME DE RÔLES

### 🔥 Platform Admin (Vectra Admin)

Rôle interne Vectra. Au-dessus de TOUT.

**Pouvoirs:**
- Voir toutes les organizations
- Créer / suspendre / supprimer une org
- Accéder aux métriques globales
- Gérer la facturation globale
- Gérer les plans
- Accéder aux logs système
- Monitoring IA & performances
- Support niveau 3

> Ce rôle n'appartient à aucune entreprise.

### 🏢 Rôles Organization

| Rôle | Accès | Restrictions |
|------|-------|--------------|
| **Owner** | Total | Responsable légal & billing |
| **Admin** | Opérations | Pas accès billing |
| **Manager** | Supervision | Pas modification settings |
| **Operator** | Exécution | Pas accès analytics |
| **Viewer** | Lecture seule | Aucune action |

---

## 4️⃣ MAP DES PAGES

### 🔐 Auth & Access
- Login
- Password reset
- SSO (Enterprise)
- 2FA

### 🌍 Platform Admin (/platform)
```
/platform
├─ Overview (global)
├─ Organizations
│   ├─ List
│   └─ Org detail
├─ Users (platform)
├─ Plans & Billing
├─ System Monitoring
│   ├─ Jobs IA
│   ├─ Queues
│   ├─ Errors
│   └─ Uptime
├─ Logs & Audit
└─ Settings
```

### 🏢 Organization Dashboard (/org/:id)
```
/org/:id
├─ Overview
├─ Campaigns
│   ├─ All campaigns
│   ├─ Create campaign
│   └─ Campaign detail
├─ Leads
│   ├─ Inbox
│   └─ Lead detail
├─ Meetings
├─ Analytics
├─ Integrations
├─ Team
├─ Billing
└─ Settings
```

---

## 5️⃣ MONITORING & CONTROL

### Platform Level
- Nombre total d'orgs
- Jobs IA actifs
- Échecs / retries
- Temps moyen d'exécution
- SLA

### Org Level
- Campagnes actives
- Leads qualifiés
- Meetings bookés
- Taux de réponse
- Consommation quota

---

## 6️⃣ BILLING & PLANS

- Plan par Organization
- Limites: campagnes, leads, intégrations
- Upgrade / downgrade
- Paiement centralisé
- Invoice par org

---

## 7️⃣ SÉCURITÉ & CONFORMITÉ

- RBAC strict
- Audit logs
- Data isolation
- Rate limiting
- Permissions explicites
- RGPD / SOC2 ready

---

## 8️⃣ ALIGNEMENT MARQUE

✔ Calme
✔ Maîtrisé
✔ Silencieux
✔ Orienté résultats

> **Vectra ne montre pas la complexité. Il la contrôle.**

---

**🔒 MAP SAAS VECTRA — VALIDÉE**
