"use client"

import { cn } from "@/lib/utils"
import type { CampaignUserInfo } from "@/types"

// Deterministic color palette — same user always gets the same color
const PALETTES = [
  ["bg-[var(--color-primary-500)]/15", "text-[var(--color-primary-600)]"],
  ["bg-[var(--color-success-500)]/15", "text-[var(--color-success-600)]"],
  ["bg-[var(--color-warning-500)]/15", "text-[var(--color-warning-600)]"],
  ["bg-purple-500/15", "text-purple-600"],
  ["bg-pink-500/15", "text-pink-600"],
  ["bg-teal-500/15", "text-teal-600"],
  ["bg-orange-500/15", "text-orange-600"],
  ["bg-indigo-500/15", "text-indigo-600"],
] as const

function paletteFor(id: string): readonly [string, string] {
  // Sum a few char codes for a stable but varied index
  const hash = [...id.replace(/-/g, "").slice(0, 8)].reduce(
    (acc, c) => acc + c.charCodeAt(0),
    0
  )
  return PALETTES[hash % PALETTES.length]
}

function initials(user: CampaignUserInfo): string {
  const f = user.first_name?.trim()[0] ?? ""
  const l = user.last_name?.trim()[0] ?? ""
  return (f + l).toUpperCase() || user.email[0].toUpperCase()
}

const sizeMap = {
  xs: "h-6 w-6 text-[10px]",
  sm: "h-7 w-7 text-caption",
  md: "h-8 w-8 text-body-sm",
} as const

interface UserAvatarProps {
  user: CampaignUserInfo
  size?: keyof typeof sizeMap
  className?: string
  showTooltip?: boolean
}

export function UserAvatar({ user, size = "sm", className }: UserAvatarProps) {
  const [bg, text] = paletteFor(user.id)
  const label = initials(user)
  const fullName =
    user.first_name || user.last_name
      ? `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim()
      : user.email

  return (
    <div
      title={fullName}
      className={cn(
        "rounded-full flex items-center justify-center font-semibold shrink-0 select-none",
        sizeMap[size],
        bg,
        text,
        className
      )}
    >
      {label}
    </div>
  )
}

interface CampaignOwnersProps {
  creator: CampaignUserInfo | null
  launcher: CampaignUserInfo | null
}

export function CampaignOwners({ creator, launcher }: CampaignOwnersProps) {
  if (!creator && !launcher) return <span className="text-caption text-[var(--text-muted)]">—</span>

  const showBoth =
    launcher && creator && launcher.id !== creator.id

  if (!showBoth) {
    const user = creator ?? launcher
    if (!user) return null
    const fullName =
      user.first_name || user.last_name
        ? `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim()
        : user.email

    return (
      <div className="flex items-center gap-2">
        <UserAvatar user={user} size="sm" />
        <span className="text-body-sm text-[var(--text-secondary)] truncate max-w-[120px]">
          {fullName}
        </span>
      </div>
    )
  }

  // Both creator and launcher differ — show stacked avatars + creator name
  const creatorName =
    creator!.first_name || creator!.last_name
      ? `${creator!.first_name ?? ""} ${creator!.last_name ?? ""}`.trim()
      : creator!.email

  return (
    <div className="flex items-center gap-2">
      <div className="flex -space-x-1.5">
        <UserAvatar
          user={creator!}
          size="sm"
          className="ring-2 ring-[var(--surface-primary)]"
        />
        <UserAvatar
          user={launcher!}
          size="sm"
          className="ring-2 ring-[var(--surface-primary)]"
        />
      </div>
      <span className="text-body-sm text-[var(--text-secondary)] truncate max-w-[100px]">
        {creatorName}
      </span>
    </div>
  )
}
