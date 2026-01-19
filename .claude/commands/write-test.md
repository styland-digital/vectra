# Écrire des Tests

## Usage

```
/write-test <type> <target>
```

## Types de Tests Disponibles

| Type | Description | Cible | Framework |
|------|-------------|-------|-----------|
| `unit-service` | Test unitaire service backend | `app/services/<nom>.py` | pytest |
| `unit-agent` | Test unitaire agent IA | `app/agents/<nom>/agent.py` | pytest |
| `unit-utils` | Test unitaire utilitaire | `app/utils/<nom>.py` | pytest |
| `integration-api` | Test intégration API | `app/api/v1/<nom>.py` | pytest + httpx |
| `integration-db` | Test intégration base de données | `app/db/repositories/<nom>.py` | pytest + SQLAlchemy |
| `e2e` | Test end-to-end | Parcours utilisateur | Playwright |
| `component` | Test composant React | `components/<nom>.tsx` | Jest + React Testing Library |

## Exemples

### Test Service Backend

```
/write-test unit-service bant
```

Crée `backend/tests/unit/services/test_bant_service.py` avec :

- Fixtures pour le service
- Tests de calcul de score
- Tests de validation
- Tests avec paramètres
- Coverage cible : 90%

### Test Agent IA

```
/write-test unit-agent prospector
```

Crée `backend/tests/unit/agents/test_prospector_agent.py` avec :

- Mock du LLM
- Tests d'analyse de profil
- Tests de matching
- Tests de fallback
- Coverage cible : 85%

### Test API

```
/write-test integration-api campaigns
```

Crée `backend/tests/integration/api/test_campaigns_api.py` avec :

- Client authentifié
- Tests CRUD complets
- Tests de validation
- Tests d'isolation multi-tenant
- Coverage cible : 80%

### Test Composant React

```
/write-test component LeadCard
```

Crée `frontend/__tests__/components/LeadCard.test.tsx` avec :

- Rendu de base
- Interactions utilisateur
- Props validation
- États (loading, error, empty)
- Coverage cible : 70%

## Structure de Test Standard

### Backend (pytest)

```python
import pytest
from unittest.mock import Mock, patch
from app.services.<nom> import <Service>

class Test<Service>:
    """Tests du service <nom>."""
    
    @pytest.fixture
    def service(self):
        """Fixture pour le service."""
        return <Service>()
    
    @pytest.fixture
    def sample_data(self):
        """Fixture pour données de test."""
        return {
            # Données de test
        }
    
    # === Tests de base ===
    
    def test_<fonction>_success(self, service, sample_data):
        """Test de succès de <fonction>."""
        result = service.<fonction>(sample_data)
        assert result.success == True
        assert result.data is not None
    
    def test_<fonction>_validation_error(self, service):
        """Test de validation d'erreur."""
        with pytest.raises(ValueError):
            service.<fonction>(invalid_data)
    
    # === Tests avec paramètres ===
    
    @pytest.mark.parametrize("input,expected", [
        (case1, result1),
        (case2, result2),
    ])
    def test_<fonction>_variants(self, service, input, expected):
        """Test avec différents paramètres."""
        result = service.<fonction>(input)
        assert result == expected
    
    # === Tests d'isolation multi-tenant ===
    
    def test_<fonction>_tenant_isolation(self, service, org_a, org_b):
        """Test d'isolation entre organisations."""
        result = service.<fonction>(org_a_data)
        assert result.organization_id == org_a.id
        # Vérifier que org_b ne voit pas les données
```

### Frontend (Jest + React Testing Library)

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { <Component> } from '@/components/<path>';

describe('<Component>', () => {
  const defaultProps = {
    // Props par défaut
  };
  
  it('renders correctly', () => {
    render(<Component {...defaultProps} />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
  
  it('handles user interaction', () => {
    const onAction = jest.fn();
    render(<Component {...defaultProps} onAction={onAction} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalledTimes(1);
  });
  
  it('displays loading state', () => {
    render(<Component {...defaultProps} loading={true} />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
  
  it('displays error state', () => {
    render(<Component {...defaultProps} error="Error message" />);
    expect(screen.getByText('Error message')).toBeInTheDocument();
  });
});
```

## Conventions de Nommage

### Fichiers de Test

- Backend : `test_<nom>.py` (snake_case)
- Frontend : `<Component>.test.tsx` (PascalCase)

### Classes de Test

- Backend : `Test<Service>` (PascalCase)
- Frontend : `describe('<Component>')`

### Méthodes de Test

- Format : `test_<scenario>_<expected_result>`
- Exemples :
  - `test_calculate_score_returns_valid_result`
  - `test_create_lead_validation_error`
  - `test_list_campaigns_empty_list`

## Coverage Requis

| Type | Cible | Minimum |
|------|-------|---------|
| Services | 90% | 80% |
| Agents | 85% | 75% |
| API Routes | 80% | 70% |
| Utils | 95% | 90% |
| Components | 70% | 60% |

## Checklist Après Création

- [ ] Tests couvrent les cas de succès
- [ ] Tests couvrent les cas d'erreur
- [ ] Tests couvrent les cas limites
- [ ] Tests d'isolation multi-tenant (si applicable)
- [ ] Fixtures créées pour données de test
- [ ] Mocks configurés correctement
- [ ] Coverage atteint (vérifier avec `pytest --cov`)
- [ ] Tests passent (`pytest tests/unit/services/test_<nom>.py`)

## Références

- Plan de tests : `docs/tech/DOC-TECH-006_TEST_PLAN.md`
- Guide développeur : `docs/tech/DOC-TECH-005_GUIDE_DEV.md`
- Exemples de tests : Voir `docs/tech/DOC-TECH-006_TEST_PLAN.md` sections 3-5
