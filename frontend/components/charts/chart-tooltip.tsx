"use client"

import type { TooltipProps } from "recharts"
import type { ValueType, NameType } from "recharts/types/component/DefaultTooltipContent"

interface VectraTooltipProps extends TooltipProps<ValueType, NameType> {
  formatter?: (value: ValueType) => string
}

export function VectraTooltip({ active, payload, label, formatter }: VectraTooltipProps) {
  if (!active || !payload?.length) return null

  return (
    <div className="rounded-lg border border-[var(--border-primary)] bg-[var(--surface-primary)] shadow-lg p-3 min-w-[140px] z-50">
      {label && (
        <p className="text-caption text-[var(--text-muted)] mb-2 font-medium">{label}</p>
      )}
      <div className="space-y-1.5">
        {payload.map((entry, i) => (
          <div key={`${entry.name}-${i}`} className="flex items-center gap-2">
            <span
              className="h-2 w-2 rounded-full shrink-0"
              style={{ background: entry.color }}
            />
            <span className="text-body-sm text-[var(--text-secondary)]">{entry.name}</span>
            <span className="ml-auto text-body-sm font-medium text-[var(--text-primary)] tabular-nums pl-4">
              {formatter ? formatter(entry.value as ValueType) : String(entry.value ?? 0)}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
