"use client"

import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { useTranslation } from "@/lib/i18n"
import type { Pagination as PaginationType } from "@/types"

interface PaginationProps {
  pagination: PaginationType
  onPageChange: (skip: number) => void
}

export function Pagination({ pagination, onPageChange }: PaginationProps) {
  const { t } = useTranslation()
  const { total, skip, limit, has_more } = pagination
  const currentPage = Math.floor(skip / limit) + 1
  const totalPages = Math.ceil(total / limit)
  const showingFrom = total === 0 ? 0 : skip + 1
  const showingTo = Math.min(skip + limit, total)

  return (
    <div className="flex items-center justify-between py-4">
      <p className="text-sm text-muted-foreground">
        {t("common.showing")} {showingFrom}-{showingTo} {t("common.of")} {total}
      </p>
      <div className="flex items-center space-x-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(Math.max(0, skip - limit))}
          disabled={skip === 0}
        >
          <ChevronLeft className="h-4 w-4 mr-1" />
          {t("common.previous")}
        </Button>
        <span className="text-sm text-muted-foreground">
          {currentPage} / {totalPages || 1}
        </span>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(skip + limit)}
          disabled={!has_more}
        >
          {t("common.next")}
          <ChevronRight className="h-4 w-4 ml-1" />
        </Button>
      </div>
    </div>
  )
}
