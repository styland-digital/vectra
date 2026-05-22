"use client"

import type { ReactNode } from "react"
import { Button } from "@/components/ui/button"
import { SlidersHorizontal, X } from "lucide-react"
import { useTranslation } from "@/lib/i18n"

interface FilterBarProps {
  children: ReactNode
  onClear?: () => void
  showClear?: boolean
  /** Optional section title shown left of the filters */
  title?: string
}

export function FilterBar({ children, onClear, showClear, title }: FilterBarProps) {
  const { t } = useTranslation()

  return (
    <div className="space-y-2">
      {title && (
        <div className="flex items-center gap-1.5">
          <SlidersHorizontal className="h-3.5 w-3.5 text-[var(--text-muted)]" />
          <span className="text-caption font-semibold uppercase tracking-wider text-[var(--text-muted)]">
            {title}
          </span>
        </div>
      )}
      <div className="flex flex-wrap items-center gap-3">
        {children}
        {showClear && onClear && (
          <Button variant="ghost" size="sm" onClick={onClear} className="h-9 text-[var(--text-muted)]">
            <X className="h-3.5 w-3.5 mr-1.5" />
            {t("common.clearFilters")}
          </Button>
        )}
      </div>
    </div>
  )
}
