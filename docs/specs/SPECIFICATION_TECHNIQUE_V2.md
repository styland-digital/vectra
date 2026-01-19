# VECTRA - SPECIFICATION TECHNIQUE V2
## Document de Spécification Technique Complet
### Version 2.0 | 14 Janvier 2026

---

**Statut**: APPROUVÉ POUR DÉVELOPPEMENT
**Équipe**: 2 Développeurs + 1 PM
**Timeline**: 12 semaines (6 sprints × 2 semaines)

---

## 1. RÉSUMÉ EXÉCUTIF

### 1.1 Vision
Vectra est une plateforme SaaS B2B d'agents IA autonomes qui automatise le cycle de vente complet : prospection, qualification BANT, et prise de rendez-vous qualifiés. L'objectif est de réduire le CAC de 35-45% tout en augmentant le volume de leads de 120%.

### 1.2 Proposition de Valeur
- Automatisation complète du pipeline de prospection
- Qualification BANT intelligente avec scoring 0-100
- Prise de rendez-vous automatisée via Calendly
- ROI client : 6-9 mois (le plus rapide du marché)
- TCO < $3,000/mois pour PME SaaS

### 1.3 Décisions Techniques Verrouillées

| Composant | Décision |
|-----------|----------|
| Framework Agents | CrewAI - Multi-agent orchestration native |
| LLM Principal | Llama 2 70B - Open-source, $0 coût inference |
| LLM Fallback | Claude API - Si qualité française insuffisante |
| Backend | Python 3.11 + FastAPI |
| Frontend | Next.js 14 + Tailwind + Shadcn/ui |
| Database | PostgreSQL + pgvector |
| Queue | Celery + Redis |
| Hosting | Render (backend) + Vercel (frontend) |

---

## 2. ARCHITECTURE SYSTÈME

### 2.1 Vue d'Ensemble

L'architecture repose sur 3 blocs fonctionnels orchestrés par un state machine :

| Bloc | Fonction | Exécution | Latence |
|------|----------|-----------|---------|
| Agent Prospector | Recherche de leads | ASYNCHRONE | Minutes/heures |
| Agent BANT | Qualification | SYNCHRONE | < 30 sec/lead |
| Agent Scheduler | Prise de RDV | ASYNCHRONE | Envoi + attente |

### 2.2 State Machine

Flow de données strict pour éviter les deadlocks :
1. Prospector recherche et enrichit les prospects
2. BANT qualifie et score chaque prospect (0-100)
3. Si score ≥ 60 : création d'une tâche de contact
4. Scheduler génère l'email personnalisé et envoie
5. Tracking des métriques (ouvertures, clics, RDVs)

### 2.3 Multi-Tenant

Architecture SaaS multi-entreprise avec isolation stricte :
- **Platform Admin (Vectra)** : vue globale, monitoring système
- **Organization** : chaque entreprise cliente isolée
- **Rôles** : Owner → Admin → Manager → Operator → Viewer

---

## 3. SPÉCIFICATION DES AGENTS

### 3.1 Agent Prospector

**Responsabilités :**
- Rechercher selon critères (métiers, géo, taille)
- Enrichir via RocketReach API
- Vérifier doublons
- Scorer par priorité firmographique
- Transmettre au BANT

**Métriques de succès :**
| Métrique | Cible |
|----------|-------|
| Prospects trouvés/jour | 100-150 |
| Taux d'enrichissement | > 85% |
| Coût par prospect | < $0.50 |
| Taux de doublons | < 2% |

### 3.2 Agent BANT

**Framework de scoring :**

| Critère | Question clé | Points | Seuil |
|---------|-------------|--------|-------|
| Budget | Taille entreprise > 50? | 0-25 | > 15 |
| Authority | Manager/VP/C-level? | 0-25 | > 15 |
| Need | Indicateurs de besoin? | 0-25 | > 10 |
| Timeline | Activité récente? | 0-25 | > 10 |

**Règle** : Score ≥ 60 = Contact | 40-60 = Nurture | < 40 = Reject

### 3.3 Agent Scheduler

**Responsabilités :**
- Générer email personnalisé (sujet + corps + contexte)
- Value prop claire en 1 ligne
- CTA avec proposition de créneau
- Envoyer via SendGrid avec tracking
- Créer lien Calendly pré-rempli
- Logger l'envoi

### 3.4 Module Détection d'Intent

| Intent | Description | Action |
|--------|-------------|--------|
| INTERESTED_NOW | Intérêt explicite | BANT + RDV |
| INTERESTED_LATER | Pas maintenant | Nurture 60j |
| OBJECTION_PRICE | Objection prix | Escalade humain |
| REQUEST_INFO | Demande de docs | Auto-réponse |
| POLITE_DECLINE | Refus poli | Archive |
| SPAM/BOUNCE | Email invalide | Blacklist |

---

## 4. MODÈLE DE DONNÉES

### Tables Principales

```
organizations
├── users
├── campaigns
│   ├── leads
│   │   ├── emails
│   │   └── meetings
│   └── agent_runs
├── subscriptions
├── usage_records
└── integrations
```

### Relations Clés

- `organizations` 1:N `users`
- `organizations` 1:N `campaigns`
- `campaigns` 1:N `leads`
- `leads` 1:N `emails`
- `leads` 1:1 `meetings`

---

## 5. SPÉCIFICATIONS API

### 5.1 Authentification
- JWT avec refresh token
- Access token : 15 min
- Refresh token : 7 jours

### 5.2 Endpoints Principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/auth/register | Inscription |
| POST | /api/v1/auth/login | Connexion |
| GET | /api/v1/campaigns | Liste campagnes |
| POST | /api/v1/campaigns | Créer campagne |
| POST | /api/v1/campaigns/{id}/launch | Lancer |
| GET | /api/v1/leads | Liste leads |
| PATCH | /api/v1/emails/{id}/approve | Approuver email |

### 5.3 Latence Cibles

| Endpoint | P50 | P99 |
|----------|-----|-----|
| GET /campaigns | < 100ms | < 300ms |
| GET /leads | < 150ms | < 500ms |
| Dashboard metrics | < 200ms | < 800ms |

---

## 6. INTERFACE UTILISATEUR

### 6.1 Design Tokens

**Couleurs :**
| Token | Valeur | Usage |
|-------|--------|-------|
| primary.500 | #2E5BFF | Actions principales |
| accent.500 | #FF9F43 | Accent (parcimonieux) |
| bg.dark | #0E1117 | Background dark mode |
| state.success | #22C55E | Succès/Validation |
| state.error | #EF4444 | Erreur/Alerte |

**Spacing** : Système 8px (4/8/12/16/24/32/48/64)

### 6.2 Écrans MVP

1. **Dashboard** : Stats, actions rapides, activité récente
2. **Campaign Setup** : Wizard 5 étapes
3. **Email Review** : Queue d'approbation
4. **Performance Tracker** : Métriques et graphiques

---

## 7. INTÉGRATIONS

### 7.1 MVP

| Service | Usage | Sprint |
|---------|-------|--------|
| RocketReach | Enrichissement | Sprint 2 |
| SendGrid | Envoi emails | Sprint 3 |
| Calendly | Booking RDV | Sprint 3 |
| HubSpot | CRM sync | Sprint 5 |

### 7.2 Rate Limiting Intelligent

Scheduler adaptatif pour optimiser les quotas API :
- Priorisation prospects à score élevé
- Répartition sur créneaux à meilleur taux d'ouverture
- Impact : +10-15% d'efficacité

---

## 8. SÉCURITÉ

### 8.1 Authentification
- JWT avec refresh tokens
- Password hashing : bcrypt (cost 12)
- RBAC strict

### 8.2 Protection des Données
- Chiffrement at-rest : AES-256
- Chiffrement in-transit : TLS 1.3
- Isolation multi-tenant stricte
- Audit logs

### 8.3 Conformité
- RGPD ready
- CAN-SPAM / CASL
- OWASP Top 10 (audit semaine 10)

---

## 9. OBSERVABILITÉ

### 9.1 Stack
- Tracing : OpenTelemetry + Jaeger
- Métriques : Prometheus + Grafana
- Logs : ELK stack
- Alerting : PagerDuty

### 9.2 Métriques Clés

| Métrique | Seuil Normal | Alerte |
|----------|--------------|--------|
| Latence BANT (P50) | < 5s | > 15s |
| Taux d'échec agents | < 2% | > 5% |
| Queue depth | < 500 | > 1000 |
| Coût LLM/lead | < $0.30 | > $0.50 |
| Uptime | > 99.5% | < 99% |

---

## 10. PLAN DE DÉPLOIEMENT

### Timeline (12 semaines)

| Sprint | Semaines | Objectif | SP |
|--------|----------|----------|-----|
| 1 | 1-2 | Foundation & Architecture | 12 |
| 2 | 3-4 | Agent Prospector + CrewAI | 16 |
| 3 | 5-6 | Agent BANT + State Machine | 14 |
| 4 | 7-8 | Frontend MVP + Dashboard | 12 |
| 5 | 9-10 | Intégrations + Polish | 10 |
| 6 | 11-12 | Beta Launch Prep | 8 |

**Total** : 72 Story Points

### Go-Live Requirements
- 3 agents fonctionnels
- 100+ prospects/campagne
- 50%+ accuracy BANT
- Audit OWASP passé
- 10-15 beta users
- NPS > 50

---

## 11. MÉTRIQUES & KPIs

### Produit

| Métrique | Cible MVP | Cible V1.1 |
|----------|-----------|------------|
| Leads générés/mois | 300-500 | 500-1000 |
| Taux qualification | 40-50% | 50-60% |
| Taux ouverture | 35-45% | 45-55% |
| Meetings bookés | 8-12 | 15-25 |
| Coût/meeting | < $150 | < $100 |

### Business

| Métrique | Mois 6 | Mois 12 |
|----------|--------|---------|
| MRR | $20-40K | $75K+ |
| Clients | 5-10 | 15-25 |
| Churn | < 5% | < 3% |
| NPS | > 50 | > 60 |

---

## 12. GESTION DES RISQUES

| Risque | Proba | Impact | Mitigation |
|--------|-------|--------|------------|
| Qualité LLM français | 80% | ÉLEVÉ | Test S3, fallback Claude |
| Orchestration multi-agent | 60% | ÉLEVÉ | State machine + chaos testing |
| Rate limiting APIs | 70% | MOYEN | Exponential backoff |
| Churn élevé | 40% | ÉLEVÉ | Playbook qualification + onboarding |

### Points Go/No-Go

**Semaine 6** :
- Agent BANT accuracy > 50%
- State machine stable (0 deadlock)
- Latence BANT < 30s P95

**Semaine 10** :
- NPS beta > 40
- 3+ clients POC positifs
- Audit OWASP passé

---

*Document approuvé pour développement*
*14 Janvier 2026*
