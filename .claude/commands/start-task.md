# /start-task

Démarre une nouvelle session de travail selon le workflow Vectra.

## Usage
```
/start-task <type> <nom>
```

Types valides : `feature` | `component` | `api` | `agent` | `database` | `fix` | `test`

---

## Instructions pour Claude

Quand `/start-task <type> <nom>` est invoqué :

### 1. Déterminer le chemin du log
- Date du jour au format `YYYY-MM-DD`
- Chemin : `docs/workflow/logs/<type>s/YYYY-MM-DD_<type>_<nom>.md`
  - Exception : `fix` → dossier `fixes/`, `feature` → `features/`, `component` → `components/`, etc.

### 2. Créer le fichier log avec ce template exact

```markdown
# [TYPE en majuscules] - [NOM]

**Date:** YYYY-MM-DD
**Statut:** in_progress
**Priorité:** P1

## Objectif

[Décrire brièvement ce qui est créé/modifié]

## Références

- Branche: `feature/...`
- Doc technique: `docs/...`

## Étapes Réalisées

### 1. [Première étape]
- [ ] À faire

## Fichiers Créés/Modifiés

- (à remplir au fur et à mesure)

## Tests

- [ ] Tests unitaires créés
- [ ] Tests d'intégration créés
- [ ] Coverage atteint

## Notes

(notes au fur et à mesure)

## Prochaines Étapes

1. (à définir)
```

### 3. Activer le skill correspondant

| Type | Skill à activer |
|------|----------------|
| `feature`, `api`, `fix`, `database` | `vectra-patterns` |
| `component` | `vectra-ui-components` |
| `agent` | `crewai-agents` |
| `test` | aucun |

Invoque le skill avec le Skill tool.

### 4. Confirmer à l'utilisateur

Afficher :
- Chemin du log créé
- Skill activé
- Rappel : "Documentez chaque fichier modifié dans le log au fur et à mesure"
