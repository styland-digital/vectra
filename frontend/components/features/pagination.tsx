"use client"

import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react"
import { cn } from "@/lib/utils"
import { useTranslation } from "@/lib/i18n"
import type { Pagination as PaginationType } from "@/types"

interface PaginationProps {
  pagination: PaginationType
  onPageChange: (skip: number) => void
  showPageNumbers?: boolean
}

function getPageWindow(current: number, total: number): (number | "...")[] {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const pages: (number | "...")[] = []
  const left = Math.max(2, current - 1)
  const right = Math.min(total - 1, current + 1)

  pages.push(1)
  if (left > 2) pages.push("...")
  for (let p = left; p <= right; p++) pages.push(p)
  if (right < total - 1) pages.push("...")
  pages.push(total)

  return pages
}

export function Pagination({ pagination, onPageChange, showPageNumbers = true }: PaginationProps) {
  const { t } = useTranslation()
  const { total, skip, limit, has_more } = pagination
  const currentPage = Math.floor(skip / limit) + 1
  const totalPages = Math.max(1, Math.ceil(total / limit))
  const showingFrom = total === 0 ? 0 : skip + 1
  const showingTo = Math.min(skip + limit, total)

  const goToPage = (page: number) => onPageChange((page - 1) * limit)

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-3 py-4">
      <p className="text-body-sm text-[var(--text-muted)] order-2 sm:order-1">
        {t("common.showing")} {showingFrom}–{showingTo} {t("common.of")} {total}
      </p>

      <div className="flex items-center gap-1 order-1 sm:order-2">
        {/* First page */}
        <Button
          variant="ghost"
          size="sm"
          className="h-8 w-8 p-0 text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)]"
          onClick={() => goToPage(1)}
          disabled={skip === 0}
        >
          <ChevronsLeft className="h-4 w-4" />
        </Button>

        {/* Previous page */}
        <Button
          variant="ghost"
          size="sm"
          className="h-8 w-8 p-0 text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)]"
          onClick={() => onPageChange(Math.max(0, skip - limit))}
          disabled={skip === 0}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>

        {/* Page numbers */}
        {showPageNumbers && getPageWindow(currentPage, totalPages).map((page, i) =>
          page === "..." ? (
            <span
              key={`ellipsis-${i}`}
              className="h-8 w-8 flex items-center justify-center text-body-sm text-[var(--text-muted)] select-none"
            >
              …
            </span>
          ) : (
            <Button
              key={page}
              variant="ghost"
              size="sm"
              className={cn(
                "h-8 w-8 p-0 text-body-sm font-medium transition-colors duration-150",
                page === currentPage
                  ? "bg-[var(--color-primary-50)] text-[var(--color-primary-600)] hover:bg-[var(--color-primary-100)]"
                  : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)]"
              )}
              onClick={() => goToPage(page as number)}
            >
              {page}
            </Button>
          )
        )}

        {/* Next page */}
        <Button
          variant="ghost"
          size="sm"
          className="h-8 w-8 p-0 text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)]"
          onClick={() => onPageChange(skip + limit)}
          disabled={!has_more}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>

        {/* Last page */}
        <Button
          variant="ghost"
          size="sm"
          className="h-8 w-8 p-0 text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)]"
          onClick={() => goToPage(totalPages)}
          disabled={!has_more}
        >
          <ChevronsRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
