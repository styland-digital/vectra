# VECTRA - WORKFLOW & LOGS

## 📁 Structure

```
docs/workflow/
├── WORKFLOW_ORCHESTRATION.md  # Guide principal du workflow
├── STATUS.md                  # État général (à mettre à jour)
├── README.md                  # Ce fichier
└── logs/                      # Logs d'activités
    ├── features/              # Nouvelles features
    ├── components/            # Composants React
    ├── api/                   # Endpoints API
    ├── agents/                # Agents IA
    ├── database/              # Migrations DB
    ├── fixes/                 # Corrections de bugs
    └── tests/                 # Création de tests
```

## 🎯 Usage

### Pour Développer une Feature

1. **Lire** `WORKFLOW_ORCHESTRATION.md`
2. **Créer** un log dans le dossier approprié : `logs/<type>/YYYY-MM-DD_<type>_<nom>.md`
3. **Suivre** le workflow étape par étape
4. **Mettre à jour** le log à chaque étape
5. **Mettre à jour** `STATUS.md` à la fin

### Format des Logs

Voir le template dans `WORKFLOW_ORCHESTRATION.md` section "Créer le Log d'Activité"

### Commandes Disponibles

- `/write-test <type> <target>` - Écrire des tests
- `/create-agent <nom>` - Créer un agent IA
- `/create-endpoint <nom>` - Créer un endpoint API
- `/create-component <nom>` - Créer un composant React
- `/create-page <path>` - Créer une page Next.js
- `/create-migration msg="<description>"` - Créer une migration DB

## 📊 État Actuel

Consulter `STATUS.md` pour l'état général de l'avancement.

---

*Dernière mise à jour : 15 Janvier 2026*
