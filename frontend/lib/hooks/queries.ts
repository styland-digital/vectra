import { useQuery, keepPreviousData } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { useAuthStore } from "@/lib/stores/auth"

export function useCampaigns(params?: {
  skip?: number
  limit?: number
  status?: string
  search?: string
  created_by?: string
  created_after?: string
  started_after?: string
}) {
  const token = useAuthStore((s) => s.token)
  return useQuery({
    queryKey: ["campaigns", params],
    queryFn: async () => {
      const res = await api.campaigns.list(params)
      return res.data
    },
    enabled: !!token,
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  })
}

export function useCampaign(id: string) {
  return useQuery({
    queryKey: ["campaigns", id],
    queryFn: async () => {
      const res = await api.campaigns.get(id)
      return res.data
    },
    enabled: !!id,
    refetchInterval: (query) =>
      query.state.data?.status === "active" ? 5_000 : false,
  })
}

export function useCampaignStats(id: string) {
  return useQuery({
    queryKey: ["campaigns", id, "stats"],
    queryFn: async () => {
      const res = await api.campaigns.stats(id)
      return res.data
    },
    enabled: !!id,
    refetchInterval: (query) =>
      query.state.data?.status === "active" ? 5_000 : false,
  })
}

export function useLeads(params?: {
  campaign_id?: string
  status?: string
  intent?: string
  bant_score_min?: number
  bant_score_max?: number
  search?: string
  skip?: number
  limit?: number
}) {
  const token = useAuthStore((s) => s.token)
  return useQuery({
    queryKey: ["leads", params],
    queryFn: async () => {
      const res = await api.leads.list(params)
      return res.data
    },
    enabled: !!token,
  })
}

export function useLead(id: string) {
  return useQuery({
    queryKey: ["leads", id],
    queryFn: async () => {
      const res = await api.leads.get(id)
      return res.data
    },
    enabled: !!id,
  })
}

export function useEmails(params?: {
  campaign_id?: string
  lead_id?: string
  status?: string
  skip?: number
  limit?: number
}) {
  const token = useAuthStore((s) => s.token)
  return useQuery({
    queryKey: ["emails", params],
    queryFn: async () => {
      const res = await api.emails.list(params)
      return res.data
    },
    enabled: !!token,
  })
}

export function useEmail(id: string) {
  return useQuery({
    queryKey: ["emails", id],
    queryFn: async () => {
      const res = await api.emails.get(id)
      return res.data
    },
    enabled: !!id,
  })
}

export function useOrganization() {
  const token = useAuthStore((s) => s.token)
  return useQuery({
    queryKey: ["organization"],
    queryFn: async () => {
      const res = await api.users.organization()
      return res.data
    },
    enabled: !!token,
  })
}

export function useOrgUsers(params?: { skip?: number; limit?: number }) {
  const token = useAuthStore((s) => s.token)
  return useQuery({
    queryKey: ["org-users", params],
    queryFn: async () => {
      const res = await api.users.orgUsers(params)
      return res.data
    },
    enabled: !!token,
  })
}

export function useBillingPlans() {
  const token = useAuthStore((s) => s.token)
  return useQuery({
    queryKey: ["billing-plans"],
    queryFn: async () => {
      const res = await api.billing.getPlans()
      return res.data.plans
    },
    enabled: !!token,
  })
}
