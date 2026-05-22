"use client"

import { useEffect, useState } from "react"
import { useRouter, usePathname } from "next/navigation"
import { useAuthStore } from "@/lib/stores/auth"
import { LoadingSkeleton } from "@/components/loading-skeleton"

const publicPaths = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/pricing",
  "/billing/success",
]

const authPaths = ["/login", "/register", "/forgot-password", "/reset-password"]

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()
  const [isHydrated, setIsHydrated] = useState(false)
  const { token, isInitialized, initAuth } = useAuthStore()

  // Manually rehydrate the Zustand store (due to skipHydration: true)
  useEffect(() => {
    useAuthStore.persist.rehydrate()
    setIsHydrated(true)
  }, [])

  // Initialize auth after hydration
  useEffect(() => {
    if (isHydrated && !isInitialized) {
      initAuth()
    }
  }, [isHydrated, isInitialized, initAuth])

  // Handle redirects
  useEffect(() => {
    if (!isHydrated || !isInitialized) return

    const isPublic = publicPaths.some((p) => pathname.startsWith(p))
    const isAuth = authPaths.some((p) => pathname.startsWith(p))

    if (!token && !isPublic) {
      router.replace("/login")
    } else if (token && isAuth) {
      router.replace("/dashboard")
    }
  }, [isHydrated, isInitialized, token, pathname, router])

  // Show loading while hydrating or initializing — but never block public/auth pages
  if (!isHydrated || !isInitialized) {
    const isPublicPage = publicPaths.some((p) => pathname.startsWith(p))
    if (isPublicPage) return <>{children}</>
    return <LoadingSkeleton variant="page" />
  }

  const isPublic = publicPaths.some((p) => pathname.startsWith(p))
  if (!token && !isPublic) {
    return <LoadingSkeleton variant="page" />
  }

  return <>{children}</>
}
