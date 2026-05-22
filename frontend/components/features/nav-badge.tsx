"use client"

import { useDataStore } from "@/lib/stores/data"

export function NavEmailBadge() {
  const pending = useDataStore((s) => s.emailSummary?.pending ?? 0)
  if (pending === 0) return null
  return (
    <span className="ml-auto text-caption bg-[var(--color-primary-500)] text-white rounded-full px-1.5 min-w-[18px] text-center leading-[18px] h-[18px] flex items-center justify-center">
      {pending > 99 ? "99+" : pending}
    </span>
  )
}
