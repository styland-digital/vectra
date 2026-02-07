"use client"

import { cn } from "@/lib/utils"

interface BANTScoreBarProps {
  score: number
  budget?: number
  authority?: number
  need?: number
  timeline?: number
  showDetails?: boolean
  className?: string
}

function ScoreSegment({ label, value, max }: { label: string; value: number; max: number }) {
  const pct = Math.round((value / max) * 100)
  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="w-16 text-[var(--text-muted)]">{label}</span>
      <div className="flex-1 h-1.5 bg-[var(--surface-secondary)] rounded-full">
        <div
          className="h-full rounded-full bg-[var(--color-primary-500)] transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="w-8 text-right text-[var(--text-secondary)]">{value}/{max}</span>
    </div>
  )
}

export function BANTScoreBar({
  score,
  budget,
  authority,
  need,
  timeline,
  showDetails = false,
  className,
}: BANTScoreBarProps) {
  const scoreColor =
    score >= 60
      ? "text-[var(--color-success-500)]"
      : score >= 40
        ? "text-[var(--color-warning-500)]"
        : "text-[var(--color-error-500)]"

  const barColor =
    score >= 60
      ? "bg-[var(--color-success-500)]"
      : score >= 40
        ? "bg-[var(--color-warning-500)]"
        : "bg-[var(--color-error-500)]"

  return (
    <div className={cn("space-y-2", className)}>
      <div className="flex items-center gap-2">
        <span className={cn("text-sm font-semibold", scoreColor)}>{score}</span>
        <div className="flex-1 h-2 bg-[var(--surface-secondary)] rounded-full">
          <div
            className={cn("h-full rounded-full transition-all", barColor)}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
      {showDetails && budget !== undefined && authority !== undefined && need !== undefined && timeline !== undefined && (
        <div className="space-y-1.5 pl-1">
          <ScoreSegment label="Budget" value={budget} max={25} />
          <ScoreSegment label="Authority" value={authority} max={25} />
          <ScoreSegment label="Need" value={need} max={25} />
          <ScoreSegment label="Timeline" value={timeline} max={25} />
        </div>
      )}
    </div>
  )
}
