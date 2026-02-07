"use client"

import type { ReactNode } from "react"
import type { LucideIcon } from "lucide-react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { LoadingSkeleton } from "@/components/loading-skeleton"
import { EmptyState } from "@/components/features/empty-state"

export interface Column<T> {
  key: string
  header: string
  render: (item: T) => ReactNode
  className?: string
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
}

export function DataTable<T extends { id: string }>({
  columns,
  data,
  isLoading,
  emptyMessage,
  emptyDescription,
  emptyIcon,
  emptyAction,
  onRowClick,
  rowClassName,
}: DataTableProps<T>) {
  if (isLoading) {
    return <LoadingSkeleton variant="table" />
  }

  if (data.length === 0) {
    return (
      <EmptyState
        icon={emptyIcon}
        title={emptyMessage}
        description={emptyDescription}
        action={emptyAction}
      />
    )
  }

  return (
    <div className="rounded-md border border-[var(--border-primary)]">
      <Table>
        <TableHeader>
          <TableRow className="border-[var(--border-primary)] hover:bg-transparent">
            {columns.map((col) => (
              <TableHead
                key={col.key}
                className={col.className}
              >
                {col.header}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item) => (
            <TableRow
              key={item.id}
              className={`border-[var(--border-primary)] hover:bg-[var(--surface-hover)] transition-colors duration-150 ${
                onRowClick ? "cursor-pointer" : ""
              } ${rowClassName ? rowClassName(item) : ""}`}
              onClick={() => onRowClick?.(item)}
            >
              {columns.map((col) => (
                <TableCell key={col.key} className={col.className}>
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
