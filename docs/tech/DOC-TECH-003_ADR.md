# VECTRA - ARCHITECTURE DECISION RECORDS (ADR)
## Registre des Décisions d'Architecture
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-004  
**Statut:** APPROUVÉ  
**Objectif:** Documenter les décisions techniques clés et leur rationale  

---

## TABLE DES MATIERES

1. Introduction
2. ADR-001: Framework Multi-Agent (CrewAI)
3. ADR-002: Modèle LLM Principal (Llama 2 70B)
4. ADR-003: Pattern State Machine
5. ADR-004: Architecture Multi-Tenant
6. ADR-005: Queue Architecture (Celery + Redis)
7. ADR-006: Base de Données (PostgreSQL)
8. ADR-007: Frontend Framework (Next.js)
9. ADR-008: Hosting Strategy (Render + Vercel)
10. ADR-009: Authentication (JWT)
11. ADR-010: Observability Stack

---

## 1. INTRODUCTION

### 1.1 Objectif des ADR

Les Architecture Decision Records (ADR) documentent les décisions techniques significatives prises durant le développement de Vectra. Chaque ADR capture:

- Le contexte de la décision
- Les options considérées
- La décision prise et sa justification
- Les conséquences attendues
- Les risques et mitigations

### 1.2 Format Standard

Chaque ADR suit ce format:
- **Statut:** Proposé | Approuvé | Déprécié | Remplacé par ADR-XXX
- **Date:** Date de la décision
- **Décideurs:** Personnes impliquées
- **Contexte:** Problème à résoudre
- **Options:** Alternatives considérées
- **Décision:** Choix final
- **Conséquences:** Impact positif et négatif
- **Risques:** Risques identifiés et mitigations

---

## 2. ADR-001: FRAMEWORK MULTI-AGENT

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead, CTO

### Contexte

Vectra nécessite l'orchestration de 3+ agents IA autonomes (Prospector, BANT, Scheduler) qui doivent:
- Communiquer entre eux
- Partager un contexte commun
- Être orchestrés de manière fiable
- Gérer les erreurs et retries

### Options Considérées

#### Option A: CrewAI
- **Pour:** Multi-agent orchestration native, mémoire partagée, tools intégrés, production-ready
- **Contre:** Moins flexible que custom, abstraction peut limiter
- **Effort:** 1-2 jours d'intégration

#### Option B: LangGraph
- **Pour:** Flexibilité maximale, graphes de workflows complexes
- **Contre:** Courbe d'apprentissage plus longue, plus de boilerplate
- **Effort:** 3-5 jours d'intégration

#### Option C: Solution Custom
- **Pour:** Contrôle total, pas de dépendance externe
- **Contre:** Beaucoup de code à écrire, plus de bugs potentiels
- **Effort:** 7-10 jours

### Décision

**CrewAI** est retenu comme framework multi-agent.

### Justification

1. **Time-to-market:** 40% plus rapide que custom
2. **Fiabilité:** Framework mature et testé en production
3. **Features:** Agent delegation, memory, tools management inclus
4. **Équipe:** Plus facile à prendre en main pour l'équipe existante

### Conséquences

**Positives:**
- Démarrage rapide du développement
- Moins de code à maintenir
- Patterns établis pour l'orchestration

**Négatives:**
- Dépendance à une librairie tierce
- Moins de flexibilité pour cas edge
- Migration potentiellement coûteuse si abandon de CrewAI

### Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| CrewAI ne répond pas aux besoins spécifiques | 30% | Moyen | Évaluation semaine 2, pivot possible vers LangGraph |
| Breaking changes dans CrewAI | 20% | Faible | Pin de version, tests de régression |
| Performance insuffisante | 15% | Moyen | Benchmarks semaine 3, optimisation si nécessaire |

### Date de Revue: Semaine 2 (Janvier 2026)

---

## 3. ADR-002: MODÈLE LLM PRINCIPAL

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead, CTO

### Contexte

Les agents Vectra nécessitent un LLM pour:
- Génération d'emails personnalisés (français)
- Scoring BANT (raisonnement)
- Classification d'intent
- Extraction d'informations

Contrainte majeure: Budget bootstrap ($0 initial pour LLM)

### Options Considérées

#### Option A: Llama 2 70B (Open-source)
- **Coût:** $0 (self-hosted)
- **Qualité:** 90% de GPT-3.5 pour notre use case
- **Hosting:** Render free tier ou local via Ollama
- **Risque:** Qualité française incertaine

#### Option B: Mistral 7B
- **Coût:** $0 (self-hosted)
- **Qualité:** Meilleur en français, plus rapide
- **Hosting:** Plus léger que Llama 70B
- **Risque:** Context window plus petit

#### Option C: Claude API (Anthropic)
- **Coût:** ~$0.01-0.03 par lead = $500-1500/mois à scale
- **Qualité:** Best-in-class pour raisonnement
- **Hosting:** Pas de gestion infra
- **Risque:** Coûts incompatibles avec bootstrap

#### Option D: GPT-4o Mini (OpenAI)
- **Coût:** $0.15/1M tokens input
- **Qualité:** Bon compromis
- **Risque:** Vendor lock-in

### Décision

**Llama 2 70B** comme LLM principal, avec **Claude API** en fallback (mois 4 si qualité française insuffisante).

### Justification

1. **Budget:** Compatible avec stratégie bootstrap ($0)
2. **Indépendance:** Pas de dépendance à un vendor
3. **Scalabilité:** Coûts prévisibles à mesure du scale
4. **Fallback:** Claude API disponible si besoin

### Plan d'Implémentation

| Phase | Action | Timeline |
|-------|--------|----------|
| 1 | Deploy Llama 2 70B via Ollama | Semaine 2 |
| 2 | Benchmark qualité française (20 emails test) | Semaine 3 |
| 3 | Fine-tuning si nécessaire | Mois 2-3 |
| 4 | Évaluation fallback Claude | Mois 4 |

### Conséquences

**Positives:**
- Coûts d'inférence à $0
- Pas de vendor lock-in
- Données restent privées (self-hosted)

**Négatives:**
- Qualité potentiellement inférieure
- Latence plus élevée (2-5s vs 0.5s)
- Gestion de l'infrastructure LLM

### Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Qualité française insuffisante | 80% | Élevé | Test semaine 3, fine-tuning mois 2-3, fallback Claude |
| Latence trop élevée | 40% | Moyen | Cache agressif, batching, GPU si budget |
| Hosting instable | 30% | Moyen | Monitoring, fallback API |

### Métriques de Succès

- Taux de réponse emails > 8%
- Temps de génération < 5s
- Score qualité humaine > 7/10 sur 20 tests

---

## 4. ADR-003: PATTERN STATE MACHINE

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead

### Contexte

Le flow de prospection suit une séquence stricte:
```
Prospector → BANT → (si qualifié) → Scheduler → Tracking
```

Problèmes à résoudre:
- Éviter les deadlocks entre agents
- Garantir l'intégrité des données
- Permettre le replay en cas d'erreur
- Tracer l'état de chaque lead

### Options Considérées

#### Option A: State Machine explicite
- États définis: NEW → ENRICHED → QUALIFIED → CONTACTED → ...
- Transitions validées par règles
- Historique des changements d'état

#### Option B: Event Sourcing
- Tous les événements sont stockés
- État reconstruit depuis les événements
- Plus flexible mais plus complexe

#### Option C: Simple flags
- Colonnes booléennes: is_enriched, is_qualified, is_contacted
- Simple mais risque d'incohérence

### Décision

**State Machine explicite** avec ENUM pour les états et table d'interactions pour l'historique.

### Justification

1. **Clarté:** États explicites et transitions définies
2. **Intégrité:** Impossible de sauter des étapes
3. **Debug:** Facile de comprendre où en est un lead
4. **Reporting:** Métriques par état simples à calculer

### Implémentation

```
États Lead:
NEW → ENRICHED → QUALIFIED → CONTACTED → RESPONDED → MEETING → CONVERTED
                    ↓                         ↓
                 REJECTED                  BOUNCED
```

**Transitions autorisées:**
| De | Vers | Condition |
|----|------|-----------|
| NEW | ENRICHED | Enrichissement terminé |
| ENRICHED | QUALIFIED | Score BANT > seuil |
| ENRICHED | REJECTED | Score BANT < seuil |
| QUALIFIED | CONTACTED | Email envoyé |
| CONTACTED | RESPONDED | Réponse reçue |
| CONTACTED | BOUNCED | Email bounce |
| RESPONDED | MEETING | RDV planifié |

### Conséquences

**Positives:**
- États clairs et prévisibles
- Facile à debugger
- Métriques précises

**Négatives:**
- Rigidité des transitions
- Migration si ajout d'états

---

## 5. ADR-004: ARCHITECTURE MULTI-TENANT

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead, CTO

### Contexte

Vectra est un SaaS B2B servant plusieurs entreprises (organizations). Chaque organization doit avoir:
- Isolation complète des données
- Gestion des utilisateurs propre
- Configuration spécifique
- Facturation séparée

### Options Considérées

#### Option A: Base de données partagée avec organization_id
- Une seule DB, chaque table a un `organization_id`
- Filtrage systématique par organization
- Le plus courant pour SaaS early-stage

#### Option B: Schéma par organization
- Un schéma PostgreSQL par organization
- Isolation plus forte
- Plus complexe à gérer

#### Option C: Base de données par organization
- Une DB complète par organization
- Isolation maximale
- Très coûteux en ressources

### Décision

**Base de données partagée avec organization_id** (Option A).

### Justification

1. **Simplicité:** Un seul schéma à maintenir
2. **Coût:** Une seule instance DB
3. **Suffisant:** Pour le volume prévu (10-25 orgs mois 12)
4. **Évolutif:** Migration vers schéma séparé possible plus tard

### Implémentation

**Règles d'isolation:**
- Toute table cliente a `organization_id` NOT NULL
- Toute requête inclut `WHERE organization_id = :current_org`
- Middleware API vérifie l'organization de l'utilisateur
- Index sur `(organization_id, ...)` pour performance

**Hiérarchie des rôles:**
```
Platform Admin (Vectra)
    └── Organization Owner
            └── Organization Admin
                    └── Manager
                            └── Operator
                                    └── Viewer
```

### Conséquences

**Positives:**
- Schéma simple
- Coûts réduits
- Maintenance simplifiée

**Négatives:**
- Risque de fuite de données si bug
- Performance si une org a beaucoup de données
- Moins d'isolation que schémas séparés

### Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Fuite de données cross-org | 10% | Critique | Tests automatisés, middleware strict, audit logs |
| Performance dégradée | 20% | Moyen | Index optimisés, monitoring, sharding si nécessaire |

---

## 6. ADR-005: QUEUE ARCHITECTURE

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead

### Contexte

Les agents Vectra effectuent des tâches asynchrones:
- Recherche de prospects (minutes)
- Enrichissement via API externes (secondes)
- Envoi d'emails (rate-limited)
- Génération LLM (secondes)

Besoins:
- Fiabilité (retry en cas d'échec)
- Priorité (leads à haut score d'abord)
- Rate limiting (respect des quotas API)
- Monitoring

### Options Considérées

#### Option A: Celery + Redis
- Standard Python pour task queues
- Redis comme broker (gratuit sur Render)
- Mature et bien documenté

#### Option B: RQ (Redis Queue)
- Plus simple que Celery
- Moins de features

#### Option C: AWS SQS
- Managed, scalable
- Coût AWS

### Décision

**Celery + Redis** pour la gestion des queues.

### Justification

1. **Maturité:** Solution éprouvée
2. **Features:** Retry, priorité, scheduling inclus
3. **Coût:** Redis gratuit sur free tier
4. **Monitoring:** Flower pour dashboard

### Implémentation

**Queues définies:**
| Queue | Usage | Priority | Rate Limit |
|-------|-------|----------|------------|
| `prospector` | Recherche leads | Normal | 100/heure |
| `enrichment` | RocketReach API | Normal | 50/minute |
| `bant` | Qualification LLM | High | - |
| `email` | Envoi SendGrid | Low | 50/jour/campaign |
| `scheduler` | Génération email | Normal | - |

**Retry Policy:**
```python
@celery.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    retry_backoff=True,
    retry_backoff_max=3600
)
```

### Conséquences

**Positives:**
- Traitement asynchrone fiable
- Rate limiting intégré
- Monitoring avec Flower

**Négatives:**
- Complexité de configuration
- Redis comme SPOF

---

## 7. ADR-006: BASE DE DONNÉES

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead

### Contexte

Vectra stocke des données structurées (leads, campaigns) et semi-structurées (enrichment data, settings).

### Décision

**PostgreSQL 15+** avec extensions:
- `pgvector` pour embeddings (future)
- `pg_trgm` pour recherche fuzzy
- JSONB pour données flexibles

### Justification

1. **Robustesse:** ACID, mature, fiable
2. **Features:** JSONB, extensions, full-text search
3. **Coût:** Free tier Render/Vercel
4. **Équipe:** Expertise existante

### Hosting

| Environnement | Provider | Tier |
|---------------|----------|------|
| Development | Local Docker | - |
| Staging | Render PostgreSQL | Free |
| Production | Render PostgreSQL | $7/mois puis scale |

---

## 8. ADR-007: FRONTEND FRAMEWORK

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead

### Contexte

Dashboard Vectra avec:
- Authentification
- Gestion campagnes
- Visualisation leads
- Métriques temps réel

### Options Considérées

#### Option A: Next.js 14
- React + SSR/SSG
- API routes intégrées
- Vercel deployment natif

#### Option B: Nuxt (Vue)
- Alternative Vue.js
- Moins de momentum

#### Option C: SvelteKit
- Performance maximale
- Communauté plus petite

### Décision

**Next.js 14** avec **Tailwind CSS** et **Shadcn/ui**.

### Justification

1. **Écosystème:** React dominant, plus de ressources
2. **Vercel:** Déploiement gratuit, optimisé
3. **Shadcn/ui:** Composants production-ready
4. **Mobile-first:** Tailwind responsive natif

---

## 9. ADR-008: HOSTING STRATEGY

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead, CTO

### Contexte

Stratégie bootstrap = maximiser free tiers.

### Décision

| Composant | Provider | Tier | Coût M1-3 | Coût M4-6 |
|-----------|----------|------|-----------|-----------|
| Backend API | Render | Free | $0 | $7/mois |
| Frontend | Vercel | Free | $0 | $0-20/mois |
| Database | Render PostgreSQL | Free | $0 | $7/mois |
| Redis | Render Redis | Free | $0 | $0 |
| LLM | Self-hosted (Ollama) | - | $0 | $0 |

**Total M1-3:** ~$0/mois  
**Total M4-6:** ~$15-35/mois

### Justification

1. **Bootstrap:** Maximise runway
2. **Scale:** Migration facile vers plans payants
3. **Simplicité:** Moins de vendors à gérer

---

## 10. ADR-009: AUTHENTICATION

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead

### Décision

**JWT (JSON Web Tokens)** avec:
- Access token: 15 minutes
- Refresh token: 7 jours
- Stockage: httpOnly cookies (web) / secure storage (mobile)
- Hash: bcrypt cost 12

### Justification

1. **Stateless:** Scalable horizontalement
2. **Standard:** Bien compris, librairies matures
3. **Sécurité:** Rotation fréquente des access tokens

### Implémentation

```
Login → Access Token (15min) + Refresh Token (7d)
       ↓
API Request → Validate Access Token
       ↓ (expiré)
Refresh → New Access Token
       ↓ (refresh expiré)
Re-login required
```

---

## 11. ADR-010: OBSERVABILITY STACK

### Statut: APPROUVÉ
### Date: 05 Janvier 2026
### Décideurs: Tech Lead

### Décision

| Fonction | Outil | Coût |
|----------|-------|------|
| Tracing | OpenTelemetry + Jaeger | $0 (self-hosted) |
| Métriques | Prometheus + Grafana | $0 (self-hosted) |
| Logs | Loki (ou ELK) | $0 |
| Alerting | Grafana Alerts | $0 |
| Uptime | BetterUptime free tier | $0 |

### Justification

1. **Standards:** OpenTelemetry = futur standard
2. **Coût:** Tout open-source
3. **Intégration:** Stack cohérente

### Métriques Clés à Monitorer

| Métrique | Seuil Normal | Alerte |
|----------|--------------|--------|
| API latency P50 | < 200ms | > 500ms |
| API latency P99 | < 1s | > 3s |
| Agent BANT latency | < 5s | > 15s |
| Error rate | < 1% | > 5% |
| Queue depth | < 500 | > 1000 |

---

## ANNEXE: REGISTRE DES ADR

| ADR | Titre | Statut | Date |
|-----|-------|--------|------|
| 001 | Framework Multi-Agent | Approuvé | 05/01/2026 |
| 002 | Modèle LLM Principal | Approuvé | 05/01/2026 |
| 003 | Pattern State Machine | Approuvé | 05/01/2026 |
| 004 | Architecture Multi-Tenant | Approuvé | 05/01/2026 |
| 005 | Queue Architecture | Approuvé | 05/01/2026 |
| 006 | Base de Données | Approuvé | 05/01/2026 |
| 007 | Frontend Framework | Approuvé | 05/01/2026 |
| 008 | Hosting Strategy | Approuvé | 05/01/2026 |
| 009 | Authentication | Approuvé | 05/01/2026 |
| 010 | Observability Stack | Approuvé | 05/01/2026 |
| 011 | Service d'Envoi d'Emails (Resend) | Approuvé | 15/01/2026 |

---

**- FIN DU DOCUMENT -**

*Toute nouvelle décision architecturale majeure doit être documentée dans un ADR.*

*14 Janvier 2026*
