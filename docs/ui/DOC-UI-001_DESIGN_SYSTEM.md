# VECTRA - DESIGN SYSTEM COMPLET
## Premium B2B SaaS Interface Guidelines
### Version 2.0 | 14 Janvier 2026

---

**Document:** DOC-UI-001  
**Statut:** RÉFÉRENCE DESIGN  
**Inspiration:** Linear, Stripe, Notion, Vercel  
**Stack:** Next.js 14 + Tailwind CSS + Shadcn/ui + Framer Motion  

---

## TABLE DES MATIÈRES

1. Philosophie Design Vectra
2. Design Tokens Avancés
3. Système Typographique
4. Palette de Couleurs
5. Spacing & Layout System
6. Composants Fondamentaux
7. Composants Complexes
8. Patterns d'Interaction
9. Motion Design
10. Responsive Strategy
11. Dark Mode Implementation
12. Accessibilité (WCAG 2.1 AA)

---

## 1. PHILOSOPHIE DESIGN VECTRA

### 1.1 Principes Fondamentaux

Vectra adopte une philosophie **"Calm Technology"** inspirée de Linear et Stripe :

| Principe | Description | Anti-pattern |
|----------|-------------|--------------|
| **Silence visuel** | L'interface s'efface au profit du contenu | Animations flashy, couleurs saturées |
| **Densité maîtrisée** | Information riche sans surcharge | Trop d'espace vide ou trop dense |
| **Hiérarchie claire** | L'œil sait où aller instantanément | Éléments de même importance visuelle |
| **Feedback subtil** | Micro-interactions qui rassurent | Pas de feedback ou feedback excessif |
| **Professionnalisme** | Inspire confiance et compétence | Look "startup" ou amateur |

### 1.2 L'ADN Visuel Vectra

```
VECTRA = Puissance silencieuse + Précision chirurgicale + Élégance sobre
```

**Ce que Vectra EST :**
- Premium mais accessible
- Technique mais humain
- Puissant mais simple
- Moderne mais intemporel

**Ce que Vectra N'EST PAS :**
- Flashy ou tape-à-l'œil
- Froid ou robotique
- Complexe ou intimidant
- Daté ou générique

### 1.3 Le Test des 10 Secondes

Chaque écran doit répondre à ces questions en < 10 secondes :

1. **Où suis-je ?** (Context)
2. **Que puis-je faire ?** (Actions)
3. **Qu'est-ce qui est important ?** (Priorité)
4. **Comment avancer ?** (Next step)

---

## 2. DESIGN TOKENS AVANCÉS

### 2.1 Architecture des Tokens

```
├── Primitives (valeurs brutes)
│   ├── colors.blue.500 = #2E5BFF
│   ├── spacing.4 = 16px
│   └── radius.md = 8px
│
├── Semantic (signification)
│   ├── color.primary = colors.blue.500
│   ├── color.success = colors.green.500
│   └── spacing.component.padding = spacing.4
│
└── Component (usage spécifique)
    ├── button.primary.bg = color.primary
    ├── card.padding = spacing.component.padding
    └── input.radius = radius.md
```

### 2.2 Tokens Complets (CSS Variables)

```css
:root {
  /* ═══════════════════════════════════════════
     COULEURS PRIMITIVES
     ═══════════════════════════════════════════ */
  
  /* Primary - Bleu Vectra */
  --color-primary-50: #EEF2FF;
  --color-primary-100: #E0E7FF;
  --color-primary-200: #C7D2FE;
  --color-primary-300: #A5B4FC;
  --color-primary-400: #818CF8;
  --color-primary-500: #2E5BFF;  /* Main */
  --color-primary-600: #2548CC;
  --color-primary-700: #1C3699;
  --color-primary-800: #132466;
  --color-primary-900: #0A1233;
  
  /* Accent - Orange */
  --color-accent-50: #FFF7ED;
  --color-accent-100: #FFEDD5;
  --color-accent-200: #FED7AA;
  --color-accent-300: #FDBA74;
  --color-accent-400: #FB923C;
  --color-accent-500: #FF9F43;  /* Main */
  --color-accent-600: #EA580C;
  --color-accent-700: #C2410C;
  --color-accent-800: #9A3412;
  --color-accent-900: #7C2D12;
  
  /* Neutrals - Slate refined */
  --color-neutral-0: #FFFFFF;
  --color-neutral-50: #F8FAFC;
  --color-neutral-100: #F1F5F9;
  --color-neutral-200: #E2E8F0;
  --color-neutral-300: #CBD5E1;
  --color-neutral-400: #94A3B8;
  --color-neutral-500: #64748B;
  --color-neutral-600: #475569;
  --color-neutral-700: #334155;
  --color-neutral-800: #1E293B;
  --color-neutral-900: #0F172A;
  --color-neutral-950: #020617;
  
  /* Semantic Colors */
  --color-success-500: #22C55E;
  --color-success-600: #16A34A;
  --color-warning-500: #F59E0B;
  --color-warning-600: #D97706;
  --color-error-500: #EF4444;
  --color-error-600: #DC2626;
  --color-info-500: #3B82F6;
  --color-info-600: #2563EB;
  
  /* ═══════════════════════════════════════════
     SPACING (8px base grid)
     ═══════════════════════════════════════════ */
  --space-0: 0px;
  --space-px: 1px;
  --space-0-5: 2px;
  --space-1: 4px;
  --space-1-5: 6px;
  --space-2: 8px;
  --space-2-5: 10px;
  --space-3: 12px;
  --space-3-5: 14px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 28px;
  --space-8: 32px;
  --space-9: 36px;
  --space-10: 40px;
  --space-11: 44px;
  --space-12: 48px;
  --space-14: 56px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  --space-28: 112px;
  --space-32: 128px;
  
  /* ═══════════════════════════════════════════
     TYPOGRAPHY
     ═══════════════════════════════════════════ */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Font Sizes */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */
  
  /* Line Heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  
  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* Letter Spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide: 0.025em;
  
  /* ═══════════════════════════════════════════
     BORDERS & RADIUS
     ═══════════════════════════════════════════ */
  --radius-none: 0px;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-2xl: 16px;
  --radius-full: 9999px;
  
  --border-width: 1px;
  --border-width-2: 2px;
  
  /* ═══════════════════════════════════════════
     SHADOWS (Layered for depth)
     ═══════════════════════════════════════════ */
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
  
  /* Focus ring */
  --ring-offset: 2px;
  --ring-width: 2px;
  --ring-color: var(--color-primary-500);
  
  /* ═══════════════════════════════════════════
     TRANSITIONS & ANIMATIONS
     ═══════════════════════════════════════════ */
  --duration-75: 75ms;
  --duration-100: 100ms;
  --duration-150: 150ms;
  --duration-200: 200ms;
  --duration-300: 300ms;
  --duration-500: 500ms;
  --duration-700: 700ms;
  --duration-1000: 1000ms;
  
  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  
  /* ═══════════════════════════════════════════
     Z-INDEX SCALE
     ═══════════════════════════════════════════ */
  --z-negative: -1;
  --z-0: 0;
  --z-10: 10;
  --z-20: 20;
  --z-30: 30;
  --z-40: 40;
  --z-50: 50;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
  --z-max: 9999;
}
```

### 2.3 Dark Mode Tokens

```css
[data-theme="dark"] {
  /* Backgrounds */
  --bg-primary: var(--color-neutral-950);
  --bg-secondary: var(--color-neutral-900);
  --bg-tertiary: var(--color-neutral-800);
  --bg-elevated: var(--color-neutral-800);
  --bg-overlay: rgba(0, 0, 0, 0.8);
  
  /* Surfaces (cards, modals) */
  --surface-primary: var(--color-neutral-900);
  --surface-secondary: var(--color-neutral-800);
  --surface-hover: var(--color-neutral-700);
  --surface-active: var(--color-neutral-600);
  
  /* Borders */
  --border-primary: var(--color-neutral-700);
  --border-secondary: var(--color-neutral-800);
  --border-hover: var(--color-neutral-600);
  
  /* Text */
  --text-primary: var(--color-neutral-50);
  --text-secondary: var(--color-neutral-400);
  --text-tertiary: var(--color-neutral-500);
  --text-muted: var(--color-neutral-600);
  --text-inverse: var(--color-neutral-900);
  
  /* Shadows for dark mode (subtle glow) */
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.3), 0 1px 2px -1px rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.3);
  --shadow-glow: 0 0 20px rgba(46, 91, 255, 0.15);
}

[data-theme="light"] {
  /* Backgrounds */
  --bg-primary: var(--color-neutral-0);
  --bg-secondary: var(--color-neutral-50);
  --bg-tertiary: var(--color-neutral-100);
  --bg-elevated: var(--color-neutral-0);
  --bg-overlay: rgba(0, 0, 0, 0.5);
  
  /* Surfaces */
  --surface-primary: var(--color-neutral-0);
  --surface-secondary: var(--color-neutral-50);
  --surface-hover: var(--color-neutral-100);
  --surface-active: var(--color-neutral-200);
  
  /* Borders */
  --border-primary: var(--color-neutral-200);
  --border-secondary: var(--color-neutral-100);
  --border-hover: var(--color-neutral-300);
  
  /* Text */
  --text-primary: var(--color-neutral-900);
  --text-secondary: var(--color-neutral-600);
  --text-tertiary: var(--color-neutral-500);
  --text-muted: var(--color-neutral-400);
  --text-inverse: var(--color-neutral-0);
}
```

---

## 3. SYSTÈME TYPOGRAPHIQUE

### 3.1 Échelle Typographique

```
Display    48px / 1.1  / -0.02em / Bold      → Héros, titres de page
H1         36px / 1.2  / -0.02em / Semibold  → Titres principaux
H2         30px / 1.25 / -0.01em / Semibold  → Sections majeures
H3         24px / 1.3  / -0.01em / Semibold  → Sous-sections
H4         20px / 1.4  / normal  / Medium    → Titres de cards
H5         18px / 1.4  / normal  / Medium    → Petits titres
H6         16px / 1.5  / normal  / Medium    → Labels importants

Body Large  18px / 1.6  / normal  / Normal   → Paragraphes importants
Body        16px / 1.5  / normal  / Normal   → Texte par défaut
Body Small  14px / 1.5  / normal  / Normal   → Texte secondaire
Caption     12px / 1.4  / 0.01em  / Normal   → Métadonnées, hints
Overline    11px / 1.3  / 0.1em   / Medium   → Labels, catégories (UPPERCASE)
```

### 3.2 Classes Tailwind

```typescript
// tailwind.config.ts
const typography = {
  '.text-display': {
    fontSize: '3rem',
    lineHeight: '1.1',
    letterSpacing: '-0.02em',
    fontWeight: '700',
  },
  '.text-h1': {
    fontSize: '2.25rem',
    lineHeight: '1.2',
    letterSpacing: '-0.02em',
    fontWeight: '600',
  },
  '.text-h2': {
    fontSize: '1.875rem',
    lineHeight: '1.25',
    letterSpacing: '-0.01em',
    fontWeight: '600',
  },
  '.text-h3': {
    fontSize: '1.5rem',
    lineHeight: '1.3',
    letterSpacing: '-0.01em',
    fontWeight: '600',
  },
  '.text-h4': {
    fontSize: '1.25rem',
    lineHeight: '1.4',
    fontWeight: '500',
  },
  '.text-body-lg': {
    fontSize: '1.125rem',
    lineHeight: '1.6',
  },
  '.text-body': {
    fontSize: '1rem',
    lineHeight: '1.5',
  },
  '.text-body-sm': {
    fontSize: '0.875rem',
    lineHeight: '1.5',
  },
  '.text-caption': {
    fontSize: '0.75rem',
    lineHeight: '1.4',
    letterSpacing: '0.01em',
  },
  '.text-overline': {
    fontSize: '0.6875rem',
    lineHeight: '1.3',
    letterSpacing: '0.1em',
    textTransform: 'uppercase',
    fontWeight: '500',
  },
};
```

### 3.3 Usage par Contexte

| Contexte | Style | Exemple |
|----------|-------|---------|
| Page title | H1 + text-primary | "Campaigns" |
| Section title | H2 + text-primary | "Active Campaigns" |
| Card title | H4 + text-primary | "Q1 Sales Outreach" |
| Body text | Body + text-secondary | Descriptions |
| Metadata | Caption + text-tertiary | "Created 2 days ago" |
| Badge/Label | Overline + colored | "QUALIFIED" |
| Numbers/Stats | H2 ou H3 + mono + text-primary | "2,847" |

---

## 4. PALETTE DE COULEURS

### 4.1 Usage des Couleurs

```
┌─────────────────────────────────────────────────────────────┐
│                    HIÉRARCHIE COULEURS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PRIMARY (Bleu Vectra #2E5BFF)                              │
│  ├── CTAs principaux                                        │
│  ├── Liens actifs                                           │
│  ├── Éléments de focus                                      │
│  └── Indicateurs de progression                             │
│                                                             │
│  ACCENT (Orange #FF9F43) - Usage TRÈS limité               │
│  ├── Highlights critiques                                   │
│  ├── Notifications importantes                              │
│  └── Points d'attention (max 1-2 par écran)                │
│                                                             │
│  SEMANTIC                                                   │
│  ├── Success (#22C55E) → Validations, complétions          │
│  ├── Warning (#F59E0B) → Alertes non-critiques             │
│  ├── Error (#EF4444) → Erreurs, suppressions               │
│  └── Info (#3B82F6) → Informations, tips                   │
│                                                             │
│  NEUTRALS (90% de l'interface)                             │
│  ├── Backgrounds                                            │
│  ├── Textes                                                 │
│  ├── Bordures                                               │
│  └── Icônes                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Règle du 60-30-10

- **60%** Neutrals (backgrounds, texte)
- **30%** Primary (éléments interactifs, accents subtils)
- **10%** Accent + Semantic (highlights, statuts)

### 4.3 Contraste et Accessibilité

| Combinaison | Ratio | WCAG |
|-------------|-------|------|
| text-primary sur bg-primary | 15.2:1 | AAA ✓ |
| text-secondary sur bg-primary | 7.1:1 | AA ✓ |
| text-tertiary sur bg-primary | 4.8:1 | AA ✓ |
| primary-500 sur bg-primary | 4.7:1 | AA ✓ |
| white sur primary-500 | 4.9:1 | AA ✓ |

---

## 5. SPACING & LAYOUT SYSTEM

### 5.1 Grille 8px

Tous les espacements sont des multiples de 8px :

```
4px   (0.5)  → Micro-spacing (icône-texte)
8px   (1)    → Tight spacing (entre éléments liés)
12px  (1.5)  → Small spacing
16px  (2)    → Default spacing
24px  (3)    → Medium spacing (sections)
32px  (4)    → Large spacing
48px  (6)    → Section breaks
64px  (8)    → Major sections
96px  (12)   → Page sections
```

### 5.2 Layout Containers

```typescript
// Container widths
const containers = {
  'xs': '320px',   // Mobile small
  'sm': '640px',   // Mobile large
  'md': '768px',   // Tablet
  'lg': '1024px',  // Desktop small
  'xl': '1280px',  // Desktop
  '2xl': '1536px', // Desktop large
  'full': '100%',
};

// Content max-widths
const contentWidths = {
  'prose': '65ch',      // Text content
  'form': '480px',      // Forms
  'card': '400px',      // Cards
  'modal-sm': '400px',  // Small modal
  'modal-md': '560px',  // Medium modal
  'modal-lg': '720px',  // Large modal
  'modal-xl': '900px',  // XL modal
};
```

### 5.3 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ TOPBAR (h-16, fixed)                                             │
│ ┌─────────┬──────────────────────────────────────┬─────────────┐ │
│ │ Logo    │ Breadcrumb / Search                  │ User Menu   │ │
│ └─────────┴──────────────────────────────────────┴─────────────┘ │
├──────────┬───────────────────────────────────────────────────────┤
│          │                                                       │
│ SIDEBAR  │  MAIN CONTENT                                         │
│ (w-64)   │  ┌─────────────────────────────────────────────────┐  │
│          │  │ Page Header                                     │  │
│ ┌──────┐ │  │ Title + Actions                                 │  │
│ │ Nav  │ │  └─────────────────────────────────────────────────┘  │
│ │ Item │ │  ┌─────────────────────────────────────────────────┐  │
│ │      │ │  │                                                 │  │
│ │ Nav  │ │  │ Content Area                                    │  │
│ │ Item │ │  │ (max-w-7xl mx-auto px-6)                        │  │
│ │      │ │  │                                                 │  │
│ │ Nav  │ │  │                                                 │  │
│ │ Item │ │  │                                                 │  │
│ └──────┘ │  └─────────────────────────────────────────────────┘  │
│          │                                                       │
└──────────┴───────────────────────────────────────────────────────┘
```

### 5.4 Spacing Component Standards

```typescript
const componentSpacing = {
  // Cards
  card: {
    padding: '24px',        // p-6
    gap: '16px',            // gap-4
    headerGap: '12px',      // gap-3
  },
  
  // Buttons
  button: {
    sm: { px: '12px', py: '6px', gap: '6px' },
    md: { px: '16px', py: '8px', gap: '8px' },
    lg: { px: '24px', py: '12px', gap: '8px' },
  },
  
  // Form fields
  form: {
    fieldGap: '24px',       // gap-6 between fields
    labelGap: '8px',        // gap-2 label to input
    inputPadding: '12px',   // px-3 py-2
  },
  
  // Tables
  table: {
    cellPadding: '16px',    // px-4 py-4
    headerPadding: '16px',  // px-4 py-3
    rowGap: '0',            // Attached rows
  },
  
  // Modals
  modal: {
    padding: '24px',        // p-6
    headerGap: '16px',      // mb-4
    footerGap: '24px',      // mt-6
    buttonGap: '12px',      // gap-3
  },
};
```

---

## 6. COMPOSANTS FONDAMENTAUX

### 6.1 Buttons

```tsx
// Button variants
const buttonVariants = cva(
  // Base styles
  "inline-flex items-center justify-center gap-2 rounded-md font-medium transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        // Primary - Main CTAs
        primary: "bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700 focus-visible:ring-primary-500",
        
        // Secondary - Secondary actions
        secondary: "bg-surface-secondary text-text-primary border border-border-primary hover:bg-surface-hover active:bg-surface-active",
        
        // Ghost - Tertiary actions
        ghost: "text-text-secondary hover:text-text-primary hover:bg-surface-hover active:bg-surface-active",
        
        // Danger - Destructive actions
        danger: "bg-error-500 text-white hover:bg-error-600 active:bg-error-700 focus-visible:ring-error-500",
        
        // Link - Text-like buttons
        link: "text-primary-500 hover:text-primary-600 underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
        icon: "h-10 w-10",
        "icon-sm": "h-8 w-8",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);
```

### 6.2 Inputs

```tsx
// Input base
const inputStyles = `
  w-full rounded-md border border-border-primary 
  bg-surface-primary px-3 py-2 text-sm text-text-primary
  placeholder:text-text-muted
  transition-colors duration-150
  hover:border-border-hover
  focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
  disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-surface-secondary
`;

// Input states
const inputStates = {
  default: "border-border-primary",
  hover: "border-border-hover",
  focus: "ring-2 ring-primary-500 border-transparent",
  error: "border-error-500 focus:ring-error-500",
  success: "border-success-500 focus:ring-success-500",
  disabled: "opacity-50 cursor-not-allowed bg-surface-secondary",
};
```

### 6.3 Cards

```tsx
// Card component
const Card = ({ children, className, hover = false, ...props }) => (
  <div
    className={cn(
      // Base
      "rounded-xl border border-border-primary bg-surface-primary",
      // Hover effect (optional)
      hover && "transition-all duration-200 hover:border-border-hover hover:shadow-md",
      className
    )}
    {...props}
  >
    {children}
  </div>
);

const CardHeader = ({ children, className }) => (
  <div className={cn("px-6 py-4 border-b border-border-secondary", className)}>
    {children}
  </div>
);

const CardContent = ({ children, className }) => (
  <div className={cn("px-6 py-4", className)}>
    {children}
  </div>
);

const CardFooter = ({ children, className }) => (
  <div className={cn("px-6 py-4 border-t border-border-secondary bg-surface-secondary/50", className)}>
    {children}
  </div>
);
```

### 6.4 Badges

```tsx
const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-surface-secondary text-text-secondary",
        primary: "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400",
        success: "bg-success-100 text-success-700 dark:bg-success-900/30 dark:text-success-400",
        warning: "bg-warning-100 text-warning-700 dark:bg-warning-900/30 dark:text-warning-400",
        error: "bg-error-100 text-error-700 dark:bg-error-900/30 dark:text-error-400",
        outline: "border border-border-primary text-text-secondary",
      },
      size: {
        sm: "px-2 py-0.5 text-xs",
        md: "px-2.5 py-0.5 text-xs",
        lg: "px-3 py-1 text-sm",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);
```

---

## 7. COMPOSANTS COMPLEXES

### 7.1 Data Table (Premium)

```tsx
// Table with sorting, filtering, pagination
const DataTable = ({ columns, data, searchable, filterable }) => {
  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between gap-4">
        {searchable && (
          <div className="relative w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" />
            <Input placeholder="Search..." className="pl-9" />
          </div>
        )}
        {filterable && (
          <div className="flex items-center gap-2">
            <FilterButton />
            <ColumnToggle />
          </div>
        )}
      </div>
      
      {/* Table */}
      <div className="rounded-lg border border-border-primary overflow-hidden">
        <table className="w-full">
          <thead className="bg-surface-secondary">
            <tr>
              {columns.map((col) => (
                <th 
                  key={col.id}
                  className="px-4 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider"
                >
                  <button className="flex items-center gap-1 hover:text-text-primary">
                    {col.header}
                    <SortIcon />
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-secondary">
            {data.map((row) => (
              <tr 
                key={row.id}
                className="hover:bg-surface-hover transition-colors"
              >
                {/* cells */}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Pagination */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-text-secondary">
          Showing 1-10 of 156 results
        </p>
        <Pagination />
      </div>
    </div>
  );
};
```

### 7.2 Stats Card (Dashboard)

```tsx
const StatsCard = ({ title, value, change, changeType, icon: Icon, trend }) => (
  <Card className="p-6">
    <div className="flex items-start justify-between">
      <div className="space-y-2">
        <p className="text-sm font-medium text-text-secondary">{title}</p>
        <p className="text-3xl font-semibold text-text-primary tracking-tight">
          {value}
        </p>
        {change && (
          <div className={cn(
            "flex items-center gap-1 text-sm",
            changeType === 'positive' && "text-success-500",
            changeType === 'negative' && "text-error-500",
            changeType === 'neutral' && "text-text-secondary"
          )}>
            {changeType === 'positive' && <TrendingUp className="h-4 w-4" />}
            {changeType === 'negative' && <TrendingDown className="h-4 w-4" />}
            <span>{change}</span>
            <span className="text-text-muted">vs last period</span>
          </div>
        )}
      </div>
      {Icon && (
        <div className="p-3 rounded-lg bg-primary-100 dark:bg-primary-900/20">
          <Icon className="h-5 w-5 text-primary-500" />
        </div>
      )}
    </div>
    {trend && (
      <div className="mt-4 h-12">
        <Sparkline data={trend} />
      </div>
    )}
  </Card>
);
```

### 7.3 BANT Score Display

```tsx
const BANTScore = ({ score, breakdown }) => {
  const getScoreColor = (score: number) => {
    if (score >= 70) return 'success';
    if (score >= 50) return 'warning';
    return 'error';
  };
  
  return (
    <div className="space-y-4">
      {/* Main Score */}
      <div className="flex items-center gap-4">
        <div className={cn(
          "w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold",
          score >= 70 && "bg-success-100 text-success-700 dark:bg-success-900/30",
          score >= 50 && score < 70 && "bg-warning-100 text-warning-700 dark:bg-warning-900/30",
          score < 50 && "bg-error-100 text-error-700 dark:bg-error-900/30"
        )}>
          {score}
        </div>
        <div>
          <p className="font-medium text-text-primary">
            {score >= 70 ? 'Qualified' : score >= 50 ? 'Needs Review' : 'Not Qualified'}
          </p>
          <p className="text-sm text-text-secondary">BANT Score</p>
        </div>
      </div>
      
      {/* Breakdown */}
      <div className="grid grid-cols-4 gap-3">
        {['Budget', 'Authority', 'Need', 'Timeline'].map((criterion, i) => (
          <div key={criterion} className="space-y-1">
            <div className="flex items-center justify-between">
              <span className="text-xs text-text-secondary">{criterion}</span>
              <span className="text-xs font-medium">{breakdown[i]}/25</span>
            </div>
            <div className="h-1.5 rounded-full bg-surface-secondary overflow-hidden">
              <div 
                className="h-full rounded-full bg-primary-500"
                style={{ width: `${(breakdown[i] / 25) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 7.4 Email Preview Card

```tsx
const EmailPreviewCard = ({ email, onApprove, onReject, onEdit }) => (
  <Card className="overflow-hidden">
    <CardHeader className="flex flex-row items-center justify-between">
      <div className="space-y-1">
        <p className="font-medium text-text-primary">{email.recipientName}</p>
        <p className="text-sm text-text-secondary">{email.recipientEmail}</p>
      </div>
      <Badge variant={email.status === 'pending' ? 'warning' : 'default'}>
        {email.status}
      </Badge>
    </CardHeader>
    
    <CardContent className="space-y-4">
      {/* Subject */}
      <div className="space-y-1">
        <p className="text-xs font-medium text-text-secondary uppercase tracking-wider">
          Subject
        </p>
        <p className="text-sm text-text-primary">{email.subject}</p>
      </div>
      
      {/* Body Preview */}
      <div className="space-y-1">
        <p className="text-xs font-medium text-text-secondary uppercase tracking-wider">
          Preview
        </p>
        <div className="p-4 rounded-lg bg-surface-secondary text-sm text-text-primary whitespace-pre-wrap">
          {email.body}
        </div>
      </div>
    </CardContent>
    
    <CardFooter className="flex items-center justify-end gap-3">
      <Button variant="ghost" size="sm" onClick={onReject}>
        <X className="h-4 w-4 mr-1" />
        Reject
      </Button>
      <Button variant="secondary" size="sm" onClick={onEdit}>
        <Pencil className="h-4 w-4 mr-1" />
        Edit
      </Button>
      <Button variant="primary" size="sm" onClick={onApprove}>
        <Check className="h-4 w-4 mr-1" />
        Approve
      </Button>
    </CardFooter>
  </Card>
);
```

---

## 8. PATTERNS D'INTERACTION

### 8.1 États des Éléments

```
┌─────────────────────────────────────────────────────────────┐
│                    ÉTATS INTERACTIFS                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DEFAULT                                                    │
│  └── État de base, neutre                                  │
│                                                             │
│  HOVER (150ms ease-out)                                    │
│  ├── Élévation subtile (border ou shadow)                  │
│  ├── Changement de couleur de fond                         │
│  └── Curseur approprié (pointer)                           │
│                                                             │
│  FOCUS (instantané)                                        │
│  ├── Ring bleu (2px, offset 2px)                          │
│  ├── Border transparent                                    │
│  └── Outline none (accessibility via ring)                 │
│                                                             │
│  ACTIVE (75ms)                                             │
│  ├── Fond plus sombre                                      │
│  └── Scale légèrement réduit (0.98)                       │
│                                                             │
│  DISABLED                                                   │
│  ├── Opacity 50%                                           │
│  ├── Cursor not-allowed                                    │
│  └── Pointer-events none                                   │
│                                                             │
│  LOADING                                                    │
│  ├── Spinner ou skeleton                                   │
│  ├── Texte "Loading..." optionnel                         │
│  └── Désactiver les interactions                           │
│                                                             │
│  ERROR                                                      │
│  ├── Border rouge                                          │
│  ├── Message d'erreur en dessous                          │
│  └── Icône d'erreur                                        │
│                                                             │
│  SUCCESS                                                    │
│  ├── Border vert temporaire                                │
│  ├── Checkmark animé                                       │
│  └── Reset après 2s                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Feedback Patterns

```typescript
// Toast notifications
const toastVariants = {
  success: {
    icon: CheckCircle,
    className: "border-success-500 bg-success-50 dark:bg-success-900/20",
  },
  error: {
    icon: XCircle,
    className: "border-error-500 bg-error-50 dark:bg-error-900/20",
  },
  warning: {
    icon: AlertTriangle,
    className: "border-warning-500 bg-warning-50 dark:bg-warning-900/20",
  },
  info: {
    icon: Info,
    className: "border-info-500 bg-info-50 dark:bg-info-900/20",
  },
};

// Loading states
const loadingPatterns = {
  button: "Spinner inside button, text changes to 'Loading...'",
  page: "Full page skeleton with pulse animation",
  table: "Row skeletons matching table structure",
  card: "Card skeleton with header + content placeholders",
  inline: "Small spinner next to text",
};
```

### 8.3 Empty States

```tsx
const EmptyState = ({ icon: Icon, title, description, action }) => (
  <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
    <div className="w-16 h-16 rounded-full bg-surface-secondary flex items-center justify-center mb-4">
      <Icon className="h-8 w-8 text-text-muted" />
    </div>
    <h3 className="text-lg font-medium text-text-primary mb-2">{title}</h3>
    <p className="text-sm text-text-secondary max-w-md mb-6">{description}</p>
    {action && (
      <Button variant="primary">
        {action.icon && <action.icon className="h-4 w-4 mr-2" />}
        {action.label}
      </Button>
    )}
  </div>
);

// Usage
<EmptyState
  icon={Users}
  title="No leads yet"
  description="Start a campaign to find qualified prospects for your business."
  action={{ icon: Plus, label: "Create Campaign" }}
/>
```

---

## 9. MOTION DESIGN

### 9.1 Principes d'Animation

```
RÈGLE D'OR: Les animations doivent être RESSENTIES, pas VUES.

Timing:
- Micro-interactions: 100-150ms
- Transitions UI: 200-300ms
- Entrées/Sorties: 300-500ms
- Complexes: 500-700ms

Easing:
- Entrées: ease-out (rapide → lent)
- Sorties: ease-in (lent → rapide)  
- Mouvements: ease-in-out
- Rebonds: cubic-bezier(0.68, -0.55, 0.265, 1.55) (avec modération)
```

### 9.2 Animations Framer Motion

```tsx
// Page transitions
const pageVariants = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -10 },
};

const pageTransition = {
  type: "tween",
  ease: "easeOut",
  duration: 0.2,
};

// List stagger
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0 },
};

// Modal
const modalVariants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { 
    opacity: 1, 
    scale: 1,
    transition: { type: "spring", damping: 25, stiffness: 300 }
  },
  exit: { opacity: 0, scale: 0.95, transition: { duration: 0.15 } },
};

// Sidebar collapse
const sidebarVariants = {
  expanded: { width: 256 },
  collapsed: { width: 64 },
};

// Number counter
const CountUp = ({ value }) => {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const duration = 1000;
    const steps = 60;
    const increment = value / steps;
    let current = 0;
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= value) {
        setCount(value);
        clearInterval(timer);
      } else {
        setCount(Math.floor(current));
      }
    }, duration / steps);
    
    return () => clearInterval(timer);
  }, [value]);
  
  return <span>{count.toLocaleString()}</span>;
};
```

### 9.3 CSS Animations

```css
/* Skeleton pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Spin */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Fade in up */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}

/* Scale in */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scaleIn 0.2s ease-out forwards;
}
```

---

## 10. RESPONSIVE STRATEGY

### 10.1 Breakpoints

```typescript
const breakpoints = {
  'sm': '640px',   // Mobile landscape
  'md': '768px',   // Tablet portrait
  'lg': '1024px',  // Tablet landscape / Small desktop
  'xl': '1280px',  // Desktop
  '2xl': '1536px', // Large desktop
};

// Mobile-first approach
// Base styles = mobile
// sm: = mobile landscape+
// md: = tablet+
// lg: = desktop+
```

### 10.2 Layout Adaptations

```
┌─────────────────────────────────────────────────────────────┐
│ MOBILE (<768px)                                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │ TOPBAR (sticky)                                     │    │
│  │ [☰] [Logo] [Avatar]                                 │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                     │    │
│  │            FULL WIDTH CONTENT                       │    │
│  │            (px-4, no sidebar)                       │    │
│  │                                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ BOTTOM NAV (fixed)                                  │    │
│  │ [🏠] [📊] [👥] [📧] [⚙️]                            │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TABLET (768px - 1024px)                                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │ TOPBAR                                              │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌────┬────────────────────────────────────────────────┐    │
│  │MINI│                                                │    │
│  │SIDE│           CONTENT                              │    │
│  │BAR │           (px-6)                               │    │
│  │64px│                                                │    │
│  └────┴────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ DESKTOP (>1024px)                                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │ TOPBAR                                              │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────┬───────────────────────────────────────────┐    │
│  │         │                                           │    │
│  │ SIDEBAR │           CONTENT                         │    │
│  │ (256px) │           (max-w-7xl mx-auto px-8)       │    │
│  │         │                                           │    │
│  └─────────┴───────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 10.3 Component Responsiveness

```tsx
// Stats Grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
  <StatsCard />
  <StatsCard />
  <StatsCard />
  <StatsCard />
</div>

// Table → Cards on mobile
<div className="hidden md:block">
  <DataTable data={leads} />
</div>
<div className="md:hidden space-y-4">
  {leads.map(lead => <LeadCard key={lead.id} lead={lead} />)}
</div>

// Sidebar
<aside className={cn(
  "fixed inset-y-0 left-0 z-50 flex flex-col bg-surface-primary border-r border-border-primary transition-all duration-300",
  // Mobile: full overlay when open
  "w-64 -translate-x-full md:translate-x-0",
  // Tablet: mini sidebar
  "md:w-16 lg:w-64",
  // Mobile open state
  isOpen && "translate-x-0"
)}>
```

---

## 11. DARK MODE IMPLEMENTATION

### 11.1 Strategy

```typescript
// Theme Provider
'use client';

import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function ThemeProvider({ children }) {
  return (
    <NextThemesProvider
      attribute="data-theme"
      defaultTheme="dark"  // Vectra default = dark
      enableSystem={false}
      disableTransitionOnChange={false}
    >
      {children}
    </NextThemesProvider>
  );
}
```

### 11.2 Color Usage

```tsx
// ❌ WRONG - Hardcoded colors
<div className="bg-white text-black" />
<div className="bg-gray-900 text-white" />

// ✅ CORRECT - Semantic tokens
<div className="bg-surface-primary text-text-primary" />
<div className="bg-bg-primary text-text-primary" />

// Tailwind classes (using CSS variables)
<div className="bg-[var(--surface-primary)] text-[var(--text-primary)]" />

// Or with Tailwind config extension
<div className="bg-surface text-foreground" />
```

### 11.3 Theme Toggle

```tsx
const ThemeToggle = () => {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => setMounted(true), []);
  
  if (!mounted) return <div className="w-9 h-9" />;
  
  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-lg hover:bg-surface-hover transition-colors"
      aria-label="Toggle theme"
    >
      {theme === 'dark' ? (
        <Sun className="h-5 w-5 text-text-secondary" />
      ) : (
        <Moon className="h-5 w-5 text-text-secondary" />
      )}
    </button>
  );
};
```

---

## 12. ACCESSIBILITÉ (WCAG 2.1 AA)

### 12.1 Checklist

```
✓ Contraste minimum 4.5:1 pour texte normal
✓ Contraste minimum 3:1 pour texte large (>18px ou 14px bold)
✓ Focus visible sur tous les éléments interactifs
✓ Navigation au clavier complète
✓ Labels sur tous les inputs
✓ Alt text sur toutes les images
✓ ARIA labels sur les icônes-boutons
✓ Rôles ARIA appropriés
✓ Skip to content link
✓ Annonces live regions pour updates dynamiques
```

### 12.2 Focus Management

```tsx
// Focus ring utility
const focusRing = "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 focus-visible:ring-offset-bg-primary";

// Skip to content
const SkipToContent = () => (
  <a
    href="#main-content"
    className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:px-4 focus:py-2 focus:bg-primary-500 focus:text-white focus:rounded-md"
  >
    Skip to main content
  </a>
);

// Focus trap in modals
import { FocusTrap } from '@headlessui/react';

const Modal = ({ isOpen, onClose, children }) => (
  <FocusTrap>
    <div role="dialog" aria-modal="true">
      {children}
    </div>
  </FocusTrap>
);
```

### 12.3 Screen Reader Support

```tsx
// Icon buttons
<button aria-label="Close modal">
  <X className="h-5 w-5" aria-hidden="true" />
</button>

// Status badges
<Badge aria-label={`Status: ${status}`}>
  {status}
</Badge>

// Live regions for updates
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {notification}
</div>

// Form errors
<Input
  aria-invalid={hasError}
  aria-describedby={hasError ? "email-error" : undefined}
/>
{hasError && (
  <p id="email-error" role="alert" className="text-error-500 text-sm">
    {errorMessage}
  </p>
)}
```

---

## ANNEXE: TAILWIND CONFIG COMPLET

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class', '[data-theme="dark"]'],
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: 'var(--color-primary-50)',
          100: 'var(--color-primary-100)',
          200: 'var(--color-primary-200)',
          300: 'var(--color-primary-300)',
          400: 'var(--color-primary-400)',
          500: 'var(--color-primary-500)',
          600: 'var(--color-primary-600)',
          700: 'var(--color-primary-700)',
          800: 'var(--color-primary-800)',
          900: 'var(--color-primary-900)',
        },
        accent: {
          500: 'var(--color-accent-500)',
        },
        surface: {
          primary: 'var(--surface-primary)',
          secondary: 'var(--surface-secondary)',
          hover: 'var(--surface-hover)',
        },
        border: {
          primary: 'var(--border-primary)',
          secondary: 'var(--border-secondary)',
        },
        text: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          tertiary: 'var(--text-tertiary)',
          muted: 'var(--text-muted)',
        },
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)'],
      },
      boxShadow: {
        'glow': 'var(--shadow-glow)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'fade-in-up': 'fadeInUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
    },
  },
  plugins: [
    require('tailwindcss-animate'),
    require('@tailwindcss/typography'),
  ],
};

export default config;
```

---

**- FIN DU DOCUMENT -**

*Design System Vectra v2.0*
*14 Janvier 2026*
