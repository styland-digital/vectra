# VECTRA — DESIGN TOKENS OFFICIELS (V1)
## Foundation du Design System
### Janvier 2026

---

## 1️⃣ SPACING SYSTEM (8pt)

**Règle : aucun spacing libre.**

| Token | Value |
|-------|-------|
| space.1 | 4px |
| space.2 | 8px |
| space.3 | 12px |
| space.4 | 16px |
| space.5 | 24px |
| space.6 | 32px |
| space.7 | 48px |
| space.8 | 64px |

**Usage:**
- UI = strict
- Marketing = tolérance max ±1 step

---

## 2️⃣ RADIUS

| Token | Value | Usage |
|-------|-------|-------|
| radius.xs | 4px | inputs, tags |
| radius.sm | 6px | buttons |
| radius.md | 8px | cards small |
| radius.lg | 12px | cards, modals |

❌ Pas de radius custom
❌ Pas de "full rounded" hors tags

---

## 3️⃣ SHADOWS (MINIMAL, PREMIUM)

| Token | Value |
|-------|-------|
| shadow.1 | 0 1px 2px rgba(0,0,0,0.06) |
| shadow.2 | 0 4px 12px rgba(0,0,0,0.08) |

**Usage:**
- shadow.1 → inputs / hover
- shadow.2 → cards / modals

---

## 4️⃣ COLOR TOKENS

### Primary
| Token | Value |
|-------|-------|
| color.primary.500 | #2E5BFF |
| color.primary.600 | #4C7DFF |

### Accent
| Token | Value |
|-------|-------|
| color.accent.500 | #FF9F43 |

### Neutrals
| Token | Value |
|-------|-------|
| color.bg.light | #F7F9FC |
| color.bg.dark | #0E1117 |
| color.text.primary.light | #1C1F26 |
| color.text.secondary.light | #5F6470 |
| color.text.primary.dark | #E6E8EB |
| color.text.secondary.dark | #A9ADB5 |

---

## 5️⃣ TYPO TOKENS

| Token | Value |
|-------|-------|
| font.family.primary | Inter |
| font.size.sm | 12px |
| font.size.md | 14px |
| font.size.base | 16px |
| font.size.lg | 20px |
| font.size.xl | 28px |
| font.size.xxl | 36px |

---

## 6️⃣ MOTION

| Token | Value |
|-------|-------|
| motion.fast | 150ms |
| motion.base | 200ms |
| motion.slow | 250ms |
| easing | ease-out |

❌ Pas de bounce
❌ Pas de spring exagéré

---

## 7️⃣ STATES

| Token | Value | Usage |
|-------|-------|-------|
| state.success | #22C55E | Validation |
| state.warning | #F59E0B | Attention |
| state.error | #EF4444 | Erreur |
| state.info | color.primary.500 | Information |

Usage strictement fonctionnel.

---

## 🔒 STATUT

**Design Tokens VECTRA : VALIDÉS (V1)**
👉 On peut maintenant designer sans incohérence.

---

## CSS Variables

```css
:root {
  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
  --space-8: 64px;

  /* Radius */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* Colors - Light */
  --color-bg: #F7F9FC;
  --color-text-primary: #1C1F26;
  --color-text-secondary: #5F6470;
  --color-primary: #2E5BFF;
  --color-accent: #FF9F43;

  /* States */
  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);

  /* Motion */
  --duration-fast: 150ms;
  --duration-base: 200ms;
  --duration-slow: 250ms;
  --easing: ease-out;
}

.dark {
  --color-bg: #0E1117;
  --color-text-primary: #E6E8EB;
  --color-text-secondary: #A9ADB5;
}
```

---

*Design Tokens Verrouillés - V1*
