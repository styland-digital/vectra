# VECTRA - ORCHESTRATION DU WORKFLOW

## Guide Complet pour le Développement de Features

### Version 1.0 | 15 Janvier 2026

---

**Document:** WORKFLOW-001  
**Statut:** RÉFÉRENCE OBLIGATOIRE  
**Usage:** Suivre ce workflow pour TOUTE nouvelle feature, composant, ou modification

---

## 🎯 PRINCIPE FONDAMENTAL

**Chaque modification doit être documentée dans `/docs/workflow/logs/` pour garder une trace complète de l'activité.**

---

## 📋 WORKFLOW COMPLET

### Phase 1 : PLANIFICATION

#### 1.1 Identifier le Type de Travail

| Type | Dossier Log | Document de Référence |
|------|-------------|----------------------|
| **Feature** | `logs/features/` | `docs/specs/REALISATION_TECHNIQUE.md` |
| **Component** | `logs/components/` | `docs/ui/DOC-UI-002_COMPONENTS_CATALOG.md` |
| **API Endpoint** | `logs/api/` | `docs/tech/DOC-TECH-002_API_CONTRACTS.md` |
| **Agent IA** | `logs/agents/` | `docs/tech/DOC-TECH-004_AGENT_PROMPTS.md` |
| **Database** | `logs/database/` | `docs/tech/DOC-TECH-001_DATABASE_SCHEMA.md` |
| **Fix/Bug** | `logs/fixes/` | - |
| **Test** | `logs/tests/` | `docs/tech/DOC-TECH-006_TEST_PLAN.md` |

#### 1.2 Créer le Log d'Activité

**Format de nommage :** `YYYY-MM-DD_<type>_<nom>.md`

Exemples :

- `2026-01-15_feature_campaign-wizard.md`
- `2026-01-15_component_lead-card.md`
- `2026-01-15_api_campaigns-endpoints.md`
- `2026-01-15_agent_bant-qualifier.md`
- `2026-01-15_database_add-lead-enrichment.md`
- `2026-01-15_fix_celery-startup.md`
- `2026-01-15_test_bant-service.md`

**Template de log :**

```markdown
# [TYPE] - [NOM]

**Date:** YYYY-MM-DD  
**Statut:** in_progress | completed | blocked  
**Priorité:** P0 | P1 | P2

## Objectif

[Description claire de ce qui est créé/modifié]

## Références

- Doc technique: `docs/...`
- Issue/Ticket: #XXX
- PR: #XXX

## Étapes Réalisées

### 1. [Étape 1]
- [x] Fait
- [ ] À faire

### 2. [Étape 2]
- [ ] À faire

## Fichiers Créés/Modifiés

- `backend/app/...`
- `frontend/components/...`

## Tests

- [ ] Tests unitaires créés
- [ ] Tests d'intégration créés
- [ ] Tests E2E créés (si applicable)
- [ ] Coverage atteint

## Notes

[Notes importantes, décisions, problèmes rencontrés]

## Prochaines Étapes

1. [Action 1]
2. [Action 2]
```

---

## 🔄 WORKFLOW PAR TYPE

### WORKFLOW : Feature Complète

#### Étape 1 : Analyse & Design

1. Lire les specs dans `docs/specs/`
2. Identifier les composants nécessaires
3. Identifier les endpoints API nécessaires
4. Identifier les modèles DB nécessaires
5. Créer le log : `docs/workflow/logs/features/YYYY-MM-DD_feature_<nom>.md`

#### Étape 2 : Backend

1. Créer/modifier les models DB (si nécessaire)
   - Créer migration : `/create-migration msg="add_<field>"`
   - Documenter dans log
2. Créer les repositories
   - Documenter dans log
3. Créer les services
   - Documenter dans log
4. Créer les schemas Pydantic
   - Documenter dans log
5. Créer les endpoints API
   - Utiliser `/create-endpoint <nom>`
   - Documenter dans log
6. Écrire les tests
   - Utiliser `/write-test integration-api <nom>`
   - Utiliser `/write-test unit-service <nom>`
   - Documenter dans log

#### Étape 3 : Frontend

1. Créer les types TypeScript
   - Documenter dans log
2. Créer les composants UI
   - Utiliser `/create-component <nom>`
   - Documenter dans log
3. Créer les pages (si nécessaire)
   - Utiliser `/create-page <path>`
   - Documenter dans log
4. Créer les hooks (si nécessaire)
   - Documenter dans log
5. Écrire les tests
   - Utiliser `/write-test component <nom>`
   - Documenter dans log

#### Étape 4 : Intégration

1. Connecter frontend ↔ backend
2. Tester le flow complet
3. Écrire tests E2E (si applicable)
   - Utiliser `/write-test e2e <scenario>`
   - Documenter dans log

#### Étape 5 : Documentation

1. Mettre à jour le log avec statut `completed`
2. Mettre à jour `docs/workflow/STATUS.md`
3. Créer/actualiser la documentation utilisateur si nécessaire

---

### WORKFLOW : Composant React

#### Étape 1 : Analyse

1. Consulter `docs/ui/DOC-UI-002_COMPONENTS_CATALOG.md`
2. Identifier le design system à utiliser
3. Créer le log : `docs/workflow/logs/components/YYYY-MM-DD_component_<nom>.md`

#### Étape 2 : Création

1. Créer le composant
   - Utiliser `/create-component <nom>`
   - Suivre les conventions TypeScript
   - Utiliser les tokens du design system
2. Créer les types TypeScript
3. Ajouter les props avec validation Zod (si nécessaire)

#### Étape 3 : Tests

1. Écrire les tests
   - Utiliser `/write-test component <nom>`
   - Coverage cible : 70%

#### Étape 4 : Documentation

1. Mettre à jour le log
2. Mettre à jour `docs/workflow/STATUS.md`
3. Ajouter au catalog si composant réutilisable

---

### WORKFLOW : Endpoint API

#### Étape 1 : Analyse

1. Consulter `docs/tech/DOC-TECH-002_API_CONTRACTS.md`
2. Identifier le schéma de requête/réponse
3. Créer le log : `docs/workflow/logs/api/YYYY-MM-DD_api_<nom>.md`

#### Étape 2 : Création

1. Créer le schema Pydantic
2. Créer l'endpoint
   - Utiliser `/create-endpoint <nom>`
   - Vérifier l'isolation multi-tenant
   - Ajouter la validation
3. Créer le service (si nécessaire)
4. Créer le repository (si nécessaire)

#### Étape 3 : Tests

1. Tests unitaires du service
   - Utiliser `/write-test unit-service <nom>`
2. Tests d'intégration API
   - Utiliser `/write-test integration-api <nom>`
   - Tester l'isolation multi-tenant
   - Coverage cible : 80%

#### Étape 4 : Documentation

1. Mettre à jour le log
2. Mettre à jour `docs/workflow/STATUS.md`
3. Mettre à jour `docs/tech/DOC-TECH-002_API_CONTRACTS.md` si nouveau endpoint

---

### WORKFLOW : Agent IA

#### Étape 1 : Analyse

1. Consulter `docs/tech/DOC-TECH-004_AGENT_PROMPTS.md`
2. Identifier le prompt système
3. Créer le log : `docs/workflow/logs/agents/YYYY-MM-DD_agent_<nom>.md`

#### Étape 2 : Création

1. Créer l'agent
   - Utiliser `/create-agent <nom>`
   - Implémenter le prompt depuis la doc
2. Créer la task Celery (si async)
3. Créer le service wrapper (si nécessaire)

#### Étape 3 : Tests

1. Tests unitaires de l'agent
   - Utiliser `/write-test unit-agent <nom>`
   - Mock du LLM
   - Tests de fallback
   - Coverage cible : 85%

#### Étape 4 : Documentation

1. Mettre à jour le log
2. Mettre à jour `docs/workflow/STATUS.md`
3. Documenter les prompts dans `docs/tech/DOC-TECH-004_AGENT_PROMPTS.md`

---

### WORKFLOW : Modification Base de Données

#### Étape 1 : Analyse

1. Consulter `docs/tech/DOC-TECH-001_DATABASE_SCHEMA.md`
2. Identifier les tables/colonnes à modifier
3. Créer le log : `docs/workflow/logs/database/YYYY-MM-DD_database_<nom>.md`

#### Étape 2 : Création

1. Créer la migration
   - Utiliser `/create-migration msg="<description>"`
2. Mettre à jour les models SQLAlchemy
3. Mettre à jour les repositories (si nécessaire)
4. Mettre à jour les schemas Pydantic (si nécessaire)

#### Étape 3 : Tests

1. Tests de migration
2. Tests d'intégration DB
   - Utiliser `/write-test integration-db <nom>`

#### Étape 4 : Documentation

1. Mettre à jour le log
2. Mettre à jour `docs/workflow/STATUS.md`
3. Mettre à jour `docs/tech/DOC-TECH-001_DATABASE_SCHEMA.md`

---

### WORKFLOW : Fix/Bug

#### Étape 1 : Analyse

1. Identifier le problème
2. Créer le log : `docs/workflow/logs/fixes/YYYY-MM-DD_fix_<nom>.md`

#### Étape 2 : Correction

1. Corriger le code
2. Écrire un test de régression
   - Utiliser `/write-test <type> <nom>`
3. Vérifier que les tests existants passent

#### Étape 3 : Documentation

1. Mettre à jour le log avec la cause et la solution
2. Mettre à jour `docs/workflow/STATUS.md`

---

## 📝 COMMANDES CLAUDE DISPONIBLES

### Création

- `/create-agent <nom>` - Créer un agent IA
- `/create-endpoint <nom>` - Créer un endpoint API
- `/create-component <nom>` - Créer un composant React
- `/create-page <path>` - Créer une page Next.js
- `/create-migration msg="<description>"` - Créer une migration DB

### Tests

- `/write-test <type> <target>` - Écrire des tests
  - Types : `unit-service`, `unit-agent`, `integration-api`, `component`, `e2e`
- `/run-tests [scope]` - Lancer les tests

### Autres

- `/deploy [env]` - Déployer
- `/debug <type>` - Aide au debugging

---

## 📊 MISE À JOUR DU STATUT

Après chaque étape importante, mettre à jour `docs/workflow/STATUS.md` :

```markdown
## [Date] - [Type] - [Nom]

**Statut:** in_progress | completed  
**Fichier log:** `logs/<type>/YYYY-MM-DD_<type>_<nom>.md`

### Résumé
[Description courte]

### Fichiers Modifiés
- `backend/app/...`
- `frontend/components/...`

### Tests
- Coverage: XX%
- Tests passent: ✅ | ❌
```

---

## ✅ CHECKLIST FINALE

Avant de considérer une feature comme terminée :

- [ ] Code écrit et fonctionnel
- [ ] Tests écrits et passent
- [ ] Coverage atteint (voir seuils)
- [ ] Linting OK (`make lint`)
- [ ] Documentation mise à jour
- [ ] Log d'activité complété
- [ ] `STATUS.md` mis à jour
- [ ] Review de code (si applicable)

---

## 🎯 ORDRE D'EXÉCUTION RECOMMANDÉ

1. **Créer le log d'activité** (dans le bon dossier)
2. **Analyser les docs de référence**
3. **Créer le code** (backend → frontend)
4. **Écrire les tests** (`/write-test`)
5. **Tester localement** (`/run-tests`)
6. **Mettre à jour la documentation**
7. **Mettre à jour le log et STATUS.md**

---

**Règle d'or :** Toujours créer le log AVANT de commencer à coder.

---

*Dernière mise à jour : 15 Janvier 2026*
