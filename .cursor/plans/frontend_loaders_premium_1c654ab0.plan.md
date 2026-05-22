---
name: Frontend loaders premium
overview: Vérifier l’implémentation frontend par rapport aux guidelines Vectra (calme, peu de gradients décoratifs, transitions courtes), corriger les états de chargement (loader global, skeletons, Suspense) et harmoniser sans remplacer tout le design system ni la logique métier.
todos:
  - id: page-loader
    content: Créer composant PageLoader (shell + indicateur discret, props dense/message)
    status: completed
  - id: loading-skeleton
    content: "Refactor LoadingSkeleton: page délègue au loader, Skeleton sans gradient shimmer, table avatar rounded-md"
    status: completed
  - id: wire-entrypoints
    content: Brancher auth-guard, landing page, Suspense auth sur le même pattern
    status: completed
  - id: i18n-hydration
    content: Remplacer return null I18nProvider par loader minimal cohérent
    status: completed
  - id: verify
    content: npm run lint + npm run build + smoke manuel thème clair/sombre
    status: completed
isProject: false
---

# Vérification frontend et amélioration loaders / chargement

## Contexte et contrainte

- Les consignes **vectra-frontend-designer** et **vectra-ui-components** servent de **référence visuelle** ; le code actuel s’appuie sur **[`frontend/app/globals.css`](frontend/app/globals.css)** (tokens `--bg-*`, `--surface-*`, `--auth-panel-*`, jaune Vectra, etc.). **Ne pas** migrer tout le projet vers le schéma HSL du skill (conflit avec Shadcn + `data-theme`).
- Objectif : **aligner loaders et squelettes** sur « quiet confidence » (peu de gradient décoratif, pas d’accent bleu dominant au boot, pas d’écran vide prolongé).

## Constats actuels (à corriger ou unifier)

| Zone | Fichier | Problème vs guidelines |
|------|---------|---------------------------|
| Page boot / auth | [`frontend/components/loading-skeleton.tsx`](frontend/components/loading-skeleton.tsx) `variant="page"` | Carré **gradient bleu** + `animate-pulse` : trop « produit générique », accent trop présent. |
| Squelettes | Même fichier, `Skeleton` | **Shimmer sur gradient** infini (2s) : acceptable pour data tables si très discret ; aujourd’hui un peu « marketing » vs Linear. |
| Table skeleton | `variant="table"` | Avatar `rounded-full` : le designer recommande d’éviter le full sur les conteneurs non circulaires ; préférer `rounded-md`. |
| Landing auth check | [`frontend/app/page.tsx`](frontend/app/page.tsx) | `VectraLogo` + `animate-pulse` seul : OK mais **incohérent** avec le reste de l’app (pas le même pattern que `AuthGuard`). |
| Suspense / formulaires | [`frontend/app/(auth)/login/page.tsx`](frontend/app/(auth)/login/page.tsx), reset, etc. | **`Loader2` + `animate-spin`** répété : fonctionnel mais non unifié ; pas de message optionnel. |
| Hydratation i18n | [`frontend/lib/providers.tsx`](frontend/lib/providers.tsx) | Tant que `I18nProvider` n’est pas hydraté, **`return null`** : flash blanc/vide possible avant le contenu. |

## Plan d’implémentation (ordre recommandé)

### 1. Composant unique de chargement « app shell »

- Créer **`frontend/components/page-loader.tsx`** (ou `app-loading.tsx`) exportant un petit bloc réutilisable :
  - Fond `bg-[var(--bg-primary)]` (cohérent light `#f6f6f6` / dark `#0e0e0e`).
  - Logo Vectra optionnel, **sans** gros bloc gradient bleu.
  - Indicateur discret : soit **3 barres / pulse d’opacité** sur un conteneur neutre (durée ~1–1.5s, style sobre), soit un **spinner minimal** (une seule implémentation pour toute l’app).
- Props optionnelles : `message?: string` (pour i18n plus tard si besoin), `dense?: boolean` pour les fallbacks `Suspense`.

### 2. Refactoriser `LoadingSkeleton`

- Dans [`frontend/components/loading-skeleton.tsx`](frontend/components/loading-skeleton.tsx) :
  - **`variant="page"`** : remplacer le carré gradient par le nouveau `PageLoader` (ou composition interne identique).
  - **`Skeleton`** : remplacer le gradient shimmer par un **fond uni** `bg-[var(--surface-secondary)]` + animation **opacity** courte (ex. 1.2s ease-in-out infinite alternate) pour rester premium et moins « Dribbble ».
  - **`variant="table"`** : `rounded-full` → `rounded-md` sur le placeholder avatar ; vérifier largeurs (`w-3/4` est valide en Tailwind fractionné ; garder ou passer en `w-[75%]` si besoin de clarté).

### 3. Brancher les points d’entrée sur le même pattern

- [`frontend/components/auth-guard.tsx`](frontend/components/auth-guard.tsx) : garder `LoadingSkeleton variant="page"` si ce variant délègue au nouveau loader (zéro duplication de markup).
- [`frontend/app/page.tsx`](frontend/app/page.tsx) : remplacer le bloc `animate-pulse` + logo par le **même** composant que l’auth guard pour cohérence.
- **Suspense fallbacks** (login, reset-password, etc.) : remplacer `Card + Loader2` par **`PageLoader dense`** ou un **skeleton de carte** aligné avec `LoadingSkeleton variant="card"` pour éviter le spinner nu.

### 4. Hydratation I18n (flash vide)

- Dans [`frontend/lib/providers.tsx`](frontend/lib/providers.tsx), remplacer `return null` avant hydratation par un **chargement minimal** (même `PageLoader` sans texte, ou skeleton neutre plein écran) pour respecter l’expérience « premium » et éviter le blanc.

### 5. Boutons et densité (hors scope strict loaders — optionnel court)

- [`frontend/components/ui/button.tsx`](frontend/components/ui/button.tsx) : `default` size `h-10` vs guideline `h-8`. **Recommandation** : ne pas tout changer en une fois ; si on touche le bouton, documenter un **ADR ou TODO** ou n’ajuster que `sm` comme taille par défaut sur les écrans dashboard dans un second temps pour limiter la régression visuelle.

### 6. Vérification

- `cd frontend && npm run lint` et `npm run build`.
- Parcours manuel : première visite (flash), `/login` Suspense, navigation dashboard avec `AuthGuard`, thème clair/sombre.

## Hors périmètre (éviter la dérive)

- Refonte complète sidebar / tables / badges pour coller au skill zinc (trop large, risque de casser les pages déjà adaptées aux tokens Vectra).
- Remplacement global des `Loader2` dans **toutes** les mutations (peut rester sur les actions inline si le loader unifié couvre shell + Suspense + page).

## Fichiers principaux touchés

- Nouveau : `frontend/components/page-loader.tsx` (nom exact à valider à l’implémentation).
- Modifiés : [`frontend/components/loading-skeleton.tsx`](frontend/components/loading-skeleton.tsx), [`frontend/lib/providers.tsx`](frontend/lib/providers.tsx), [`frontend/app/page.tsx`](frontend/app/page.tsx), fallbacks Suspense dans [`frontend/app/(auth)/login/page.tsx`](frontend/app/(auth)/login/page.tsx) et [`frontend/app/(auth)/reset-password/page.tsx`](frontend/app/(auth)/reset-password/page.tsx) (et autres auth si mêmes patterns).
