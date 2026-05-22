"use client"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { VectraTooltip } from "./chart-tooltip"
import { cn } from "@/lib/utils"

export interface BarSeries {
  key: string
  label: string
  color: string
}

interface VectraBarChartProps {
  data: Record<string, string | number>[]
  series: BarSeries[]
  xKey: string
  height?: number
  formatter?: (v: number) => string
  showLegend?: boolean
  className?: string
}

function CustomLegend({ payload }: { payload?: Array<{ value: string; color: string }> }) {
  if (!payload?.length) return null
  return (
    <div className="flex items-center justify-end gap-4 pt-2">
      {payload.map((entry) => (
        <div key={entry.value} className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full" style={{ background: entry.color }} />
          <span className="text-caption text-[var(--text-muted)]">{entry.value}</span>
        </div>
      ))}
    </div>
  )
}

export function VectraBarChart({
  data,
  series,
  xKey,
  height = 240,
  formatter,
  showLegend = true,
  className,
}: VectraBarChartProps) {
  return (
    <div className={cn("w-full", className)} style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 4, right: 4, left: -20, bottom: 0 }} barGap={4} barCategoryGap="30%">
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="var(--border-secondary)"
            vertical={false}
          />
          <XAxis
            dataKey={xKey}
            tick={{ fill: "var(--text-muted)", fontSize: 12 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "var(--text-muted)", fontSize: 12 }}
            axisLine={false}
            tickLine={false}
            tickFormatter={formatter}
          />
          <Tooltip
            content={<VectraTooltip formatter={formatter ? (v) => formatter(v as number) : undefined} />}
            cursor={{ fill: "var(--surface-secondary)", radius: 4 }}
          />
          {showLegend && (
            <Legend content={<CustomLegend />} />
          )}
          {series.map((s, i) => (
            <Bar
              key={s.key}
              dataKey={s.key}
              name={s.label}
              fill={s.color}
              radius={i === series.length - 1 ? [4, 4, 0, 0] : [4, 4, 0, 0]}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
