"use client"

import { LoadingSkeleton } from "@/components/loading-skeleton"
import { KPICard, type KPICardProps } from "@/components/features/kpi-card"
import { StaggerContainer, StaggerItem } from "@/components/motion"
import { cn } from "@/lib/utils"

interface KPIGridProps {
  kpis: KPICardProps[]
  cols?: 2 | 3 | 4
  variant?: KPICardProps["variant"]
  isLoading?: boolean
  className?: string
}

const colsMap = {
  2: "sm:grid-cols-2",
  3: "sm:grid-cols-2 lg:grid-cols-3",
  4: "sm:grid-cols-2 lg:grid-cols-4",
}

export function KPIGrid({ kpis, cols = 4, variant = "elevated", isLoading, className }: KPIGridProps) {
  if (isLoading) {
    return <LoadingSkeleton variant="stats" />
  }

  return (
    <StaggerContainer className={cn("grid gap-4", colsMap[cols], className)}>
      {kpis.map((kpi) => (
        <StaggerItem key={kpi.label} className="h-full">
          <KPICard {...kpi} variant={variant} className={cn("h-full", kpi.className)} />
        </StaggerItem>
      ))}
    </StaggerContainer>
  )
}
