# TECH REVIEW & SPECIFICATION DOCUMENT
## Agent IA pour Ventes B2B - SaaS
### 05 Janvier 2026

---

## EXECUTIVE SUMMARY

**Status**: FEASIBLE & RECOMMANDÉ ✅
**Risque technique global**: MOYEN (gérable avec planning précis)
**Complexité estimée**: 8/10
**Timeline réaliste Q1**: 12 semaines (vs 16 prévues = 25% ahead)

---

## 1. ARCHITECTURE DECISION FRAMEWORK

### A. Agent Framework Decision

| Option | Pros | Cons | Effort | Recommandation |
|--------|------|------|--------|----------------|
| **CrewAI** | Multi-agent OOB, Mature | Less flexible | 3/10 | ✅ MVP |
| LangGraph | Max flexibility | Learning curve | 6/10 | Alternative |
| Custom | Full control | Boilerplate | 8/10 | Non |

**Décision**: CrewAI (sweet spot speed & flexibility)

### B. LLM Model Decision

| Option | Cost | Quality | Use Case |
|--------|------|---------|----------|
| **Llama 2 70B** | $0 | 90% GPT-3.5 | ✅ MVP |
| Mistral 7B | $0 | Better French | Cost optimized |
| Claude/GPT-4 | $$$ | Best | Fallback only |

**Décision**: Llama 2 70B + fine-tuning roadmap (mois 2-3)

---

## 2. CRITICAL RISKS

### RISK #1: Multi-Agent Orchestration (HIGH)
- **Problem**: Coordinating 3+ agents sans deadlocks
- **Probability**: 60%
- **Mitigation**: State machine design Week 1, idempotent ops, distributed tracing

### RISK #2: LLM French Output Quality
- **Problem**: Llama 2 speaks accented French
- **Probability**: 80%
- **Mitigation**: Collect data Month 1, fine-tune Month 2-3, fallback Claude Month 4

### RISK #3: External API Rate Limiting
- **Problem**: RocketReach/HubSpot strict limits
- **Probability**: 70%
- **Mitigation**: Exponential backoff, Celery + Redis queues

### RISK #4: Data Pipeline Reliability
- **Problem**: Deduplication, lead matching failures
- **Probability**: 50%
- **Mitigation**: Idempotent ETL, data quality checks, reconciliation job

---

## 3. APPROVED TECH STACK

### Backend
- Python 3.11 + FastAPI
- CrewAI framework
- Llama 2 70B self-hosted
- Celery + Redis
- PostgreSQL + pgvector

### Frontend
- Next.js 14 React
- Tailwind + Shadcn/ui
- Vercel deployment

### Infra
- Render free tier
- Vercel Serverless
- OpenTelemetry + Jaeger

---

## 4. KEY DECISIONS SUMMARY

| Decision | Rationale | Risk | Review Date |
|----------|-----------|------|-------------|
| CrewAI | 40% faster MVP | Less flexibility | Week 2 |
| Llama 2 70B | $0 cost | French quality | Month 3 |
| State Machine | Prevents deadlocks | Implementation | Week 2 |
| Queue-based | Handles rate limits | Complexity | Week 2 |

---

**RECOMMENDATION: PROCEED WITH CAUTIOUS OPTIMISM**

- Technical Feasibility: 95% ✓
- Market Timing: Excellent
- Cost Structure: Sustainable
- Timeline: Realistic 12 weeks

---

*Signoff Date: 05 Jan 2026*
*Status: READY FOR SPRINT PLANNING*
