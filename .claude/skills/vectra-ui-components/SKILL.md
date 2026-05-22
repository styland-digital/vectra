---
name: vectra-ui-components
description: Production-ready Vectra UI components following premium SaaS aesthetic. Use when building any UI component, page, or layout.
---

# Vectra UI Component Library

## Base Configuration

### globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Light mode */
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 98%;
    --card-foreground: 240 10% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;
    --primary: 217 91% 60%;
    --primary-foreground: 0 0% 100%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84% 60%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 217 91% 60%;
  }

  .dark {
    --background: 240 6% 4%;
    --foreground: 0 0% 98%;
    --card: 240 6% 6%;
    --card-foreground: 0 0% 98%;
    --popover: 240 6% 6%;
    --popover-foreground: 0 0% 98%;
    --primary: 217 91% 60%;
    --primary-foreground: 0 0% 100%;
    --secondary: 240 5% 14%;
    --secondary-foreground: 0 0% 98%;
    --muted: 240 5% 14%;
    --muted-foreground: 240 5% 64.9%;
    --accent: 240 5% 14%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62% 50%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5% 12%;
    --input: 240 5% 12%;
    --ring: 217 91% 60%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground antialiased;
    font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  }
}

/* Scrollbar - Minimal */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: hsl(var(--muted));
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground) / 0.3);
}
```

### tailwind.config.ts

```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      fontSize: {
        "2xs": ["0.6875rem", { lineHeight: "1rem" }],  // 11px
        xs: ["0.75rem", { lineHeight: "1rem" }],       // 12px
        sm: ["0.8125rem", { lineHeight: "1.25rem" }],  // 13px
        base: ["0.875rem", { lineHeight: "1.5rem" }],  // 14px - DEFAULT
        lg: ["1rem", { lineHeight: "1.5rem" }],        // 16px
        xl: ["1.125rem", { lineHeight: "1.75rem" }],   // 18px
        "2xl": ["1.25rem", { lineHeight: "1.75rem" }], // 20px
        "3xl": ["1.5rem", { lineHeight: "2rem" }],     // 24px
        "4xl": ["1.875rem", { lineHeight: "2.25rem" }],// 30px
      },
      borderRadius: {
        lg: "8px",
        md: "6px",
        sm: "4px",
      },
      animation: {
        "fade-in": "fade-in 0.15s ease-out",
        "slide-up": "slide-up 0.15s ease-out",
      },
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        "slide-up": {
          "0%": { opacity: "0", transform: "translateY(4px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
```

---

## Core Components

### Button

```tsx
// components/ui/button.tsx
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-zinc-100 text-zinc-900 hover:bg-white dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-white",
        secondary: "border border-zinc-200 bg-transparent text-zinc-700 hover:bg-zinc-100 dark:border-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-zinc-100",
        ghost: "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100",
        destructive: "bg-red-500/10 text-red-600 hover:bg-red-500/20 dark:text-red-400",
        link: "text-zinc-600 underline-offset-4 hover:underline dark:text-zinc-400",
      },
      size: {
        default: "h-8 px-3 rounded-md",
        sm: "h-7 px-2 text-xs rounded",
        lg: "h-9 px-4 rounded-md",
        icon: "h-8 w-8 rounded-md",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

### Card

```tsx
// components/ui/card.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border border-zinc-200 bg-white dark:border-zinc-800/50 dark:bg-zinc-900/50",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1 p-5 pb-0", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn("text-base font-medium text-zinc-900 dark:text-zinc-100", className)}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-zinc-500 dark:text-zinc-400", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-5", className)} {...props} />
))
CardContent.displayName = "CardContent"

export { Card, CardHeader, CardTitle, CardDescription, CardContent }
```

### Input

```tsx
// components/ui/input.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-9 w-full rounded-md border border-zinc-200 bg-white px-3 text-sm text-zinc-900 transition-colors duration-150",
          "placeholder:text-zinc-400",
          "focus:outline-none focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400",
          "disabled:cursor-not-allowed disabled:opacity-50",
          "dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-100 dark:placeholder:text-zinc-500",
          "dark:focus:border-zinc-600 dark:focus:ring-zinc-600",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
```

### Badge

```tsx
// components/ui/badge.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded px-2 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300",
        success: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
        warning: "bg-amber-500/10 text-amber-600 dark:text-amber-400",
        error: "bg-red-500/10 text-red-600 dark:text-red-400",
        info: "bg-blue-500/10 text-blue-600 dark:text-blue-400",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
```

---

## Layout Components

### Sidebar (Linear-style)

```tsx
// components/layout/sidebar.tsx
"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Target,
  Users,
  Mail,
  Calendar,
  BarChart3,
  Settings,
} from "lucide-react"

const navigation = [
  { name: "Overview", href: "/", icon: LayoutDashboard },
  { name: "Campaigns", href: "/campaigns", icon: Target },
  { name: "Leads", href: "/leads", icon: Users },
  { name: "Emails", href: "/emails", icon: Mail },
  { name: "Meetings", href: "/meetings", icon: Calendar },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="flex h-full w-60 flex-col bg-zinc-950">
      {/* Logo */}
      <div className="flex h-14 items-center gap-2 border-b border-zinc-800/50 px-4">
        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-white">
          <span className="text-sm font-semibold text-zinc-900">V</span>
        </div>
        <span className="text-sm font-medium text-zinc-100">Vectra</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-0.5 p-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors duration-150",
                isActive
                  ? "bg-zinc-800/70 text-white"
                  : "text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200"
              )}
            >
              <item.icon className="h-4 w-4" />
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-zinc-800/50 p-2">
        <Link
          href="/settings"
          className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-zinc-400 transition-colors hover:bg-zinc-800/50 hover:text-zinc-200"
        >
          <Settings className="h-4 w-4" />
          <span>Settings</span>
        </Link>
      </div>
    </div>
  )
}
```

### Page Header

```tsx
// components/layout/page-header.tsx
import { Button } from "@/components/ui/button"

interface PageHeaderProps {
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
}

export function PageHeader({ title, description, action }: PageHeaderProps) {
  return (
    <div className="mb-6 flex items-center justify-between">
      <div>
        <h1 className="text-xl font-semibold text-zinc-900 dark:text-white">
          {title}
        </h1>
        {description && (
          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            {description}
          </p>
        )}
      </div>
      {action && (
        <Button onClick={action.onClick}>{action.label}</Button>
      )}
    </div>
  )
}
```

---

## Data Display

### Stats Card

```tsx
// components/ui/stats-card.tsx
import { cn } from "@/lib/utils"
import { ArrowUp, ArrowDown } from "lucide-react"

interface StatsCardProps {
  title: string
  value: string | number
  change?: {
    value: number
    label: string
  }
  className?: string
}

export function StatsCard({ title, value, change, className }: StatsCardProps) {
  const isPositive = change && change.value > 0

  return (
    <div
      className={cn(
        "rounded-lg border border-zinc-200 bg-white p-5 dark:border-zinc-800/50 dark:bg-zinc-900/50",
        className
      )}
    >
      <p className="text-sm text-zinc-500 dark:text-zinc-400">{title}</p>
      <p className="mt-1 text-2xl font-semibold text-zinc-900 dark:text-white">
        {value}
      </p>
      {change && (
        <div className="mt-2 flex items-center gap-1 text-xs">
          {isPositive ? (
            <ArrowUp className="h-3 w-3 text-emerald-500" />
          ) : (
            <ArrowDown className="h-3 w-3 text-red-500" />
          )}
          <span
            className={cn(
              isPositive ? "text-emerald-500" : "text-red-500"
            )}
          >
            {Math.abs(change.value)}%
          </span>
          <span className="text-zinc-400">{change.label}</span>
        </div>
      )}
    </div>
  )
}
```

### Data Table

```tsx
// components/ui/data-table.tsx
import { cn } from "@/lib/utils"

interface Column<T> {
  key: keyof T
  header: string
  render?: (value: T[keyof T], row: T) => React.ReactNode
}

interface DataTableProps<T> {
  columns: Column<T>[]
  data: T[]
  onRowClick?: (row: T) => void
}

export function DataTable<T extends { id: string }>({
  columns,
  data,
  onRowClick,
}: DataTableProps<T>) {
  return (
    <div className="overflow-hidden rounded-lg border border-zinc-200 dark:border-zinc-800/50">
      <table className="w-full">
        <thead>
          <tr className="border-b border-zinc-200 bg-zinc-50 dark:border-zinc-800/50 dark:bg-zinc-900/50">
            {columns.map((col) => (
              <th
                key={String(col.key)}
                className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400"
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-200 bg-white dark:divide-zinc-800/30 dark:bg-zinc-900/30">
          {data.map((row) => (
            <tr
              key={row.id}
              onClick={() => onRowClick?.(row)}
              className={cn(
                "transition-colors duration-150",
                onRowClick && "cursor-pointer hover:bg-zinc-50 dark:hover:bg-zinc-800/30"
              )}
            >
              {columns.map((col) => (
                <td
                  key={String(col.key)}
                  className="px-4 py-3 text-sm text-zinc-700 dark:text-zinc-300"
                >
                  {col.render
                    ? col.render(row[col.key], row)
                    : String(row[col.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

---

## Empty States

```tsx
// components/ui/empty-state.tsx
import { LucideIcon } from "lucide-react"
import { Button } from "@/components/ui/button"

interface EmptyStateProps {
  icon: LucideIcon
  title: string
  description: string
  action?: {
    label: string
    onClick: () => void
  }
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-zinc-100 dark:bg-zinc-800">
        <Icon className="h-6 w-6 text-zinc-400" />
      </div>
      <h3 className="mt-4 text-sm font-medium text-zinc-900 dark:text-white">
        {title}
      </h3>
      <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
        {description}
      </p>
      {action && (
        <Button onClick={action.onClick} className="mt-4" variant="secondary">
          {action.label}
        </Button>
      )}
    </div>
  )
}
```

---

## Usage Examples

### Campaign List Page

```tsx
// app/(dashboard)/campaigns/page.tsx
import { PageHeader } from "@/components/layout/page-header"
import { DataTable } from "@/components/ui/data-table"
import { Badge } from "@/components/ui/badge"
import { Campaign } from "@/lib/types"

const columns = [
  { key: "name" as const, header: "Name" },
  {
    key: "status" as const,
    header: "Status",
    render: (value: string) => (
      <Badge variant={value === "active" ? "success" : "default"}>
        {value}
      </Badge>
    ),
  },
  { key: "leadsCount" as const, header: "Leads" },
  { key: "createdAt" as const, header: "Created" },
]

export default async function CampaignsPage() {
  const campaigns = await getCampaigns()

  return (
    <>
      <PageHeader
        title="Campaigns"
        description="Manage your outreach campaigns"
        action={{ label: "New Campaign", onClick: () => {} }}
      />
      <DataTable columns={columns} data={campaigns} />
    </>
  )
}
```

---

## Patterns d'erreur et validation

### Formulaire auth complet (pattern de référence)

```tsx
// Règle : erreur API en haut (Alert), erreurs champs en bas (p tag), clearError au onChange
<Formik validate={toFormikValidate(createXxxSchema(t))} onSubmit={handleSubmit}>
  {({ errors, touched }) => (
    <Form onChange={() => { if (error) clearError() }}>
      <CardContent className="space-y-4 text-left">
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
            >
              <Alert variant="destructive">
                <AlertDescription>
                  {error?.startsWith("auth.") ? t(error) : error}
                </AlertDescription>
              </Alert>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="space-y-2">
          <Label htmlFor="email">{t("...")}</Label>
          <Field name="email">
            {({ field }: FieldProps) => (
              <Input {...field} id="email" type="email" disabled={isLoading} />
            )}
          </Field>
          {touched.email && errors.email && (
            <p className="text-xs text-[var(--color-error-500)]">{errors.email}</p>
          )}
        </div>
      </CardContent>
    </Form>
  )}
</Formik>
```

### Hiérarchie typographique — tokens obligatoires

| Élément | Token | Jamais |
|---------|-------|--------|
| Titre page | `text-h1`, `text-h2` | `text-3xl`, `text-4xl` |
| Titre card | `text-h3` | `text-2xl`, `text-xl` |
| Sous-titre card | `text-h4` | `text-lg` |
| Corps | `text-body`, `text-body-sm` | `text-sm`, `text-base` |
| Meta | `text-caption`, `text-overline` | `text-xs` |

### Couleurs sémantiques — règles absolues

```tsx
// ✅ Progress bar / indicateur
<div className="h-full bg-[var(--color-primary-500)] rounded-full" />

// ❌ JAMAIS
<div className="h-full bg-[var(--text-primary)] rounded-full" />

// ✅ Erreur champ
<p className="text-xs text-[var(--color-error-500)]">{errors.field}</p>

// ✅ Message succès
<div className="flex items-center gap-3 rounded-lg border border-[var(--color-success-500)] bg-[var(--color-success-500)]/10 p-4">
  <CheckCircle2 className="h-5 w-5 text-[var(--color-success-500)]" />
</div>
```

### Schéma i18n — règle absolue

```tsx
// ✅ TOUJOURS passer t
validate={toFormikValidate(createLoginSchema(t))}

// ❌ JAMAIS utiliser le schéma brut
validate={toFormikValidate(loginSchema)}
```

> Voir `.claude/rules/UI_CONVENTIONS.md` pour la checklist complète avant livraison.

---

*These components follow Vectra's premium SaaS aesthetic - calm, confident, expensive.*
