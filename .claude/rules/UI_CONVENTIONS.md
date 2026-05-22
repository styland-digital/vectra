# Règles UI/UX Vectra — Premium SaaS

## Erreurs de formulaire

- Erreur API → `<Alert variant="destructive">` en haut du formulaire (dans CardContent)
- Erreur champ → `<p className="text-xs text-[var(--color-error-500)]">` sous le champ
- Effacer l'erreur API dès que l'utilisateur tape :
  ```tsx
  <Form onChange={() => { if (error) clearError() }}>
  ```
- Les deux types PEUVENT coexister mais l'erreur API doit disparaître dès la saisie

## Typography — tokens obligatoires

| Usage | Token | Interdit |
|-------|-------|----------|
| Titre page / section | `text-h1`, `text-h2` | `text-3xl`, `text-4xl` |
| Titre card | `text-h3` | `text-2xl`, `text-xl` |
| Sous-titre card | `text-h4`, `text-h5` | `text-lg` |
| Corps | `text-body`, `text-body-sm` | `text-sm`, `text-base` |
| Meta / label | `text-caption`, `text-overline` | `text-xs` |

> **Règle :** Jamais de tailles Tailwind brutes (`text-sm`, `text-xs`, `text-lg`) en dehors des composants shadcn internes.

## Couleurs sémantiques

- **Erreur :** `text-[var(--color-error-500)]` ou `text-destructive`
- **Succès :** `text-[var(--color-success-500)]`
- **Primary fill** (progress bar, indicateur) : `bg-[var(--color-primary-500)]` — JAMAIS `bg-[var(--text-primary)]`
- **Texte secondaire :** `text-[var(--text-secondary)]`
- **Texte muted :** `text-[var(--text-muted)]`
- **Accent** : `--color-vectra-yellow-*` uniquement pour badges et icônes Sparkles

## Structure auth page

- Titre de la page : **1 seul endroit** — dans `<CardHeader>` (PAS en doublon à l'extérieur)
- Succès : `<Alert variant="default">` ou bloc avec `<CheckCircle2>` + couleur `--color-success-500`
- Loading/Suspense fallback : `<PageLoader dense showLogo={false} />`

## Schémas de validation i18n (Formik + Zod)

- **TOUJOURS** passer `t` au schéma : `createXxxSchema(t)` — jamais `xxxSchema` directement
- Validation en langue utilisateur, pas en anglais hardcodé

## Grilles responsive

- KPI grid : `sm:grid-cols-2 lg:grid-cols-4` (cohérent entre dashboard et campaign detail)
- Cards content : `lg:grid-cols-3` pour panels principaux

## Uniformité des boutons — RÈGLE CRITIQUE

Tous les boutons côte à côte dans un groupe d'actions **doivent avoir la même hauteur**.

| Cas | Solution |
|-----|----------|
| Bouton icône seul (sans texte) à côté d'un bouton normal | `size="icon"` (h-10 w-10) — JAMAIS `size="sm"` |
| Toggle/segmented control à côté d'un `<Button>` | Conteneur `h-10 items-stretch` + boutons `flex items-center` sans `py-*` |
| Bouton `sm` inévitable dans un groupe mixte | Compenser avec `h-10` sur le `sm` via className |

**Pattern segmented control aligné avec Button default (h-10) :**
```tsx
<div className="flex items-stretch h-10 rounded-lg border border-[var(--border-primary)] bg-[var(--surface-secondary)] p-0.5 gap-0.5">
  <button className="flex items-center px-3 text-body-sm rounded-md ...">Option</button>
</div>
```

**Checklist groupe d'actions :**
- Tous les `<Button>` sans `size` → h-10
- Bouton icône seul → `size="icon"` (h-10 w-10)
- Jamais `size="sm"` (h-8) ni `size="lg"` (h-11) mélangés avec `default` (h-10) dans un même groupe

## Interactions boutons

- Eye toggle (password) : `transition-colors duration-150` obligatoire
- Liens auth : `transition-colors duration-150`
- Cards cliquables : `transition-colors duration-200`

## Motions / animations

- Page entière : `<PageTransition>` wrapper
- Listes : `<StaggerContainer>` + `<StaggerItem>`
- Erreurs animées :
  ```tsx
  <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }}>
  ```

## Checklist avant livraison UI

- [ ] Un seul titre par page (pas de doublon CardHeader / page wrapper)
- [ ] Tokens typography utilisés (pas de raw Tailwind sizes)
- [ ] `createXxxSchema(t)` sur tous les formulaires
- [ ] `onChange` sur chaque `<Form>` pour vider erreur API stale
- [ ] Progress bars : `bg-[var(--color-primary-500)]`
- [ ] **Tous les boutons d'un même groupe ont la même hauteur** (h-10 par défaut)
- [ ] Boutons icône seuls → `size="icon"`, jamais `size="sm"`
- [ ] Segmented controls (toggles période, tabs custom) → `h-10 items-stretch` sur le conteneur
- [ ] `npx tsc --noEmit` → zéro erreur
