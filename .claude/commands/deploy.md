---

## 5. deploy.md

```markdown
# Déployer

## Usage
```
/deploy <environment>
```

Environments:
- `staging` - Déployer sur staging
- `production` - Déployer sur production (⚠️ confirmation requise)

## Pré-requis

- [ ] Tous les tests passent
- [ ] Pas de changements non commités
- [ ] PR mergée dans la bonne branche

## Process Staging

```bash
git checkout develop
git pull origin develop
# Le déploiement est automatique via GitHub Actions
```

## Process Production

```bash
# 1. Créer une PR develop → main
# 2. Review et approval
# 3. Merge

# Le déploiement est automatique via GitHub Actions
```

## Vérifications post-déploiement

1. [ ] Health check OK: `curl https://api.vectra.io/health`
2. [ ] Pas d'erreurs dans les logs (5 min)
3. [ ] Métriques stables dans Grafana
4. [ ] Test smoke manuel des fonctions critiques

## Rollback si problème

```bash
# Via Render Dashboard
# Service > Deploys > Sélectionner version précédente > Rollback

# Ou via Git
git revert HEAD
git push origin main
```
```

---