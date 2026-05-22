"use client"

import { cn } from "@/lib/utils"
import { VectraLogo } from "@/components/vectra-logo"

export interface PageLoaderProps {
  /** Texte optionnel sous l’indicateur (ex. après i18n hydraté) */
  message?: string
  /** Mode compact pour fallbacks Suspense / embarqué */
  dense?: boolean
  /** Afficher le logo Vectra (désactivé en dense pour les petits blocs) */
  showLogo?: boolean
  className?: string
}

/** Chargement plein écran ou compact : fond token, pas d’accent bleu décoratif */
export function PageLoader({
  message,
  dense = false,
  showLogo = true,
  className,
}: PageLoaderProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center bg-[var(--bg-primary)]",
        dense ? "min-h-[140px] py-6" : "min-h-screen",
        className
      )}
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <span className="sr-only">{message ?? "Chargement"}</span>
      {showLogo && !dense && (
        <div className="mb-6 opacity-90">
          <VectraLogo size="md" />
        </div>
      )}
      <div className="flex items-end justify-center gap-1.5 h-6" aria-hidden>
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className={cn(
              "w-1 rounded-full bg-[var(--text-muted)] animate-pulse",
              i === 1 && "delay-150",
              i === 2 && "delay-300"
            )}
            style={{ height: dense ? 10 + i * 3 : 12 + i * 4 }}
          />
        ))}
      </div>
      {message && (
        <p className="mt-4 text-body-sm text-[var(--text-secondary)] text-center max-w-xs px-4">
          {message}
        </p>
      )}
    </div>
  )
}
