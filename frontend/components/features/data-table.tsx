"use client"

import type { ReactNode } from "react"
import type { LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Inbox, Plus } from "lucide-react"

// ─── Column definition ────────────────────────────────────────────────────────

export interface Column<T> {
  key: string
  header: string
  render: (item: T) => ReactNode
  className?: string
  /** Hide this column on screens smaller than the given breakpoint */
  hideBelow?: "sm" | "md" | "lg" | "xl"
  /** Text alignment for header and cells */
  align?: "left" | "center" | "right"
  /** Fixed column width (e.g. 'w-[100px]') */
  width?: string
}

interface DataTableProps<T> {
  columns: Column<T>[]
  data: T[]
  isLoading?: boolean
  emptyMessage?: string
  emptyDescription?: string
  emptyIcon?: LucideIcon
  emptyAction?: ReactNode
  onRowClick?: (item: T) => void
  rowClassName?: (item: T) => string
  /** Page offset for correct row numbering (e.g. page 2 with skip=10 → rows start at 11) */
  skip?: number
}

// ─── Column class helpers ─────────────────────────────────────────────────────

const hideMap: Record<NonNullable<Column<unknown>["hideBelow"]>, string> = {
  sm: "hidden sm:table-cell",
  md: "hidden md:table-cell",
  lg: "hidden lg:table-cell",
  xl: "hidden xl:table-cell",
}

const alignMap: Record<NonNullable<Column<unknown>["align"]>, string> = {
  left: "text-left",
  center: "text-center",
  right: "text-right",
}

function colClass<T>(col: Column<T>): string {
  return cn(
    col.className,
    col.hideBelow && hideMap[col.hideBelow],
    col.align && alignMap[col.align],
    col.width
  )
}

// ─── Inline skeleton bar ──────────────────────────────────────────────────────

function Skel({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "rounded-md bg-[var(--surface-secondary)] animate-vectra-skeleton",
        className
      )}
    />
  )
}

// ─── DataTable ────────────────────────────────────────────────────────────────

export function DataTable<T extends { id: string }>({
  columns,
  data,
  isLoading,
  emptyMessage = "No results",
  emptyDescription,
  emptyIcon: EmptyIcon = Inbox,
  emptyAction,
  onRowClick,
  rowClassName,
  skip = 0,
}: DataTableProps<T>) {
  const totalCols = columns.length + 1 // +1 for the # column

  const headerRow = (
    <TableRow className="border-b border-[var(--border-primary)] bg-[var(--surface-secondary)] hover:bg-[var(--surface-secondary)]">
      {/* # column */}
      <TableHead className="w-[52px] text-center px-4 py-3 text-caption font-semibold uppercase tracking-wider text-[var(--text-muted)]">
        #
      </TableHead>
      {columns.map((col) => (
        <TableHead
          key={col.key}
          className={cn(
            colClass(col),
            "py-3 text-caption font-semibold uppercase tracking-wider text-[var(--text-secondary)]"
          )}
        >
          {col.header}
        </TableHead>
      ))}
    </TableRow>
  )

  return (
    <div className="rounded-xl border border-[var(--border-primary)] overflow-hidden bg-[var(--surface-primary)]">
      <Table>
        <TableHeader>{headerRow}</TableHeader>

        <TableBody>
          {/* Loading skeleton rows */}
          {isLoading && Array.from({ length: 6 }).map((_, i) => (
            <TableRow
              key={i}
              className="border-b border-[var(--border-primary)] last:border-0 hover:bg-transparent"
            >
              {/* # skeleton */}
              <TableCell className="w-[52px] text-center px-4 py-4">
                <Skel className="h-3 w-4 mx-auto" />
              </TableCell>
              {columns.map((col, j) => (
                <TableCell key={col.key} className={cn(colClass(col), "py-4")}>
                  {j === 0 ? (
                    <div className="space-y-1.5">
                      <Skel className="h-4 w-[70%]" />
                      <Skel className="h-3 w-[45%]" />
                    </div>
                  ) : j === columns.length - 1 ? (
                    <Skel className="h-7 w-7 ml-auto rounded-md" />
                  ) : (
                    <Skel className="h-5 w-[80%]" />
                  )}
                </TableCell>
              ))}
            </TableRow>
          ))}

          {/* Empty state — spans all columns */}
          {!isLoading && data.length === 0 && (
            <TableRow className="hover:bg-transparent">
              <TableCell colSpan={totalCols} className="py-16 text-center">
                <div className="flex flex-col items-center gap-3">
                  <div className="h-12 w-12 rounded-full bg-[var(--surface-secondary)] flex items-center justify-center">
                    <EmptyIcon className="h-6 w-6 text-[var(--text-muted)]" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-body-sm font-medium text-[var(--text-primary)]">
                      {emptyMessage}
                    </p>
                    {emptyDescription && (
                      <p className="text-caption text-[var(--text-muted)] max-w-xs mx-auto">
                        {emptyDescription}
                      </p>
                    )}
                  </div>
                  {emptyAction && <div className="mt-1">{emptyAction}</div>}
                </div>
              </TableCell>
            </TableRow>
          )}

          {/* Data rows */}
          {!isLoading && data.map((item, index) => (
            <TableRow
              key={item.id}
              className={cn(
                "border-b border-[var(--border-primary)] last:border-0",
                "hover:bg-[var(--surface-hover)] transition-colors duration-150",
                onRowClick && "cursor-pointer",
                rowClassName?.(item)
              )}
              onClick={() => onRowClick?.(item)}
            >
              {/* Row number */}
              <TableCell className="w-[52px] text-center px-4 py-3 tabular-nums text-caption text-[var(--text-muted)] font-medium select-none">
                {skip + index + 1}
              </TableCell>
              {columns.map((col) => (
                <TableCell key={col.key} className={cn(colClass(col), "py-3")}>
                  {col.render(item)}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
