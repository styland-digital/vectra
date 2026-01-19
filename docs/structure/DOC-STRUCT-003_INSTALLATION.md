# VECTRA - GUIDE D'INSTALLATION CLAUDE CODE
## Comment Configurer Claude Code pour le Projet
### 14 Janvier 2026

---

## 🎯 OBJECTIF

Ce guide explique comment structurer ton projet pour que Claude Code:
1. Comprenne parfaitement l'architecture
2. Suive les conventions établies
3. Utilise les commandes personnalisées
4. Reste cohérent tout au long du développement

---

## 📁 STRUCTURE À CRÉER

Avant de commencer à coder, crée cette structure:

```bash
# Créer le projet
mkdir vectra && cd vectra
git init

# Structure .claude (CRITIQUE)
mkdir -p .claude/commands

# Docs
mkdir -p docs/{specs,guides,adr,operations}

# Backend
mkdir -p backend/{app/{api/v1,agents/{prospector,bant,scheduler},core,db/{models,repositories},services,schemas,tasks,utils},tests/{unit,integration,e2e},alembic/versions,scripts}

# Frontend
mkdir -p frontend/{app/{auth,dashboard},components/{ui,layout,features},lib,hooks,stores,types,__tests__,e2e,public}

# Scripts globaux
mkdir -p scripts .github/workflows
```

---

## 📄 FICHIERS À PLACER

### 1. Fichier Principal: `.claude/CLAUDE.md`

C'est le fichier que Claude Code lit EN PREMIER. Copie le contenu de `CLAUDE.md` que j'ai créé.

```bash
cp /chemin/vers/CLAUDE.md .claude/CLAUDE.md
```

### 2. Commandes Personnalisées: `.claude/commands/`

Crée ces 6 fichiers dans `.claude/commands/`:

```bash
# Dans .claude/commands/
touch create-agent.md
touch create-endpoint.md
touch create-migration.md
touch run-tests.md
touch deploy.md
touch debug.md
```

Copie le contenu de chaque section du document `DOC12_CLAUDE_COMMANDS.md` dans le fichier correspondant.

### 3. Documentation: `docs/`

Place les documents de spec:

```
docs/
├── specs/
│   ├── SPECIFICATION_TECHNIQUE_V2.md
│   ├── SCHEMA_DATABASE.md
│   └── CONTRATS_API.md
├── guides/
│   ├── GUIDE_DEVELOPPEUR.md
│   ├── PROMPTS_TEMPLATES.md
│   ├── PLAN_TESTS.md
│   └── DOCUMENTATION_UTILISATEUR.md
├── adr/
│   └── (créer au fur et à mesure)
└── operations/
    ├── RUNBOOK.md
    └── PLAYBOOK_COMMERCIAL.md
```

### 4. Fichiers de Configuration

Place ces fichiers à la racine et dans les sous-dossiers:

```
vectra/
├── docker-compose.yml          # Depuis DOC11
├── Makefile                    # Depuis DOC11
├── README.md
├── .gitignore
├── backend/
│   ├── pyproject.toml         # Depuis DOC11
│   ├── requirements.txt       # Depuis DOC11
│   ├── requirements-dev.txt   # Depuis DOC11
│   ├── alembic.ini
│   ├── .env.example           # Depuis DOC11
│   └── Dockerfile
└── frontend/
    ├── package.json           # Depuis DOC11
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── next.config.js
    ├── .env.example           # Depuis DOC11
    └── Dockerfile
```

---

## 🚀 DÉMARRER AVEC CLAUDE CODE

### Étape 1: Ouvrir le projet

```bash
cd vectra
claude  # ou ouvrir dans VS Code avec extension Claude
```

### Étape 2: Vérifier que Claude lit le contexte

Claude Code devrait automatiquement:
1. Lire `.claude/CLAUDE.md`
2. Comprendre l'architecture
3. Connaître les conventions

Tu peux vérifier en demandant:
> "Quel est le stack technique de ce projet?"

Claude devrait répondre: Python/FastAPI, Next.js, PostgreSQL, CrewAI, etc.

### Étape 3: Utiliser les commandes

```
/create-agent intent-classifier
/create-endpoint leads PATCH
/create-migration "add intent column to leads"
/run-tests unit
/debug db
```

---

## 📋 CHECKLIST D'INSTALLATION

### Structure Minimale Requise

- [ ] `.claude/CLAUDE.md` existe et contient les instructions
- [ ] `.claude/commands/` contient les 6 fichiers de commandes
- [ ] `docs/specs/` contient les 3 specs principales
- [ ] `docker-compose.yml` existe
- [ ] `Makefile` existe
- [ ] `backend/requirements.txt` existe
- [ ] `frontend/package.json` existe

### Vérification

```bash
# Vérifier la structure
tree -L 3 -I 'node_modules|__pycache__|.git'

# Vérifier les fichiers critiques
cat .claude/CLAUDE.md | head -20
ls .claude/commands/
ls docs/specs/
```

---

## 💡 CONSEILS D'UTILISATION

### 1. Toujours Donner du Contexte

```
# Bon
"Je travaille sur l'agent BANT. Comment implémenter le scoring?"

# Moins bon
"Comment faire le scoring?"
```

### 2. Référencer les Docs

```
"Selon SCHEMA_DATABASE.md, la table leads a une colonne bant_score. 
Comment l'utiliser dans le service?"
```

### 3. Utiliser les Commandes

Au lieu de demander "comment créer un endpoint", utilise:
```
/create-endpoint campaigns POST
```

### 4. Demander des ADR pour les Décisions

```
"Je dois choisir entre Redis et RabbitMQ pour les queues. 
Peux-tu créer un ADR pour documenter cette décision?"
```

---

## 🔄 WORKFLOW RECOMMANDÉ

### Pour une Nouvelle Feature

1. **Commencer par la spec**
   ```
   "Je veux ajouter la fonctionnalité X. Que dois-je modifier?"
   ```

2. **Créer la migration si DB**
   ```
   /create-migration "add X table"
   ```

3. **Créer l'endpoint**
   ```
   /create-endpoint X POST
   ```

4. **Implémenter le service**
   ```
   "Implémente le service pour X selon le pattern existant"
   ```

5. **Créer les tests**
   ```
   "Écris les tests pour le service X"
   ```

6. **Vérifier**
   ```
   /run-tests unit
   ```

### Pour Debugger

1. **Identifier le type de problème**
   ```
   /debug api
   ```

2. **Suivre les instructions**

3. **Demander de l'aide ciblée**
   ```
   "J'ai cette erreur dans les logs: [erreur]. 
   Que dois-je vérifier?"
   ```

---

## 📦 FICHIERS PRÊTS À L'EMPLOI

Tu as maintenant **13 documents** :

| # | Fichier | Usage |
|---|---------|-------|
| 1 | SPECIFICATION_TECHNIQUE_V2 | Architecture globale |
| 2 | SCHEMA_DATABASE | Tables PostgreSQL |
| 3 | CONTRATS_API | Endpoints REST |
| 4 | ADR | Décisions techniques |
| 5 | GUIDE_DEVELOPPEUR | Onboarding dev |
| 6 | PROMPTS_TEMPLATES | Prompts agents |
| 7 | PLAN_TESTS | Stratégie tests |
| 8 | DOCUMENTATION_UTILISATEUR | Guide end-user |
| 9 | RUNBOOK | Ops & incidents |
| 10 | PLAYBOOK_COMMERCIAL | Vente |
| 11 | STRUCTURE_MONOREPO | Config & structure |
| 12 | CLAUDE_COMMANDS | Commandes slash |
| 13 | Ce guide | Installation |

---

## ✅ PRÊT!

Une fois cette structure en place, Claude Code sera capable de:

- ✅ Comprendre l'architecture multi-agent
- ✅ Respecter les conventions de code
- ✅ Créer des fichiers cohérents
- ✅ Suggérer les bons patterns
- ✅ Exécuter les commandes personnalisées
- ✅ Maintenir la cohérence sur tout le projet

---

**Bonne construction de Vectra! 🚀**

*14 Janvier 2026*
