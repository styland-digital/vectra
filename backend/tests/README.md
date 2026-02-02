# Tests - Vectra Backend

## Structure

```
tests/
├── unit/
│   ├── agents/
│   │   ├── test_prospector.py
│   │   └── test_bant.py
│   └── services/
│       └── test_scoring.py
├── integration/
│   └── (à venir)
└── e2e/
    └── (à venir)
```

## Lancer les tests

### Tous les tests

```bash
cd backend
pytest
```

### Tests unitaires uniquement

```bash
pytest tests/unit/
```

### Tests spécifiques

```bash
# Tests d'un agent
pytest tests/unit/agents/test_prospector.py

# Tests d'un service
pytest tests/unit/services/test_scoring.py

# Tests avec coverage
pytest --cov=app tests/unit/
```

### Avec verbosité

```bash
pytest -v
```

### Avec coverage report

```bash
pytest --cov=app --cov-report=html tests/unit/
```

## Prérequis

```bash
pip install pytest pytest-asyncio pytest-cov
```
