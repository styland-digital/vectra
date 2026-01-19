# VECTRA - PLAN DE TESTS
## Stratégie de Test Complète
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-007  
**Statut:** APPROUVÉ  
**Objectif:** Définir la stratégie de test pour garantir la qualité du produit  

---

## TABLE DES MATIERES

1. Vue d'Ensemble
2. Types de Tests
3. Tests Unitaires
4. Tests d'Intégration
5. Tests End-to-End
6. Tests de Performance
7. Tests de Sécurité
8. Tests des Agents IA
9. Validation BANT (Gold Standard)
10. Environnements de Test
11. Automatisation CI/CD
12. Critères de Release

---

## 1. VUE D'ENSEMBLE

### 1.1 Pyramide des Tests

```
        /\
       /  \      E2E Tests (10%)
      /----\     - Parcours utilisateur complets
     /      \    
    /--------\   Integration Tests (20%)
   /          \  - API endpoints, DB, agents
  /------------\ 
 /              \ Unit Tests (70%)
/----------------\ - Services, utils, composants
```

### 1.2 Objectifs de Couverture

| Couche | Cible | Minimum | Critique |
|--------|-------|---------|----------|
| Services métier | 90% | 80% | Oui |
| Agents IA | 85% | 75% | Oui |
| API Routes | 80% | 70% | Oui |
| Repositories | 85% | 75% | Non |
| Utils | 95% | 90% | Non |
| Frontend Components | 70% | 60% | Non |

### 1.3 Responsabilités

| Rôle | Responsabilité |
|------|----------------|
| Développeur | Tests unitaires + intégration pour son code |
| Tech Lead | Review des tests, tests d'architecture |
| QA (si présent) | Tests E2E, tests exploratoires |
| PM | Validation fonctionnelle, acceptance criteria |

---

## 2. TYPES DE TESTS

### 2.1 Matrice des Tests

| Type | Quoi | Quand | Qui |
|------|------|-------|-----|
| Unitaire | Fonctions isolées | À chaque commit | Dev |
| Intégration | APIs, DB, agents | À chaque PR | Dev + CI |
| E2E | Parcours complets | Avant release | CI + QA |
| Performance | Charge, latence | Hebdo + avant release | CI |
| Sécurité | OWASP, vulnérabilités | Mensuel + avant release | Security |
| Smoke | Fonctions critiques | Après deploy | CI |
| Régression | Suite complète | Avant release | CI |

---

## 3. TESTS UNITAIRES

### 3.1 Structure Backend

```
backend/tests/unit/
├── services/
│   ├── test_bant_service.py
│   ├── test_campaign_service.py
│   ├── test_lead_service.py
│   └── test_email_service.py
├── agents/
│   ├── test_prospector_agent.py
│   ├── test_bant_agent.py
│   └── test_scheduler_agent.py
├── utils/
│   ├── test_validators.py
│   ├── test_formatters.py
│   └── test_crypto.py
└── conftest.py
```

### 3.2 Exemple: Test Service BANT

```python
# tests/unit/services/test_bant_service.py

import pytest
from unittest.mock import Mock, patch
from app.services.bant import BANTService, BANTScore, BANTCriteria

class TestBANTService:
    """Tests du service de qualification BANT."""
    
    @pytest.fixture
    def service(self):
        return BANTService(threshold=60)
    
    @pytest.fixture
    def sample_lead(self):
        return {
            "company_size": "100-500",
            "job_title": "VP Sales",
            "industry": "SaaS",
            "recent_activity": True
        }
    
    # === Tests du calcul de score ===
    
    def test_calculate_score_returns_bant_score(self, service):
        """Le calcul doit retourner un objet BANTScore."""
        result = service.calculate_score(
            budget=20, authority=20, need=15, timeline=15
        )
        assert isinstance(result, BANTScore)
        assert result.total == 70
    
    def test_calculate_score_max_values(self, service):
        """Score maximum = 100."""
        result = service.calculate_score(25, 25, 25, 25)
        assert result.total == 100
        assert result.qualified == True
    
    def test_calculate_score_min_values(self, service):
        """Score minimum = 0."""
        result = service.calculate_score(0, 0, 0, 0)
        assert result.total == 0
        assert result.qualified == False
    
    def test_calculate_score_at_threshold(self, service):
        """Score égal au seuil = qualifié."""
        result = service.calculate_score(15, 15, 15, 15)  # = 60
        assert result.total == 60
        assert result.qualified == True
    
    def test_calculate_score_below_threshold(self, service):
        """Score sous le seuil = non qualifié."""
        result = service.calculate_score(14, 15, 15, 15)  # = 59
        assert result.total == 59
        assert result.qualified == False
    
    # === Tests de validation des inputs ===
    
    @pytest.mark.parametrize("invalid_value", [-1, 26, 100, -100])
    def test_calculate_score_invalid_budget(self, service, invalid_value):
        """Budget hors range doit lever ValueError."""
        with pytest.raises(ValueError, match="budget"):
            service.calculate_score(invalid_value, 20, 20, 20)
    
    @pytest.mark.parametrize("criterion,value", [
        ("budget", -1),
        ("authority", 30),
        ("need", -5),
        ("timeline", 26),
    ])
    def test_validate_criterion_range(self, service, criterion, value):
        """Chaque critère doit être entre 0 et 25."""
        kwargs = {"budget": 15, "authority": 15, "need": 15, "timeline": 15}
        kwargs[criterion] = value
        with pytest.raises(ValueError):
            service.calculate_score(**kwargs)
    
    # === Tests avec critères pondérés ===
    
    def test_calculate_with_custom_weights(self):
        """Les poids personnalisés doivent être appliqués."""
        weights = BANTCriteria(
            budget_weight=30,  # Sur 100
            authority_weight=30,
            need_weight=20,
            timeline_weight=20
        )
        service = BANTService(threshold=60, weights=weights)
        
        # Budget et Authority ont plus de poids
        result = service.calculate_score(25, 25, 10, 10)
        
        # (25*0.3 + 25*0.3 + 10*0.2 + 10*0.2) = 7.5 + 7.5 + 2 + 2 = 19
        # Normalized to 0-100: ...
        assert result.qualified == True
    
    # === Tests du scoring par profil ===
    
    def test_score_from_profile_vp_level(self, service, sample_lead):
        """Un VP doit avoir un score authority élevé."""
        result = service.score_from_profile(sample_lead)
        assert result.authority >= 16  # VP = 16-20
    
    def test_score_from_profile_large_company(self, service):
        """Grande entreprise = score budget élevé."""
        lead = {"company_size": "500+", "job_title": "Manager"}
        result = service.score_from_profile(lead)
        assert result.budget >= 16
    
    def test_score_from_profile_missing_data(self, service):
        """Données manquantes = scores conservateurs."""
        lead = {}
        result = service.score_from_profile(lead)
        assert result.total < 40  # Score faible par défaut
    
    # === Tests de la recommandation ===
    
    @pytest.mark.parametrize("score,expected", [
        (80, "contact"),
        (65, "contact"),
        (60, "contact"),
        (55, "nurture"),
        (45, "nurture"),
        (40, "nurture"),
        (35, "reject"),
        (20, "reject"),
    ])
    def test_get_recommendation(self, service, score, expected):
        """La recommandation dépend du score."""
        bant_score = BANTScore(
            budget=score//4, authority=score//4, 
            need=score//4, timeline=score//4,
            total=score
        )
        recommendation = service.get_recommendation(bant_score)
        assert recommendation == expected
```

### 3.3 Exemple: Test Utils

```python
# tests/unit/utils/test_validators.py

import pytest
from app.utils.validators import validate_email, validate_phone, validate_url

class TestEmailValidator:
    @pytest.mark.parametrize("email", [
        "user@example.com",
        "user.name@example.com",
        "user+tag@example.com",
        "user@subdomain.example.com",
    ])
    def test_valid_emails(self, email):
        assert validate_email(email) == True
    
    @pytest.mark.parametrize("email", [
        "invalid",
        "@example.com",
        "user@",
        "user@.com",
        "",
        None,
    ])
    def test_invalid_emails(self, email):
        assert validate_email(email) == False

class TestPhoneValidator:
    @pytest.mark.parametrize("phone", [
        "+33612345678",
        "+1 (555) 123-4567",
        "0612345678",
    ])
    def test_valid_phones(self, phone):
        assert validate_phone(phone) == True
```

### 3.4 Frontend Unit Tests

```typescript
// frontend/__tests__/components/LeadCard.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { LeadCard } from '@/components/features/leads/LeadCard';
import { Lead } from '@/types';

const mockLead: Lead = {
  id: '123',
  firstName: 'Marie',
  lastName: 'Dupont',
  email: 'marie@company.com',
  company: 'TechCorp',
  status: 'qualified',
  bantScore: 75,
};

describe('LeadCard', () => {
  it('renders lead name and company', () => {
    render(<LeadCard lead={mockLead} />);
    
    expect(screen.getByText('Marie Dupont')).toBeInTheDocument();
    expect(screen.getByText('TechCorp')).toBeInTheDocument();
  });
  
  it('displays BANT score badge', () => {
    render(<LeadCard lead={mockLead} />);
    
    expect(screen.getByText('75')).toBeInTheDocument();
  });
  
  it('calls onSelect when clicked', () => {
    const onSelect = jest.fn();
    render(<LeadCard lead={mockLead} onSelect={onSelect} />);
    
    fireEvent.click(screen.getByRole('button'));
    
    expect(onSelect).toHaveBeenCalledWith(mockLead);
  });
  
  it('shows qualified status with green badge', () => {
    render(<LeadCard lead={mockLead} />);
    
    const badge = screen.getByText('qualified');
    expect(badge).toHaveClass('bg-green-100');
  });
});
```

---

## 4. TESTS D'INTÉGRATION

### 4.1 Tests API

```python
# tests/integration/api/test_campaigns_api.py

import pytest
from httpx import AsyncClient
from app.main import app
from app.db.models import Campaign

@pytest.fixture
async def auth_client(test_db, test_user):
    """Client authentifié pour les tests."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/auth/login", json={
            "email": test_user.email,
            "password": "testpassword"
        })
        token = response.json()["data"]["access_token"]
        client.headers["Authorization"] = f"Bearer {token}"
        yield client

class TestCampaignsAPI:
    """Tests d'intégration pour l'API Campaigns."""
    
    async def test_list_campaigns_empty(self, auth_client):
        """Liste vide si pas de campagnes."""
        response = await auth_client.get("/v1/campaigns")
        
        assert response.status_code == 200
        assert response.json()["data"] == []
    
    async def test_create_campaign_success(self, auth_client):
        """Création d'une campagne valide."""
        response = await auth_client.post("/v1/campaigns", json={
            "name": "Test Campaign",
            "target_criteria": {
                "job_titles": ["VP Sales"],
                "locations": ["France"]
            },
            "bant_threshold": 60
        })
        
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["name"] == "Test Campaign"
        assert data["status"] == "draft"
        assert "id" in data
    
    async def test_create_campaign_validation_error(self, auth_client):
        """Erreur si nom manquant."""
        response = await auth_client.post("/v1/campaigns", json={
            "target_criteria": {}
        })
        
        assert response.status_code == 422
        assert "name" in response.json()["error"]["details"][0]["field"]
    
    async def test_get_campaign_not_found(self, auth_client):
        """404 si campagne inexistante."""
        response = await auth_client.get("/v1/campaigns/00000000-0000-0000-0000-000000000000")
        
        assert response.status_code == 404
    
    async def test_launch_campaign(self, auth_client, test_campaign):
        """Lancement d'une campagne draft."""
        response = await auth_client.post(f"/v1/campaigns/{test_campaign.id}/launch")
        
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "active"
    
    async def test_launch_campaign_already_active(self, auth_client, active_campaign):
        """Erreur si campagne déjà active."""
        response = await auth_client.post(f"/v1/campaigns/{active_campaign.id}/launch")
        
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "INVALID_STATUS"
    
    async def test_campaign_isolation(self, auth_client, other_org_campaign):
        """Une org ne voit pas les campagnes des autres."""
        response = await auth_client.get(f"/v1/campaigns/{other_org_campaign.id}")
        
        assert response.status_code == 404  # Pas 403, on cache l'existence
```

### 4.2 Tests Base de Données

```python
# tests/integration/db/test_lead_repository.py

import pytest
from app.db.repositories.lead_repository import LeadRepository
from app.db.models import Lead

class TestLeadRepository:
    """Tests d'intégration pour le repository Lead."""
    
    @pytest.fixture
    def repo(self, test_db):
        return LeadRepository(test_db)
    
    async def test_create_lead(self, repo, test_campaign):
        """Création d'un lead."""
        lead = await repo.create({
            "campaign_id": test_campaign.id,
            "organization_id": test_campaign.organization_id,
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        })
        
        assert lead.id is not None
        assert lead.email == "test@example.com"
        assert lead.status == "new"
    
    async def test_find_by_email_hash(self, repo, test_lead):
        """Recherche par hash email pour déduplication."""
        found = await repo.find_by_email_hash(
            campaign_id=test_lead.campaign_id,
            email_hash=test_lead.email_hash
        )
        
        assert found is not None
        assert found.id == test_lead.id
    
    async def test_list_qualified_leads(self, repo, test_campaign):
        """Liste des leads qualifiés."""
        # Setup: créer des leads avec différents scores
        await repo.create({"email": "low@test.com", "bant_score": 40, ...})
        await repo.create({"email": "high@test.com", "bant_score": 75, ...})
        
        leads = await repo.list_qualified(
            campaign_id=test_campaign.id,
            threshold=60
        )
        
        assert len(leads) == 1
        assert leads[0].email == "high@test.com"
```

---

## 5. TESTS END-TO-END

### 5.1 Setup Playwright

```typescript
// playwright.config.ts

import { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
  testDir: './e2e',
  timeout: 30000,
  retries: 2,
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
  ],
};

export default config;
```

### 5.2 Tests E2E Critiques

```typescript
// e2e/campaigns/create-campaign.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Create Campaign Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('[name="email"]', 'admin@vectra-demo.com');
    await page.fill('[name="password"]', 'demo123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });
  
  test('complete campaign creation wizard', async ({ page }) => {
    // Step 1: Start wizard
    await page.click('text=Nouvelle Campagne');
    await expect(page).toHaveURL(/\/campaigns\/new/);
    
    // Step 2: Name & Sector
    await page.fill('[name="name"]', 'E2E Test Campaign');
    await page.selectOption('[name="sector"]', 'saas');
    await page.click('text=Suivant');
    
    // Step 3: Target Profile
    await page.fill('[name="job_titles"]', 'VP Sales, Director');
    await page.selectOption('[name="company_size"]', '50-200');
    await page.fill('[name="locations"]', 'France');
    await page.click('text=Suivant');
    
    // Step 4: Email Template
    await expect(page.locator('[name="email_subject"]')).toBeVisible();
    await page.fill('[name="email_subject"]', 'Test Subject');
    await page.fill('[name="email_template"]', 'Test email body...');
    await page.click('text=Suivant');
    
    // Step 5: Meeting Availability
    await page.check('[name="days.1"]'); // Monday
    await page.check('[name="days.2"]'); // Tuesday
    await page.fill('[name="calendly_link"]', 'https://calendly.com/test');
    await page.click('text=Suivant');
    
    // Step 6: Review & Create
    await expect(page.locator('text=E2E Test Campaign')).toBeVisible();
    await page.click('text=Créer la Campagne');
    
    // Verify success
    await expect(page.locator('text=Campagne créée')).toBeVisible();
    await expect(page).toHaveURL(/\/campaigns\/[a-z0-9-]+$/);
  });
  
  test('validation errors on empty form', async ({ page }) => {
    await page.goto('/campaigns/new');
    await page.click('text=Suivant');
    
    await expect(page.locator('text=Le nom est requis')).toBeVisible();
  });
});
```

### 5.3 Test E2E: Parcours Lead Complet

```typescript
// e2e/leads/lead-lifecycle.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Lead Lifecycle', () => {
  test('lead from new to meeting scheduled', async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('[name="email"]', 'admin@vectra-demo.com');
    await page.fill('[name="password"]', 'demo123');
    await page.click('button[type="submit"]');
    
    // Go to leads page
    await page.click('text=Leads');
    await page.waitForURL('/leads');
    
    // Find a qualified lead
    await page.click('[data-status="qualified"]');
    
    // View lead details
    await expect(page.locator('[data-testid="bant-score"]')).toBeVisible();
    await expect(page.locator('text=Score BANT')).toBeVisible();
    
    // View generated email
    await page.click('text=Email Généré');
    await expect(page.locator('[data-testid="email-preview"]')).toBeVisible();
    
    // Approve email
    await page.click('text=Approuver');
    await expect(page.locator('text=Email approuvé')).toBeVisible();
    
    // Verify status changed
    await expect(page.locator('[data-status="contacted"]')).toBeVisible();
  });
});
```

---

## 6. TESTS DE PERFORMANCE

### 6.1 Tests de Charge avec Locust

```python
# tests/performance/locustfile.py

from locust import HttpUser, task, between

class VectraUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login au démarrage."""
        response = self.client.post("/v1/auth/login", json={
            "email": "loadtest@vectra.io",
            "password": "loadtest123"
        })
        self.token = response.json()["data"]["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def list_campaigns(self):
        """Liste des campagnes (fréquent)."""
        self.client.get("/v1/campaigns", headers=self.headers)
    
    @task(5)
    def list_leads(self):
        """Liste des leads (très fréquent)."""
        self.client.get("/v1/leads?per_page=20", headers=self.headers)
    
    @task(2)
    def get_dashboard(self):
        """Dashboard métriques."""
        self.client.get("/v1/analytics/dashboard", headers=self.headers)
    
    @task(1)
    def create_lead(self):
        """Création de lead (moins fréquent)."""
        self.client.post("/v1/leads", headers=self.headers, json={
            "campaign_id": "test-campaign-id",
            "email": f"test{self.random()}@example.com",
            "first_name": "Load",
            "last_name": "Test"
        })
```

### 6.2 Seuils de Performance

| Endpoint | P50 | P95 | P99 | Max |
|----------|-----|-----|-----|-----|
| GET /campaigns | 50ms | 150ms | 300ms | 1s |
| GET /leads (paginated) | 100ms | 200ms | 400ms | 1s |
| POST /leads | 150ms | 300ms | 500ms | 2s |
| GET /analytics/dashboard | 200ms | 500ms | 1s | 3s |
| Agent BANT | 3s | 10s | 15s | 30s |

### 6.3 Commandes

```bash
# Lancer Locust
locust -f tests/performance/locustfile.py --host=http://localhost:8000

# Avec paramètres
locust -f tests/performance/locustfile.py \
  --headless \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m
```

---

## 7. TESTS DE SÉCURITÉ

### 7.1 Checklist OWASP Top 10

| Vulnérabilité | Test | Statut |
|---------------|------|--------|
| A01 - Broken Access Control | Test isolation multi-tenant | ⬜ |
| A02 - Cryptographic Failures | Audit encryption, JWT | ⬜ |
| A03 - Injection | SQL injection tests | ⬜ |
| A04 - Insecure Design | Review architecture | ⬜ |
| A05 - Security Misconfiguration | Headers, CORS | ⬜ |
| A06 - Vulnerable Components | Dependency scan | ⬜ |
| A07 - Auth Failures | Brute force, token security | ⬜ |
| A08 - Data Integrity Failures | Input validation | ⬜ |
| A09 - Logging Failures | Audit log coverage | ⬜ |
| A10 - SSRF | URL validation | ⬜ |

### 7.2 Tests d'Isolation Multi-Tenant

```python
# tests/security/test_tenant_isolation.py

class TestTenantIsolation:
    """Tests de sécurité pour l'isolation multi-tenant."""
    
    async def test_cannot_access_other_org_campaigns(self, org_a_client, org_b_campaign):
        """Org A ne peut pas voir les campagnes de Org B."""
        response = await org_a_client.get(f"/v1/campaigns/{org_b_campaign.id}")
        assert response.status_code == 404
    
    async def test_cannot_access_other_org_leads(self, org_a_client, org_b_lead):
        """Org A ne peut pas voir les leads de Org B."""
        response = await org_a_client.get(f"/v1/leads/{org_b_lead.id}")
        assert response.status_code == 404
    
    async def test_cannot_modify_other_org_data(self, org_a_client, org_b_campaign):
        """Org A ne peut pas modifier les données de Org B."""
        response = await org_a_client.patch(
            f"/v1/campaigns/{org_b_campaign.id}",
            json={"name": "Hacked!"}
        )
        assert response.status_code == 404
    
    async def test_leads_list_only_own_org(self, org_a_client, org_a_leads, org_b_leads):
        """Liste ne retourne que les leads de sa propre org."""
        response = await org_a_client.get("/v1/leads")
        lead_ids = [l["id"] for l in response.json()["data"]]
        
        for lead in org_a_leads:
            assert str(lead.id) in lead_ids
        for lead in org_b_leads:
            assert str(lead.id) not in lead_ids
```

---

## 8. TESTS DES AGENTS IA

### 8.1 Tests du Prospector Agent

```python
# tests/unit/agents/test_prospector_agent.py

class TestProspectorAgent:
    @pytest.fixture
    def agent(self, mock_llm):
        return ProspectorAgent(llm=mock_llm)
    
    async def test_analyze_profile_match(self, agent):
        """Profil correspondant aux critères."""
        profile = {
            "name": "Marie Dupont",
            "title": "VP Sales",
            "company": "TechCorp",
            "industry": "SaaS",
            "size": "50-200"
        }
        criteria = {
            "job_titles": ["VP Sales", "Director"],
            "industries": ["SaaS", "Tech"]
        }
        
        result = await agent.analyze_profile(profile, criteria)
        
        assert result.match == True
        assert result.score >= 70
    
    async def test_analyze_profile_no_match(self, agent):
        """Profil ne correspondant pas."""
        profile = {"title": "Junior Developer", "industry": "Retail"}
        criteria = {"job_titles": ["VP Sales"], "industries": ["SaaS"]}
        
        result = await agent.analyze_profile(profile, criteria)
        
        assert result.match == False
        assert result.recommendation == "skip"
```

### 8.2 Tests du BANT Agent

```python
# tests/unit/agents/test_bant_agent.py

class TestBANTAgent:
    async def test_score_high_value_prospect(self, agent):
        """VP dans grande entreprise = score élevé."""
        lead = {
            "job_title": "VP Sales",
            "company_size": "500+",
            "recent_activity": True,
            "industry": "SaaS"
        }
        
        result = await agent.score(lead)
        
        assert result.total >= 70
        assert result.qualified == True
        assert result.authority >= 16
    
    async def test_score_low_value_prospect(self, agent):
        """Junior sans budget = score faible."""
        lead = {
            "job_title": "Sales Rep",
            "company_size": "1-10",
            "recent_activity": False
        }
        
        result = await agent.score(lead)
        
        assert result.total < 40
        assert result.qualified == False
    
    async def test_llm_failure_fallback(self, agent, failing_llm):
        """Fallback si LLM échoue."""
        agent.llm = failing_llm
        lead = {"job_title": "VP Sales"}
        
        result = await agent.score(lead)
        
        # Score conservateur en fallback
        assert result.requires_review == True
        assert result.total == 50  # Score neutre
```

---

## 9. VALIDATION BANT (GOLD STANDARD)

### 9.1 Dataset de Validation

20 leads manuellement évalués par l'équipe pour calibrer le BANT agent.

```python
# tests/validation/bant_gold_standard.py

GOLD_STANDARD = [
    {
        "id": 1,
        "profile": {
            "job_title": "VP Sales",
            "company_size": "200-500",
            "industry": "SaaS",
            "recent_posts": True
        },
        "expected_score": 85,
        "expected_qualified": True,
        "human_notes": "Décideur clair, entreprise cible, actif"
    },
    {
        "id": 2,
        "profile": {
            "job_title": "Sales Manager",
            "company_size": "50-100",
            "industry": "Tech"
        },
        "expected_score": 65,
        "expected_qualified": True,
        "human_notes": "Bon profil mais pas top décideur"
    },
    # ... 18 autres cas
]

class TestBANTGoldStandard:
    @pytest.mark.parametrize("case", GOLD_STANDARD)
    async def test_gold_standard_case(self, agent, case):
        """Vérifie chaque cas du gold standard."""
        result = await agent.score(case["profile"])
        
        # Tolérance de ±15 points
        assert abs(result.total - case["expected_score"]) <= 15
        assert result.qualified == case["expected_qualified"]
    
    async def test_overall_accuracy(self, agent):
        """Accuracy globale ≥ 80%."""
        correct = 0
        for case in GOLD_STANDARD:
            result = await agent.score(case["profile"])
            if result.qualified == case["expected_qualified"]:
                correct += 1
        
        accuracy = correct / len(GOLD_STANDARD)
        assert accuracy >= 0.80, f"Accuracy {accuracy:.0%} < 80%"
```

---

## 10. ENVIRONNEMENTS DE TEST

| Env | Base de données | LLM | Données |
|-----|-----------------|-----|---------|
| Unit | Mock / SQLite | Mock | Fixtures |
| Integration | PostgreSQL Docker | Mock | Seeds |
| E2E | PostgreSQL Docker | Ollama local | Seeds |
| Staging | PostgreSQL Render | Ollama Render | Copy prod (anonymisé) |

---

## 11. AUTOMATISATION CI/CD

```yaml
# .github/workflows/test.yml

name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/unit --cov=app --cov-fail-under=80

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx playwright install
      - run: npm run test:e2e
```

---

## 12. CRITÈRES DE RELEASE

### 12.1 Checklist Pre-Release

- [ ] Tous les tests passent (unit, integration, e2e)
- [ ] Coverage ≥ 80% sur services et agents
- [ ] Aucune vulnérabilité critique (security scan)
- [ ] Performance dans les seuils
- [ ] Gold standard BANT ≥ 80% accuracy
- [ ] Review de code approuvée
- [ ] Documentation à jour
- [ ] Changelog mis à jour

### 12.2 Definition of Done

Une feature est "done" quand:
1. Code mergé dans develop
2. Tests unitaires écrits (coverage ≥ 80%)
3. Tests d'intégration si API
4. Documentation mise à jour
5. Review approuvée
6. QA validée (si applicable)

---

**- FIN DU DOCUMENT -**

*14 Janvier 2026*
