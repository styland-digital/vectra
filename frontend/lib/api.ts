import axios, { AxiosError, type AxiosResponse, type InternalAxiosRequestConfig } from "axios"
import type {
  LoginResponse,
  TokenResponse,
  RegisterRequest,
  MessageResponse,
  Campaign,
  CampaignCreate,
  CampaignUpdate,
  CampaignStats,
  Lead,
  LeadDetail,
  LeadListResponse,
  Email,
  EmailDetail,
  EmailListResponse,
  CheckoutSessionCreate,
  CheckoutSessionResponse,
  PortalSessionResponse,
  Plan,
  AnalyticsDashboard,
  UsageMetrics,
  EngagementMetrics,
  AIAgentMetrics,
  AnalyticsEventTrack,
  EventTrackResponse,
  OrganizationUser,
  UserWithOrg,
  Organization,
  InviteUserRequest,
  CreateUserRequest,
  UpdateUserRoleRequest,
  NotificationResponse,
  Interaction,
} from "@/types"

const TOKEN_KEY = "vectra_token"
const REFRESH_KEY = "vectra_refresh_token"
const ZUSTAND_AUTH_KEY = "vectra-auth"
const COOKIE_MAX_AGE = 60 * 60 * 24 * 7

function getCookieToken(): string | null {
  if (typeof document === "undefined") return null
  const match = document.cookie.match(new RegExp(`(?:^|; )${TOKEN_KEY}=([^;]+)`))
  return match ? decodeURIComponent(match[1]) : null
}

function setTokenCookie(token: string): void {
  if (typeof document === "undefined") return
  document.cookie = `${TOKEN_KEY}=${token}; path=/; max-age=${COOKIE_MAX_AGE}; SameSite=Lax`
}

function clearTokenCookie(): void {
  if (typeof document === "undefined") return
  document.cookie = `${TOKEN_KEY}=; path=/; max-age=0; SameSite=Lax`
}

// Read token from Zustand persisted state in localStorage (fallback when cookie is absent).
function getPersistedToken(): string | null {
  if (typeof window === "undefined") return null
  try {
    const raw = localStorage.getItem(ZUSTAND_AUTH_KEY)
    if (!raw) return null
    return JSON.parse(raw)?.state?.token ?? null
  } catch {
    return null
  }
}

// Write a new access token back into the Zustand persisted state so that
// initAuth reads the fresh token on the next page load instead of the stale one.
function syncTokenToStore(token: string): void {
  if (typeof window === "undefined") return
  try {
    const raw = localStorage.getItem(ZUSTAND_AUTH_KEY)
    if (!raw) return
    const parsed = JSON.parse(raw)
    if (parsed?.state) {
      parsed.state.token = token
      localStorage.setItem(ZUSTAND_AUTH_KEY, JSON.stringify(parsed))
    }
  } catch {
    // non-fatal — store will self-correct on next initAuth
  }
}

const apiClient = axios.create({
  baseURL:
    process.env.NODE_ENV === "production"
      ? process.env.NEXT_PUBLIC_API_URL
      : "http://localhost:8000",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
})

// Request interceptor — attach token from cookie (primary) or Zustand localStorage (fallback).
// The cookie can go missing (cleared, browser restart) while the Zustand persist in
// localStorage is still intact. In that case we restore the cookie on the fly so that
// the SSR middleware stays in sync and subsequent requests don't need the fallback path.
apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  let token = getCookieToken()
  if (!token) {
    token = getPersistedToken()
    if (token) {
      // Restore cookie so middleware and future requests can find it without going through localStorage again.
      setTokenCookie(token)
    }
  }
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor - handle token refresh
let isRefreshing = false
let failedQueue: Array<{
  resolve: (token: string) => void
  reject: (error: unknown) => void
}> = []

function processQueue(error: unknown, token: string | null) {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else if (token) {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: (token: string) => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              resolve(apiClient(originalRequest))
            },
            reject,
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const refreshToken = typeof window !== "undefined" ? localStorage.getItem(REFRESH_KEY) : null
        if (!refreshToken) {
          throw new Error("No refresh token")
        }

        const response = await axios.post<TokenResponse>(
          `${apiClient.defaults.baseURL}/api/v1/auth/refresh`,
          { refresh_token: refreshToken }
        )

        const { access_token, refresh_token } = response.data

        // Keep cookie in sync so middleware SSR check stays valid.
        setTokenCookie(access_token)
        // Sync new token into Zustand persist so initAuth reads the fresh value on next load.
        syncTokenToStore(access_token)
        if (typeof window !== "undefined") {
          localStorage.setItem(REFRESH_KEY, refresh_token)
        }

        processQueue(null, access_token)
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        clearTokenCookie()
        if (typeof window !== "undefined") {
          localStorage.removeItem(TOKEN_KEY)
          localStorage.removeItem(REFRESH_KEY)
          window.location.href = "/login"
        }
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export const api = {
  auth: {
    login: (credentials: { email: string; password: string }) =>
      apiClient.post<LoginResponse>("/api/v1/auth/login", new URLSearchParams({
        username: credentials.email,
        password: credentials.password,
      }), {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }),

    register: (data: RegisterRequest) =>
      apiClient.post<LoginResponse>("/api/v1/auth/register", data),

    refresh: (refreshToken: string) =>
      apiClient.post<TokenResponse>("/api/v1/auth/refresh", { refresh_token: refreshToken }),

    logout: () =>
      apiClient.post("/api/v1/auth/logout"),

    verifyEmail: (email: string, otp: string) =>
      apiClient.post<MessageResponse>("/api/v1/auth/verify-email", { email, otp }),

    forgotPassword: (email: string) =>
      apiClient.post<MessageResponse>("/api/v1/auth/forgot-password", { email }),

    resetPassword: (token: string, password: string, password_confirmation: string) =>
      apiClient.post<MessageResponse>("/api/v1/auth/reset-password", {
        token,
        password,
        password_confirmation,
      }),

    changePasswordRequest: () =>
      apiClient.post<MessageResponse>("/api/v1/auth/change-password/request"),

    changePasswordVerify: (otp: string, new_password: string) =>
      apiClient.post("/api/v1/auth/change-password/verify", { otp, new_password }),
  },

  campaigns: {
    list: (params?: { skip?: number; limit?: number; status?: string }) =>
      apiClient.get<Campaign[]>("/api/v1/user/campaigns", { params }),

    get: (id: string) =>
      apiClient.get<Campaign>(`/api/v1/user/campaigns/${id}`),

    create: (data: CampaignCreate) =>
      apiClient.post<Campaign>("/api/v1/user/campaigns", data),

    update: (id: string, data: CampaignUpdate) =>
      apiClient.patch<Campaign>(`/api/v1/user/campaigns/${id}`, data),

    delete: (id: string) =>
      apiClient.delete(`/api/v1/user/campaigns/${id}`),

    launch: (id: string) =>
      apiClient.post<Campaign>(`/api/v1/user/campaigns/${id}/launch`),

    pause: (id: string) =>
      apiClient.post<Campaign>(`/api/v1/user/campaigns/${id}/pause`),

    resume: (id: string) =>
      apiClient.post<Campaign>(`/api/v1/user/campaigns/${id}/resume`),

    stats: (id: string) =>
      apiClient.get<CampaignStats>(`/api/v1/user/campaigns/${id}/stats`),
  },

  leads: {
    list: (params?: {
      campaign_id?: string
      status?: string
      intent?: string
      bant_score_min?: number
      bant_score_max?: number
      search?: string
      skip?: number
      limit?: number
    }) =>
      apiClient.get<LeadListResponse>("/api/v1/user/leads", { params }),

    get: (id: string) =>
      apiClient.get<LeadDetail>(`/api/v1/user/leads/${id}`),

    update: (id: string, data: Partial<Lead>) =>
      apiClient.patch<Lead>(`/api/v1/user/leads/${id}`, data),

    interactions: (id: string, params?: { skip?: number; limit?: number }) =>
      apiClient.get<{ data: Interaction[] }>(`/api/v1/user/leads/${id}/interactions`, { params }),
  },

  emails: {
    list: (params?: {
      campaign_id?: string
      lead_id?: string
      status?: string
      skip?: number
      limit?: number
    }) =>
      apiClient.get<EmailListResponse>("/api/v1/user/emails", { params }),

    get: (id: string) =>
      apiClient.get<EmailDetail>(`/api/v1/user/emails/${id}`),

    approve: (id: string, modifications?: Record<string, unknown>) =>
      apiClient.post<EmailDetail>(`/api/v1/user/emails/${id}/approve`, { modifications }),

    reject: (id: string, reason: string) =>
      apiClient.post<EmailDetail>(`/api/v1/user/emails/${id}/reject`, { reason }),
  },

  billing: {
    createCheckout: (data: CheckoutSessionCreate) =>
      apiClient.post<CheckoutSessionResponse>("/api/v1/user/billing/create-checkout-session", data),

    createPortal: () =>
      apiClient.post<PortalSessionResponse>("/api/v1/user/billing/create-portal-session"),

    getPlans: () =>
      apiClient.get<{ plans: Plan[] }>("/api/v1/user/billing/plans"),

    getSession: (sessionId: string) =>
      apiClient.get(`/api/v1/user/billing/session/${sessionId}`),
  },

  analytics: {
    overview: () =>
      apiClient.get<AnalyticsDashboard>("/api/v1/user/analytics/overview"),

    usage: (days?: number) =>
      apiClient.get<UsageMetrics>("/api/v1/user/analytics/usage", { params: { days } }),

    engagement: (days?: number) =>
      apiClient.get<EngagementMetrics>("/api/v1/user/analytics/engagement", { params: { days } }),

    aiAgents: (days?: number) =>
      apiClient.get<AIAgentMetrics>("/api/v1/user/analytics/ai-agents", { params: { days } }),

    trackEvent: (data: AnalyticsEventTrack) =>
      apiClient.post<EventTrackResponse>("/api/v1/user/analytics/events", data),
  },

  users: {
    me: () =>
      apiClient.get<UserWithOrg>("/api/v1/user/me"),

    organization: () =>
      apiClient.get<Organization>("/api/v1/user/organizations/me"),

    updateOrganization: (data: { name?: string; plan?: string; settings?: Record<string, unknown> }) =>
      apiClient.patch<Organization>("/api/v1/user/organizations/me", data),

    orgUsers: (params?: { skip?: number; limit?: number }) =>
      apiClient.get<OrganizationUser[]>("/api/v1/user/organizations/me/users", { params }),

    invite: (data: InviteUserRequest) =>
      apiClient.post<MessageResponse>("/api/v1/user/organizations/me/users/invite", data),

    createUser: (data: CreateUserRequest) =>
      apiClient.post<OrganizationUser>("/api/v1/user/organizations/me/users/create", data),

    updateRole: (userId: string, data: UpdateUserRoleRequest) =>
      apiClient.patch<OrganizationUser>(`/api/v1/user/organizations/me/users/${userId}/role`, data),

    removeUser: (userId: string) =>
      apiClient.delete(`/api/v1/user/organizations/me/users/${userId}`),

    sendNotification: (data: { type: string; recipients: string[]; subject: string; body: string }) =>
      apiClient.post<NotificationResponse>("/api/v1/user/notifications/send", data),
  },
}

export { TOKEN_KEY, REFRESH_KEY }
export default api
