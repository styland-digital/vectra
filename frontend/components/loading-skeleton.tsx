"use client"

import { cn } from "@/lib/utils"

function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "rounded-xl bg-gradient-to-r from-[var(--surface-secondary)] via-[var(--surface-hover)] to-[var(--surface-secondary)] bg-[length:200%_100%] animate-shimmer",
        className
      )}
    />
  )
}

interface LoadingSkeletonProps {
  variant?: "page" | "card" | "stats" | "table"
}

export function LoadingSkeleton({ variant = "card" }: LoadingSkeletonProps) {
  if (variant === "page") {
    return (
      <div className="min-h-screen bg-[var(--bg-primary)] flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="h-8 w-8 rounded-md bg-gradient-to-br from-[var(--color-primary-500)] to-[var(--color-primary-600)] animate-pulse" />
          <Skeleton className="h-4 w-24" />
        </div>
      </div>
    )
  }

  if (variant === "stats") {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="rounded-lg border border-[var(--border-primary)] bg-[var(--surface-primary)] p-6"
          >
            <Skeleton className="h-4 w-24 mb-3" />
            <Skeleton className="h-8 w-16 mb-2" />
            <Skeleton className="h-3 w-32" />
          </div>
        ))}
      </div>
    )
  }

  if (variant === "table") {
    return (
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="flex items-center space-x-4 py-3">
            <Skeleton className="h-10 w-10 rounded-full" />
            <div className="flex-1 space-y-2">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-3 w-1/2" />
            </div>
            <Skeleton className="h-6 w-16" />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="rounded-lg border border-[var(--border-primary)] bg-[var(--surface-primary)] p-6">
      <Skeleton className="h-5 w-32 mb-2" />
      <Skeleton className="h-3 w-48 mb-6" />
      <div className="space-y-3">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-4 w-4/6" />
      </div>
    </div>
  )
}

export { Skeleton }
