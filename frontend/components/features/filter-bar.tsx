"use client"

import type { ReactNode } from "react"
import { Button } from "@/components/ui/button"
import { X } from "lucide-react"
import { useTranslation } from "@/lib/i18n"

interface FilterBarProps {
  children: ReactNode
  onClear?: () => void
  showClear?: boolean
}

export function FilterBar({ children, onClear, showClear }: FilterBarProps) {
  const { t } = useTranslation()

  return (
    <div className="flex flex-wrap items-center gap-3">
      {children}
      {showClear && onClear && (
        <Button variant="ghost" size="sm" onClick={onClear} className="h-9">
          <X className="h-4 w-4 mr-1" />
          {t("common.clearFilters")}
        </Button>
      )}
    </div>
  )
}
