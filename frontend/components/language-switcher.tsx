"use client"

import { useTranslation } from "@/lib/i18n"
import { Check } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useTranslation()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="sm"
          className="h-9 px-2 hover:bg-[var(--surface-hover)] transition-colors duration-150"
        >
          <span className="text-sm font-medium text-[var(--text-muted)]">
            {locale.toUpperCase()}
          </span>
          <span className="sr-only">{t("common.language")}</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setLocale("fr")} className="flex items-center gap-2">
          <span className="w-4 h-4 flex items-center justify-center">
            {locale === "fr" && <Check className="h-4 w-4" />}
          </span>
          Français (FR)
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setLocale("en")} className="flex items-center gap-2">
          <span className="w-4 h-4 flex items-center justify-center">
            {locale === "en" && <Check className="h-4 w-4" />}
          </span>
          English (EN)
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
