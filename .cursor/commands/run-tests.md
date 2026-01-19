---

## 4. run-tests.md

```markdown
# Lancer les Tests

## Usage
```
/run-tests [scope]
```

Scopes disponibles:
- `all` - Tous les tests
- `unit` - Tests unitaires backend
- `integration` - Tests d'intégration API
- `e2e` - Tests end-to-end Playwright
- `frontend` - Tests frontend Jest
- `<fichier>` - Tests d'un fichier spécifique

## Commandes selon le scope

### All
```bash
cd backend && pytest --cov=app --cov-fail-under=80
cd frontend && npm run test
```

### Unit
```bash
cd backend && pytest tests/unit -v
```

### Integration
```bash
cd backend && pytest tests/integration -v
```

### E2E
```bash
cd frontend && npm run test:e2e
```

### Fichier spécifique
```bash
cd backend && pytest tests/unit/services/test_bant_service.py -v
```

## Interprétation des résultats

### Coverage minimum requis

| Couche | Minimum |
|--------|---------|
| Services | 80% |
| Agents | 75% |
| API | 70% |
| Frontend | 60% |

### Actions si échec

1. Lire le message d'erreur
2. Identifier le test qui échoue
3. Vérifier si c'est le test ou le code qui est faux
4. Fixer et relancer
```

---