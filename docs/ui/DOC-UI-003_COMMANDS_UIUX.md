# VECTRA - COMMANDES CLAUDE CODE UI/UX
## Fichiers pour .claude/commands/ (UI/UX)
### 14 Janvier 2026

---

Ce document contient les commandes spécifiques à l'UI/UX pour Claude Code.

---

## 1. create-page.md

```markdown
# Créer une Nouvelle Page

## Usage
```
/create-page <path>
```

Exemples:
- `/create-page campaigns/[id]`
- `/create-page settings/team`

## Ce que cette commande fait

1. Crée le fichier page.tsx dans le dossier approprié
2. Crée les composants spécifiques à la page
3. Ajoute à la navigation si nécessaire
4. Génère les types TypeScript
5. Crée un test basique

## Structure créée

```
frontend/app/(dashboard)/<path>/
├── page.tsx           # Page principale
├── loading.tsx        # Loading state
├── error.tsx          # Error boundary
└── _components/       # Composants locaux (optionnel)
    └── ...
```

## Template page.tsx

```tsx
import { Suspense } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { PageContainer } from '@/components/layout/page-container';

export const metadata = {
  title: '<Page Title> | Vectra',
  description: '<Page description>',
};

export default async function PageName() {
  return (
    <PageContainer>
      <PageHeader
        title="<Title>"
        description="<Description>"
        breadcrumbs={[
          { label: 'Dashboard', href: '/dashboard' },
          { label: '<Current>' },
        ]}
        actions={
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Action
          </Button>
        }
      />
      
      <Suspense fallback={<Loading />}>
        <Content />
      </Suspense>
    </PageContainer>
  );
}

function Loading() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, i) => (
        <Skeleton key={i} className="h-24" />
      ))}
    </div>
  );
}

async function Content() {
  const data = await getData();
  return <PageContent data={data} />;
}
```

## Règles de Design

1. Utiliser les tokens du Design System
2. Mobile-first (commencer par mobile)
3. Dark mode compatible
4. Accessible (WCAG 2.1 AA)
5. Performance (Suspense + streaming)

## Checklist

- [ ] Page créée avec layout correct
- [ ] Breadcrumbs configurés
- [ ] Loading state avec Skeleton
- [ ] Error boundary
- [ ] Responsive (mobile, tablet, desktop)
- [ ] Dark mode testé
- [ ] Types TypeScript
```

---

## 2. create-component.md

```markdown
# Créer un Composant UI

## Usage
```
/create-component <category>/<name>
```

Categories:
- `ui/` - Composants primitifs (Shadcn style)
- `layout/` - Composants de structure
- `features/<module>/` - Composants métier
- `shared/` - Composants partagés

Exemples:
- `/create-component ui/toggle`
- `/create-component features/leads/lead-filters`

## Template Component

```tsx
'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const componentVariants = cva(
  'base-classes-here',
  {
    variants: {
      variant: {
        default: 'default-variant-classes',
        primary: 'primary-variant-classes',
      },
      size: {
        sm: 'size-sm-classes',
        md: 'size-md-classes',
        lg: 'size-lg-classes',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

export interface ComponentProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof componentVariants> {}

const Component = React.forwardRef<HTMLDivElement, ComponentProps>(
  ({ className, variant, size, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(componentVariants({ variant, size, className }))}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Component.displayName = 'Component';

export { Component, componentVariants };
```

## Checklist

- [ ] Variants définis avec CVA
- [ ] Types TypeScript complets
- [ ] forwardRef pour composants DOM
- [ ] Dark mode compatible
- [ ] États interactifs
- [ ] Accessible
```

---

## 3. create-form.md

```markdown
# Créer un Formulaire

## Usage
```
/create-form <name>
```

## Template Form

```tsx
'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { FormField } from '@/components/ui/form-field';

const formSchema = z.object({
  field1: z.string().min(1, 'Requis'),
  field2: z.string().email('Email invalide'),
});

type FormData = z.infer<typeof formSchema>;

interface FormProps {
  defaultValues?: Partial<FormData>;
  onSubmit: (data: FormData) => Promise<void>;
  onCancel?: () => void;
}

export function Form({ defaultValues, onSubmit, onCancel }: FormProps) {
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: { field1: '', field2: '', ...defaultValues },
  });

  const handleSubmit = async (data: FormData) => {
    try {
      setIsSubmitting(true);
      await onSubmit(data);
      toast.success('Sauvegardé');
    } catch (error) {
      toast.error('Une erreur est survenue');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
      <FormField
        label="Field 1"
        error={form.formState.errors.field1?.message}
        required
        {...form.register('field1')}
      />
      
      <div className="flex justify-end gap-3">
        {onCancel && (
          <Button type="button" variant="ghost" onClick={onCancel}>
            Annuler
          </Button>
        )}
        <Button type="submit" loading={isSubmitting}>
          Sauvegarder
        </Button>
      </div>
    </form>
  );
}
```
```

---

## 4. create-modal.md

```markdown
# Créer une Modal

## Usage
```
/create-modal <name>
```

## Template Modal

```tsx
'use client';

import * as React from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

interface ModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm?: () => void | Promise<void>;
}

export function Modal({ open, onOpenChange, onConfirm }: ModalProps) {
  const [isLoading, setIsLoading] = React.useState(false);

  const handleConfirm = async () => {
    if (!onConfirm) return;
    
    try {
      setIsLoading(true);
      await onConfirm();
      onOpenChange(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Titre</DialogTitle>
          <DialogDescription>Description.</DialogDescription>
        </DialogHeader>

        <div className="py-4">
          {/* Contenu */}
        </div>

        <DialogFooter>
          <DialogClose asChild>
            <Button variant="ghost">Annuler</Button>
          </DialogClose>
          <Button onClick={handleConfirm} loading={isLoading}>
            Confirmer
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export function useModal() {
  const [open, setOpen] = React.useState(false);
  return {
    open,
    onOpenChange: setOpen,
    show: () => setOpen(true),
    hide: () => setOpen(false),
  };
}
```
```

---

## 5. style-guide.md

```markdown
# Style Guide Reference

## Usage
```
/style-guide
```

## Quick Reference

### Colors
```
Primary:    #2E5BFF
Accent:     #FF9F43
Success:    #22C55E
Warning:    #F59E0B
Error:      #EF4444
```

### Typography
```
H1:    36px / semibold
H2:    30px / semibold
H3:    24px / semibold
H4:    20px / medium
Body:  16px / normal
Small: 14px / normal
```

### Spacing (8px grid)
```
1: 4px    4: 16px   8: 32px
2: 8px    5: 20px   12: 48px
3: 12px   6: 24px   16: 64px
```

### Border Radius
```
sm: 4px   lg: 8px
md: 6px   xl: 12px
```

### Component Patterns

**Button:**
```tsx
<Button variant="primary" size="md">
  <Icon className="h-4 w-4 mr-2" />
  Label
</Button>
```

**Card:**
```tsx
<Card className="p-6">
  <h3 className="font-medium text-text-primary">Title</h3>
  <p className="text-sm text-text-secondary">Content</p>
</Card>
```

**Stats:**
```tsx
<div className="text-3xl font-semibold">{value}</div>
<div className="text-sm text-text-secondary">Label</div>
```
```

---

## 6. check-accessibility.md

```markdown
# Check Accessibility

## Usage
```
/check-accessibility
```

## Checklist WCAG 2.1 AA

- [ ] Contraste ≥ 4.5:1 (texte) ou ≥ 3:1 (large)
- [ ] Alt text sur images
- [ ] Navigation clavier complète
- [ ] Focus visible
- [ ] Labels sur inputs
- [ ] ARIA correct
- [ ] Skip to content

## Common Fixes

### Focus ring
```tsx
className="focus-visible:ring-2 focus-visible:ring-primary-500"
```

### Icon button
```tsx
<button aria-label="Close">
  <X aria-hidden="true" />
</button>
```

### Form field
```tsx
<label>
  <span>Email</span>
  <input aria-describedby="email-error" />
</label>
{error && <p id="email-error" role="alert">{error}</p>}
```
```

---

## 7. responsive-check.md

```markdown
# Check Responsive

## Usage
```
/responsive-check
```

## Breakpoints

| Name | Width | Usage |
|------|-------|-------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablet |
| lg | 1024px | Laptop |
| xl | 1280px | Desktop |
| 2xl | 1536px | Large desktop |

## Checklist

### Mobile (< 768px)
- [ ] Sidebar cachée
- [ ] Bottom nav visible
- [ ] Cards en colonne
- [ ] Touch targets ≥ 44px

### Tablet (768-1024px)
- [ ] Mini sidebar (64px)
- [ ] 2 colonnes

### Desktop (> 1024px)
- [ ] Full sidebar (256px)
- [ ] 3-4 colonnes

## Patterns

```tsx
// Grid responsive
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

// Hide/Show
<div className="hidden md:block">Desktop</div>
<div className="md:hidden">Mobile</div>
```
```

---

## INSTALLATION

```bash
mkdir -p .claude/commands
cd .claude/commands

# Créer les fichiers
touch create-page.md create-component.md create-form.md
touch create-modal.md style-guide.md
touch check-accessibility.md responsive-check.md
```

---

*14 Janvier 2026*
