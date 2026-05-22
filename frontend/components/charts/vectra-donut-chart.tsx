"use client"

import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts"
import { cn } from "@/lib/utils"

interface VectraDonutChartProps {
  value: number
  max: number
  label?: string
  color?: string
  trackColor?: string
  size?: number
  className?: string
}

export function VectraDonutChart({
  value,
  max,
  label,
  color = "var(--color-primary-500)",
  trackColor = "var(--surface-secondary)",
  size = 160,
  className,
}: VectraDonutChartProps) {
  const percentage = max > 0 ? Math.min(Math.round((value / max) * 100), 100) : 0
  const remaining = Math.max(max - value, 0)

  const chartData = [
    { name: "used", value: value },
    { name: "remaining", value: remaining },
  ]

  const innerRadius = size * 0.3
  const outerRadius = size * 0.46

  return (
    <div className={cn("relative flex items-center justify-center", className)} style={{ width: size, height: size }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={innerRadius}
            outerRadius={outerRadius}
            startAngle={90}
            endAngle={-270}
            dataKey="value"
            strokeWidth={0}
          >
            <Cell fill={color} />
            <Cell fill={trackColor} />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      {/* Centre text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <span className="text-h3 font-bold tabular-nums text-[var(--text-primary)] leading-none">
          {percentage}%
        </span>
        {label && (
          <span className="text-caption text-[var(--text-muted)] mt-0.5">{label}</span>
        )}
      </div>
    </div>
  )
}
