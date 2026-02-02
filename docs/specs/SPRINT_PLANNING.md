# AGILE SPRINT PLANNING - Q1 MVP
## 12 Semaines | 6 Sprints × 2 Semaines
### 05 Janvier 2026

---

## OVERVIEW

- **Duration**: 12 weeks
- **Team**: 2 devs + 1 PM
- **Total Story Points**: 72 SP
- **Velocity**: 6 SP/week/dev

---

## SPRINT 1 (WK 1-2): FOUNDATION & ARCHITECTURE

**Goal**: Project setup + architecture decisions locked
**Capacity**: 12 SP

| ID | Story | Type | SP |
|----|-------|------|-----|
| US-001 | Setup project monorepo | Task | 3 |
| US-002 | Setup CI/CD pipeline | Task | 3 |
| US-003 | Design database schema | Design | 3 |
| US-004 | Architecture workshop | Meeting | 2 |
| US-005 | Setup testing infrastructure | Task | 1 |

---

## SPRINT 2 (WK 3-4): CREWAI + PROSPECTOR

**Goal**: Agent 1 working end-to-end
**Capacity**: 16 SP

| ID | Story | Type | SP |
|----|-------|------|-----|
| US-006 | CrewAI integration & setup | Feature | 5 |
| US-007 | Prospector agent core logic | Feature | 5 |
| US-008 | RocketReach API integration | Feature | 3 |
| US-009 | Lead deduplication logic | Feature | 2 |
| US-010 | Error handling + logging | Task | 1 |

---

## SPRINT 3 (WK 5-6): BANT AGENT + STATE MACHINE

**Goal**: Multi-agent orchestration working
**Capacity**: 14 SP

| ID | Story | Type | SP |
|----|-------|------|-----|
| US-011 | BANT qualification agent | Feature | 5 |
| US-012 | State machine orchestration | Feature | 5 |
| US-013 | Email generation (LLM) | Feature | 3 |
| US-014 | Integration tests (multi-agent) | Test | 1 |

---

## SPRINT 4 (WK 7-8): FRONTEND MVP + DASHBOARD

**Goal**: Users can see leads + agent status
**Capacity**: 12 SP

| ID | Story | Type | SP |
|----|-------|------|-----|
| US-015 | Dashboard layout + components | Feature | 4 |
| US-016 | Lead list display + filtering | Feature | 3 |
| US-017 | Agent status monitoring UI | Feature | 3 |
| US-018 | JWT authentication | Feature | 2 |

---

## SPRINT 5 (WK 9-10): INTEGRATIONS & POLISH

**Goal**: Production-ready for beta
**Capacity**: 10 SP

| ID | Story | Type | SP |
|----|-------|------|-----|
| US-019 | HubSpot API sync | Feature | 4 |
| US-020 | End-to-end testing | Test | 3 |
| US-021 | Performance optimization | Task | 2 |
| US-022 | Security audit (OWASP) | Task | 1 |

---

## SPRINT 6 (WK 11-12): BETA LAUNCH PREP

**Goal**: Ready for 10-15 beta testers
**Capacity**: 8 SP

| ID | Story | Type | SP |
|----|-------|------|-----|
| US-023 | Onboarding workflow | Feature | 3 |
| US-024 | Support infrastructure | Task | 2 |
| US-025 | Documentation | Doc | 2 |
| US-026 | Production deployment | Task | 1 |

---

## HIGH-RISK ITEMS

- **US-012**: State machine orchestration (CRITICAL PATH)
- **US-007**: Prospector logic
- **US-013**: LLM French quality

## DEPENDENCIES

```
US-005 → US-006
US-012 → US-015
US-019 requires full backend
```

---

## READY FOR JIRA

- **Project**: AGENTIC
- **Board**: Scrum
- **Sprint**: 2 weeks
- **Scale**: Fibonacci

---

*APPROVED FOR SPRINT 1 START*
*Signoff: 05 January 2026*
