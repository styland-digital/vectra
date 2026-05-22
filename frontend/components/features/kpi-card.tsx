"use client"

import { type LucideIcon, TrendingUp, TrendingDown, Minus } from "lucide-react"
import { cn } from "@/lib/utils"

export type KPITrendDirection = "up" | "down" | "neutral"

export interface KPITrend {
  direction: KPITrendDirection
  /** e.g. "+12%" or "-5%" or "vs last month" */
  label: string
}

export type KPIImportance = "high" | "medium" | "low"

export interface KPICardProps {
  /** Label au-dessus de la valeur (ex: "Prospects générés") */
  label: string
  /** Valeur principale (nombre, string ou ReactNode) */
  value: React.ReactNode
  /** Tendance optionnelle (flèche + texte) */
  trend?: KPITrend
  /** Importance visuelle: high = plus mis en avant */
  importance?: KPIImportance
  /** Description secondaire sous la tendance (ex: "Ce mois-ci") */
  description?: string
  /** Icône optionnelle à droite */
  icon?: LucideIcon
  /** Couleur sémantique de l'icône (optionnel): primary, success, error, warning, accent, vectra-yellow */
  iconColor?: "primary" | "success" | "error" | "warning" | "accent" | "vectra-yellow" | "muted"
  /** Variante d'affichage */
  variant?: "default" | "compact" | "elevated"
  className?: string
  /** Lien optionnel (rend la card cliquable) */
  href?: string
  /** Mini sparkline data (array of numbers) for a background chart */
  sparkline?: number[]
  /** Progress bar (0-100) shown below the value */
  progress?: { value: number; max?: number; label?: string }
  /** Optional secondary value shown next to main value (e.g., "/500") */
  secondaryValue?: string
}

const iconColorMap: Record<NonNullable<KPICardProps["iconColor"]>, string> = {
  primary: "text-[var(--color-primary-500)]",
  success: "text-[var(--color-success-500)]",
  error: "text-[var(--color-error-500)]",
  warning: "text-[var(--color-warning-500)]",
  accent: "text-[var(--color-accent-500)]",
  "vectra-yellow": "text-[var(--color-vectra-yellow-500)]",
  muted: "text-[var(--text-muted)]",
}

const trendIconMap = {
  up: TrendingUp,
  down: TrendingDown,
  neutral: Minus,
}

function Sparkline({ data }: { data: number[] }) {
  if (data.length < 2) return null
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1
  const points = data
    .map((v, i) => `${i},${1 - (v - min) / range}`)
    .join(" ")

  return (
    <div className="absolute bottom-0 left-0 right-0 h-12 overflow-hidden rounded-b-xl opacity-[0.08] pointer-events-none">
      <svg
        viewBox={`0 0 ${data.length - 1} 1`}
        preserveAspectRatio="none"
        className="h-full w-full"
      >
        <polyline
          points={points}
          fill="none"
          stroke="currentColor"
          strokeWidth="0.05"
          className="text-[var(--text-primary)]"
        />
      </svg>
    </div>
  )
}

export function KPICard({
  label,
  value,
  trend,
  importance = "medium",
  description,
  icon: Icon,
  iconColor = "muted",
  variant = "default",
  className,
  href,
  sparkline,
  progress,
  secondaryValue,
}: KPICardProps) {
  const TrendIcon = trend ? trendIconMap[trend.direction] : null
  const isCompact = variant === "compact"
  const isElevated = variant === "elevated"

  const content = (
    <>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1 space-y-1">
          <p className="text-body-sm text-[var(--text-secondary)] truncate">{label}</p>
          <p
            className={cn(
              "font-semibold tabular-nums text-[var(--text-primary)]",
              importance === "high" && "text-h2",
              importance === "medium" && "text-xl",
              importance === "low" && "text-lg"
            )}
          >
            {value}
            {secondaryValue && (
              <span className="text-body-sm font-normal text-[var(--text-muted)]">{secondaryValue}</span>
            )}
          </p>
          {(trend || description) && (
            <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5">
              {trend && TrendIcon && (
                <span
                  className={cn(
                    "inline-flex items-center gap-1 text-caption font-medium rounded-full px-1.5 py-0.5",
                    trend.direction === "up" && "bg-[var(--color-success-500)]/10 text-[var(--color-success-600)]",
                    trend.direction === "down" && "bg-[var(--color-error-500)]/10 text-[var(--color-error-600)]",
                    trend.direction === "neutral" && "bg-[var(--surface-secondary)] text-[var(--text-muted)]"
                  )}
                >
                  <TrendIcon className="h-3 w-3 shrink-0" />
                  {trend.label}
                </span>
              )}
              {description && (
                <span className="text-caption text-[var(--text-muted)]">{description}</span>
              )}
            </div>
          )}
          {progress && (
            <div className="space-y-1 pt-1">
              <div className="h-1.5 w-full bg-[var(--surface-secondary)] rounded-full overflow-hidden">
                <div
                  className="h-full bg-[var(--color-primary-500)] rounded-full transition-all duration-500"
                  style={{ width: `${Math.min((progress.value / (progress.max ?? 100)) * 100, 100)}%` }}
                />
              </div>
              {progress.label && (
                <span className="text-caption text-[var(--text-muted)]">{progress.label}</span>
              )}
            </div>
          )}
        </div>
        {Icon && (
          <div
            className={cn(
              "shrink-0 rounded-lg flex items-center justify-center border border-[var(--border-secondary)]",
              isCompact ? "h-9 w-9" : "h-10 w-10",
              "bg-[var(--surface-secondary)]"
            )}
          >
            <Icon className={cn("h-5 w-5", iconColorMap[iconColor])} />
          </div>
        )}
      </div>
      {sparkline && sparkline.length >= 2 && <Sparkline data={sparkline} />}
    </>
  )

  const cardClass = cn(
    "relative overflow-hidden rounded-xl border border-[var(--border-primary)] bg-[var(--surface-primary)] transition-colors duration-200",
    isCompact && "p-4",
    !isCompact && "p-5",
    isElevated && "hover:border-[var(--border-hover)]",
    !isElevated && "hover:border-[var(--border-hover)]",
    className
  )

  if (href) {
    return (
      <a href={href} className={cn("block", cardClass)}>
        {content}
      </a>
    )
  }

  return <div className={cardClass}>{content}</div>
}
