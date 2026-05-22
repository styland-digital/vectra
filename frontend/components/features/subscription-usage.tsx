"use client"

import { VectraDonutChart } from "@/components/charts/vectra-donut-chart"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface SubscriptionUsageProps {
  leadsUsed: number
  leadsLimit: number
  plan: string
  className?: string
}

export function SubscriptionUsage({ leadsUsed, leadsLimit, plan, className }: SubscriptionUsageProps) {
  const percentage = leadsLimit > 0 ? Math.min(Math.round((leadsUsed / leadsLimit) * 100), 100) : 0
  const remaining = Math.max(leadsLimit - leadsUsed, 0)
  const isWarning = percentage >= 80
  const isCritical = percentage >= 95

  const color = isCritical
    ? "var(--color-error-500)"
    : isWarning
      ? "var(--color-warning-500)"
      : "var(--color-primary-500)"

  return (
    <div className={cn("flex flex-col items-center gap-4", className)}>
      {/* Plan badge */}
      <div className="flex items-center justify-between w-full">
        <span className="text-body-sm text-[var(--text-secondary)]">Subscription</span>
        <Badge
          variant="secondary"
          className="bg-[var(--color-vectra-yellow-100)] text-[var(--color-vectra-yellow-700)] hover:bg-[var(--color-vectra-yellow-200)] border-0 capitalize"
        >
          {plan}
        </Badge>
      </div>

      {/* Donut */}
      <VectraDonutChart
        value={leadsUsed}
        max={leadsLimit}
        label="Leads"
        color={color}
        size={148}
      />

      {/* Stats */}
      <div className="w-full space-y-2">
        <div className="flex items-center justify-between text-body-sm">
          <span className="text-[var(--text-muted)]">Used</span>
          <span className="font-medium text-[var(--text-primary)] tabular-nums">
            {leadsUsed.toLocaleString()}
          </span>
        </div>
        <div className="flex items-center justify-between text-body-sm">
          <span className="text-[var(--text-muted)]">Remaining</span>
          <span
            className={cn(
              "font-medium tabular-nums",
              isCritical
                ? "text-[var(--color-error-600)]"
                : isWarning
                  ? "text-[var(--color-warning-600)]"
                  : "text-[var(--text-primary)]"
            )}
          >
            {remaining.toLocaleString()}
          </span>
        </div>
        <div className="flex items-center justify-between text-body-sm">
          <span className="text-[var(--text-muted)]">Limit</span>
          <span className="text-[var(--text-muted)] tabular-nums">{leadsLimit.toLocaleString()}</span>
        </div>
      </div>
    </div>
  )
}
