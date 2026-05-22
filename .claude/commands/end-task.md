# /end-task

Clôture la session de travail en cours selon le workflow Vectra.

---

## Instructions pour Claude

Quand `/end-task` est invoqué :

### 1. Trouver le log actif

Scanner `docs/workflow/logs/**/*.md` pour un fichier contenant `Statut: in_progress`.

- Si **aucun log trouvé** : afficher "Aucun log in_progress trouvé. Utilisez /start-task pour démarrer une session." et s'arrêter.

### 2. Demander un résumé à l'utilisateur

"Résumé des changements effectués pour le log [nom du log] ?"

### 3. Mettre à jour le log

Editer le fichier log :
- `Statut: in_progress` → `Statut: completed`
- Remplir / compléter la section "Fichiers Créés/Modifiés" avec les fichiers réellement touchés
- Cocher les items complétés dans "Étapes Réalisées"
- Remplir "Prochaines Étapes" si applicable

### 4. Mettre à jour STATUS.md

Ouvrir `docs/workflow/STATUS.md` et ajouter une nouvelle ligne dans le tableau d'activité en haut du fichier :

```
| YYYY-MM-DD | TYPE | NOM | completed | `chemin/du/log.md` | Résumé en une phrase |
```

### 5. Confirmer

Afficher : "Session clôturée — [nom du log] marqué completed, STATUS.md mis à jour."
