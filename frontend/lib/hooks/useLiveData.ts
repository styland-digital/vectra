"use client"

import { useEffect } from "react"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { useDataStore } from "@/lib/stores/data"
import { useAuthStore } from "@/lib/stores/auth"

const POLL_INTERVAL = 30_000

export function useLiveData() {
  const token = useAuthStore((s) => s.token)

  // Use individual selectors to avoid subscribing to the entire store.
  // Zustand actions are stable references — these selectors never trigger re-renders.
  const setCampaignSummary = useDataStore((s) => s.setCampaignSummary)
  const setLeadSummary = useDataStore((s) => s.setLeadSummary)
  const setEmailSummary = useDataStore((s) => s.setEmailSummary)

  const { data: analyticsData } = useQuery({
    queryKey: ["live", "analytics"],
    queryFn: async () => {
      const res = await api.analytics.overview()
      return res.data
    },
    enabled: !!token,
    refetchInterval: POLL_INTERVAL,
    staleTime: 60_000,
  })

  // Side effects belong in useEffect, NOT in select.
  // select is re-run whenever its function reference changes (every Sidebar render),
  // which previously created an infinite loop via NavEmailBadge → Sidebar → select → store → NavEmailBadge.
  useEffect(() => {
    if (!analyticsData) return
    setCampaignSummary({
      total: analyticsData.overview.active_campaigns,
      active: analyticsData.overview.active_campaigns,
      draft: 0,
      paused: 0,
    })
    setLeadSummary({
      total: analyticsData.growth.leads_current,
      qualified: analyticsData.overview.qualified_leads,
    })
  }, [analyticsData, setCampaignSummary, setLeadSummary])

  const { data: emailsData } = useQuery({
    queryKey: ["live", "emails-pending"],
    queryFn: async () => {
      const res = await api.emails.list({ status: "pending", limit: 1 })
      return res.data
    },
    enabled: !!token,
    refetchInterval: POLL_INTERVAL,
    staleTime: 60_000,
  })

  useEffect(() => {
    if (!emailsData) return
    const pending = emailsData.pagination?.total ?? 0
    setEmailSummary({ pending, total: pending })
  }, [emailsData, setEmailSummary])
}
