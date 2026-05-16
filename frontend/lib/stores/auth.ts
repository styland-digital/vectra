import { create } from "zustand"
import { persist } from "zustand/middleware"
import { api, TOKEN_KEY, REFRESH_KEY } from "../api"
import type { UserWithOrg, RegisterRequest } from "@/types"
import { AxiosError } from "axios"

// Cookie utilities for SSR middleware support
const COOKIE_TOKEN_KEY = "vectra_token"
const COOKIE_MAX_AGE = 60 * 60 * 24 * 7 // 7 days

function setCookie(name: string, value: string, maxAge: number = COOKIE_MAX_AGE): void {
  if (typeof document === "undefined") return
  document.cookie = `${name}=${value}; path=/; max-age=${maxAge}; SameSite=Lax`
}

function removeCookie(name: string): void {
  if (typeof document === "undefined") return
  document.cookie = `${name}=; path=/; max-age=0; SameSite=Lax`
}

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]+)`))
  return match ? decodeURIComponent(match[1]) : null
}

interface AuthState {
  user: UserWithOrg | null
  token: string | null
  refreshToken: string | null
  isLoading: boolean
  error: string | null
  isInitialized: boolean

  register: (data: RegisterRequest) => Promise<void>
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  clearError: () => void
  initAuth: () => Promise<void>
}

/** Returns i18n key for known errors, raw message otherwise. Call t() on result when displaying. */
function getErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    const status = error.response?.status
    const data = error.response?.data
    const msg =
      typeof data === "object" && data !== null
        ? ("detail" in data && typeof data.detail === "string" ? data.detail
          : "error" in data && typeof data.error === "string" ? data.error
          : "message" in data && typeof data.message === "string" ? data.message
          : null)
        : null

    if (status === 401 || msg?.toLowerCase().includes("invalid credentials")) {
      return "auth.errors.invalidCredentials"
    }
    if (status === 409 || msg?.toLowerCase().includes("already registered") || msg?.toLowerCase().includes("email exists")) {
      return "auth.errors.emailExists"
    }
    if (error.code === "ERR_NETWORK" || error.message?.includes("Network Error")) {
      return "auth.errors.networkError"
    }
    if (msg) return msg
  }
  return "auth.errors.genericError"
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      refreshToken: null,
      isLoading: false,
      error: null,
      isInitialized: false,

      register: async (data: RegisterRequest) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.auth.register(data)
          const { access_token, refresh_token, user } = response.data

          localStorage.setItem(REFRESH_KEY, refresh_token)
          setCookie(COOKIE_TOKEN_KEY, access_token)

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isLoading: false,
          })
        } catch (error: unknown) {
          const message = getErrorMessage(error)
          set({ isLoading: false, error: message })
          throw error
        }
      },

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.auth.login({ email, password })
          const { access_token, refresh_token, user } = response.data

          localStorage.setItem(REFRESH_KEY, refresh_token)
          setCookie(COOKIE_TOKEN_KEY, access_token)

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isLoading: false,
          })
        } catch (error: unknown) {
          const message = getErrorMessage(error)
          set({ isLoading: false, error: message })
          throw error
        }
      },

      logout: () => {
        // Clear localStorage
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(REFRESH_KEY)

        // Clear cookie
        removeCookie(COOKIE_TOKEN_KEY)

        set({
          user: null,
          token: null,
          refreshToken: null,
          error: null,
        })
      },

      clearError: () => set({ error: null }),

      initAuth: async () => {
        // Primary source: cookie (read by the axios interceptor).
        // Fallback: Zustand persisted state in localStorage (survives cookie eviction).
        let token = getCookie(COOKIE_TOKEN_KEY)

        if (!token) {
          try {
            const raw = localStorage.getItem("vectra-auth")
            if (raw) {
              token = JSON.parse(raw)?.state?.token ?? null
            }
          } catch { /* non-fatal */ }
        }

        if (!token) {
          set({ isInitialized: true })
          return
        }

        // Ensure the cookie is present so the axios interceptor can attach it
        // without needing to fall back to the localStorage path on every request.
        if (!getCookie(COOKIE_TOKEN_KEY)) {
          setCookie(COOKIE_TOKEN_KEY, token)
        }

        try {
          const response = await api.users.me()
          // Re-read the cookie after the request: the response interceptor may have
          // silently refreshed an expired JWT and written a new value to the cookie.
          const currentToken = getCookie(COOKIE_TOKEN_KEY) ?? token
          set({
            user: response.data,
            token: currentToken,
            refreshToken: localStorage.getItem(REFRESH_KEY),
            isInitialized: true,
          })
        } catch {
          localStorage.removeItem(TOKEN_KEY)
          localStorage.removeItem(REFRESH_KEY)
          removeCookie(COOKIE_TOKEN_KEY)
          set({
            user: null,
            token: null,
            refreshToken: null,
            isInitialized: true,
          })
        }
      },
    }),
    {
      name: "vectra-auth",
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        user: state.user,
      }),
      skipHydration: true, // Fix SSR hydration issues
    }
  )
)
