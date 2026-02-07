"use client"

import { cn } from "@/lib/utils"
import { useTranslation } from "@/lib/i18n"

type StatusType = "campaign" | "lead" | "email" | "meeting"

const statusColors: Record<string, string> = {
  // Campaign
  draft: "bg-[var(--color-neutral-500)]/10 text-[var(--color-neutral-400)] border-[var(--color-neutral-500)]/20",
  active: "bg-[var(--color-success-500)]/10 text-[var(--color-success-500)] border-[var(--color-success-500)]/20",
  paused: "bg-[var(--color-warning-500)]/10 text-[var(--color-warning-500)] border-[var(--color-warning-500)]/20",
  completed: "bg-[var(--color-info-500)]/10 text-[var(--color-info-500)] border-[var(--color-info-500)]/20",
  archived: "bg-[var(--color-neutral-500)]/10 text-[var(--color-neutral-500)] border-[var(--color-neutral-500)]/20",
  // Lead
  new: "bg-[var(--color-info-500)]/10 text-[var(--color-info-500)] border-[var(--color-info-500)]/20",
  enriched: "bg-[var(--color-primary-400)]/10 text-[var(--color-primary-400)] border-[var(--color-primary-400)]/20",
  qualified: "bg-[var(--color-success-500)]/10 text-[var(--color-success-500)] border-[var(--color-success-500)]/20",
  nurture: "bg-[var(--color-warning-500)]/10 text-[var(--color-warning-500)] border-[var(--color-warning-500)]/20",
  rejected: "bg-[var(--color-error-500)]/10 text-[var(--color-error-500)] border-[var(--color-error-500)]/20",
  contacted: "bg-[var(--color-info-500)]/10 text-[var(--color-info-500)] border-[var(--color-info-500)]/20",
  // Email
  pending: "bg-[var(--color-warning-500)]/10 text-[var(--color-warning-500)] border-[var(--color-warning-500)]/20",
  approved: "bg-[var(--color-success-500)]/10 text-[var(--color-success-500)] border-[var(--color-success-500)]/20",
  sent: "bg-[var(--color-info-500)]/10 text-[var(--color-info-500)] border-[var(--color-info-500)]/20",
  opened: "bg-[var(--color-info-500)]/10 text-[var(--color-info-500)] border-[var(--color-info-500)]/20",
  clicked: "bg-[var(--color-primary-400)]/10 text-[var(--color-primary-400)] border-[var(--color-primary-400)]/20",
  bounced: "bg-[var(--color-error-500)]/10 text-[var(--color-error-500)] border-[var(--color-error-500)]/20",
  // Meeting
  scheduled: "bg-[var(--color-info-500)]/10 text-[var(--color-info-500)] border-[var(--color-info-500)]/20",
  no_show: "bg-[var(--color-error-500)]/10 text-[var(--color-error-500)] border-[var(--color-error-500)]/20",
}

interface StatusBadgeProps {
  status: string
  type: StatusType
  className?: string
}

export function StatusBadge({ status, type, className }: StatusBadgeProps) {
  const { t } = useTranslation()
  const colorClass = statusColors[status] ?? "bg-[var(--color-neutral-500)]/10 text-[var(--color-neutral-400)] border-[var(--color-neutral-500)]/20"

  const labelKey = `${type === "campaign" ? "campaigns" : type === "lead" ? "leads" : type === "email" ? "emails" : "meetings"}.status.${status}`
  const label = t(labelKey)
  const displayLabel = label === labelKey ? status : label

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium capitalize transition-colors duration-150",
        colorClass,
        className
      )}
    >
      {displayLabel}
    </span>
  )
}
