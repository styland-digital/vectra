"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import {
  BarChart3,
  Users,
  TrendingUp,
  TrendingDown,
  Mail,
  Target,
  Bot,
  RefreshCw,
  Activity,
  Zap,
  CheckCircle,
  Clock
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface AnalyticsDashboard {
  overview: {
    campaigns_active: number
    leads_processed_30d: number
    leads_qualified_30d: number
    emails_sent_30d: number
    qualification_rate: number
    email_open_rate: number
  }
  growth: {
    leads_7d_vs_30d: { current: number; previous: number }
    emails_7d_vs_30d: { current: number; previous: number }
  }
  team: {
    total_users: number
    active_users: number
    user_activity_rate: number
    role_distribution: Record<string, number>
    period_days: number
  }
  ai_agents: {
    total_agent_runs: number
    successful_runs: number
    success_rate: number
    prospector_runs: number
    bant_runs: number
    scheduler_runs: number
    period_days: number
  }
  subscription?: {
    plan_type: string
    status: string
    current_period_end?: string
  }
  generated_at: string
}

export default function AnalyticsPage() {
  const [dashboard, setDashboard] = useState<AnalyticsDashboard | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchDashboard = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/v1/user/analytics/overview', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setDashboard(data)
      } else {
        setError('Failed to load analytics data')
      }
    } catch (error) {
      console.error('Analytics fetch error:', error)
      setError('Connection error')
    }

    setIsLoading(false)
  }

  useEffect(() => {
    fetchDashboard()
  }, [])

  const formatPercent = (value: number) => `${value.toFixed(1)}%`
  const formatNumber = (value: number) => value.toLocaleString()

  const calculateGrowth = (current: number, previous: number) => {
    if (previous === 0) return 0
    return ((current - previous) / previous) * 100
  }

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <div className="space-y-2">
            <h1 className="text-h1 text-[var(--text-primary)]">Analytics</h1>
            <p className="text-body text-[var(--text-secondary)]">Performance insights and business metrics</p>
          </div>
          <RefreshCw className="w-5 h-5 animate-spin text-[var(--text-muted)]" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-[var(--surface-secondary)] rounded w-3/4 mb-3"></div>
                <div className="h-8 bg-[var(--surface-secondary)] rounded w-1/2"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-16 space-y-4">
        <div className="w-16 h-16 rounded-full bg-[var(--color-error-100)] flex items-center justify-center mb-4">
          <TrendingDown className="w-8 h-8 text-[var(--color-error-500)]" />
        </div>
        <h2 className="text-h3 text-[var(--text-primary)]">Failed to load analytics</h2>
        <p className="text-body text-[var(--text-secondary)]">{error}</p>
        <Button onClick={fetchDashboard} className="focus-ring">
          <RefreshCw className="w-4 h-4 mr-2" />
          Retry
        </Button>
      </div>
    )
  }

  if (!dashboard) return null

  const leadsGrowth = calculateGrowth(
    dashboard.growth.leads_7d_vs_30d.current,
    dashboard.growth.leads_7d_vs_30d.previous
  )

  const emailsGrowth = calculateGrowth(
    dashboard.growth.emails_7d_vs_30d.current,
    dashboard.growth.emails_7d_vs_30d.previous
  )

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <h1 className="text-h1 text-[var(--text-primary)]">Analytics</h1>
          <p className="text-body text-[var(--text-secondary)]">
            Performance insights and business metrics
            <span className="text-caption text-[var(--text-muted)] ml-2">
              • Updated {new Date(dashboard.generated_at).toLocaleString()}
            </span>
          </p>
        </div>
        <div className="flex items-center space-x-3">
          {dashboard.subscription && (
            <Badge variant="secondary" className="capitalize text-xs">
              {dashboard.subscription.plan_type} Plan
            </Badge>
          )}
          <Button onClick={fetchDashboard} variant="outline" size="sm" className="focus-ring">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="card-hover">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <p className="text-body-sm text-[var(--text-secondary)] font-medium">Active Campaigns</p>
                <p className="text-h2 text-[var(--text-primary)] tracking-tight">{dashboard.overview.campaigns_active}</p>
              </div>
              <div className="p-3 rounded-lg bg-[var(--color-primary-100)] dark:bg-[var(--color-primary-900)]/20">
                <Activity className="w-5 h-5 text-[var(--color-primary-500)]" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="card-hover">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <p className="text-body-sm text-[var(--text-secondary)] font-medium">Qualified Leads</p>
                <p className="text-h2 text-[var(--text-primary)] tracking-tight">{formatNumber(dashboard.overview.leads_qualified_30d)}</p>
                <p className="text-caption text-[var(--text-muted)]">
                  {formatPercent(dashboard.overview.qualification_rate)} qualification rate
                </p>
              </div>
              <div className="p-3 rounded-lg bg-[var(--color-success-100)] dark:bg-[var(--color-success-900)]/20">
                <Target className="w-5 h-5 text-[var(--color-success-500)]" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="card-hover">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <p className="text-body-sm text-[var(--text-secondary)] font-medium">Emails Sent</p>
                <p className="text-h2 text-[var(--text-primary)] tracking-tight">{formatNumber(dashboard.overview.emails_sent_30d)}</p>
                <p className="text-caption text-[var(--text-muted)]">
                  {formatPercent(dashboard.overview.email_open_rate)} open rate
                </p>
              </div>
              <div className="p-3 rounded-lg bg-[var(--color-info-100)] dark:bg-[var(--color-info-900)]/20">
                <Mail className="w-5 h-5 text-[var(--color-info-500)]" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="card-hover">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <p className="text-body-sm text-[var(--text-secondary)] font-medium">AI Success Rate</p>
                <p className="text-h2 text-[var(--text-primary)] tracking-tight">{formatPercent(dashboard.ai_agents.success_rate)}</p>
                <p className="text-caption text-[var(--text-muted)]">
                  {dashboard.ai_agents.total_agent_runs} total runs
                </p>
              </div>
              <div className="p-3 rounded-lg bg-[var(--color-accent-100)] dark:bg-[var(--color-accent-900)]/20">
                <Zap className="w-5 h-5 text-[var(--color-accent-500)]" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Analytics */}
      <Tabs defaultValue="performance" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="growth">Growth</TabsTrigger>
          <TabsTrigger value="team">Team</TabsTrigger>
          <TabsTrigger value="agents">AI Agents</TabsTrigger>
        </TabsList>

        <TabsContent value="performance" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-h4">
                  <BarChart3 className="w-5 h-5 mr-3 text-[var(--text-muted)]" />
                  Campaign Performance
                </CardTitle>
                <CardDescription>Last 30 days metrics</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <p className="text-body-sm text-[var(--text-secondary)] font-medium">Leads Processed</p>
                    <p className="text-h3 text-[var(--text-primary)]">{formatNumber(dashboard.overview.leads_processed_30d)}</p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-body-sm text-[var(--text-secondary)] font-medium">Leads Qualified</p>
                    <p className="text-h3 text-[var(--text-primary)]">{formatNumber(dashboard.overview.leads_qualified_30d)}</p>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <p className="text-body-sm text-[var(--text-secondary)] font-medium">Qualification Rate</p>
                    <p className="text-body-sm font-medium text-[var(--text-primary)]">{formatPercent(dashboard.overview.qualification_rate)}</p>
                  </div>
                  <div className="w-full bg-[var(--surface-secondary)] rounded-full h-2">
                    <div
                      className="h-2 bg-[var(--color-success-500)] rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(dashboard.overview.qualification_rate, 100)}%` }}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-h4">
                  <Mail className="w-5 h-5 mr-3 text-[var(--text-muted)]" />
                  Email Performance
                </CardTitle>
                <CardDescription>Engagement metrics</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <p className="text-body-sm text-[var(--text-secondary)] font-medium">Total Sent</p>
                  <p className="text-h3 text-[var(--text-primary)]">{formatNumber(dashboard.overview.emails_sent_30d)}</p>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <p className="text-body-sm text-[var(--text-secondary)] font-medium">Open Rate</p>
                    <p className="text-body-sm font-medium text-[var(--text-primary)]">{formatPercent(dashboard.overview.email_open_rate)}</p>
                  </div>
                  <div className="w-full bg-[var(--surface-secondary)] rounded-full h-2">
                    <div
                      className="h-2 bg-[var(--color-info-500)] rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(dashboard.overview.email_open_rate, 100)}%` }}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="growth" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-h4">
                  <TrendingUp className="w-5 h-5 mr-3 text-[var(--text-muted)]" />
                  Leads Growth
                </CardTitle>
                <CardDescription>7-day vs previous period comparison</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <p className="text-caption text-[var(--text-secondary)] uppercase font-medium tracking-wider">Current Period</p>
                    <p className="text-h3 text-[var(--text-primary)]">{formatNumber(dashboard.growth.leads_7d_vs_30d.current)}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-caption text-[var(--text-secondary)] uppercase font-medium tracking-wider">Previous Period</p>
                    <p className="text-h4 text-[var(--text-secondary)]">{formatNumber(dashboard.growth.leads_7d_vs_30d.previous)}</p>
                  </div>
                </div>
                <div className={cn(
                  "flex items-center space-x-2 text-body-sm font-medium",
                  leadsGrowth >= 0 ? "text-[var(--color-success-500)]" : "text-[var(--color-error-500)]"
                )}>
                  {leadsGrowth >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                  <span>{formatPercent(Math.abs(leadsGrowth))} {leadsGrowth >= 0 ? 'growth' : 'decline'}</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-h4">
                  <Mail className="w-5 h-5 mr-3 text-[var(--text-muted)]" />
                  Email Growth
                </CardTitle>
                <CardDescription>Email activity comparison</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <p className="text-caption text-[var(--text-secondary)] uppercase font-medium tracking-wider">Current Period</p>
                    <p className="text-h3 text-[var(--text-primary)]">{formatNumber(dashboard.growth.emails_7d_vs_30d.current)}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-caption text-[var(--text-secondary)] uppercase font-medium tracking-wider">Previous Period</p>
                    <p className="text-h4 text-[var(--text-secondary)]">{formatNumber(dashboard.growth.emails_7d_vs_30d.previous)}</p>
                  </div>
                </div>
                <div className={cn(
                  "flex items-center space-x-2 text-body-sm font-medium",
                  emailsGrowth >= 0 ? "text-[var(--color-success-500)]" : "text-[var(--color-error-500)]"
                )}>
                  {emailsGrowth >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                  <span>{formatPercent(Math.abs(emailsGrowth))} {emailsGrowth >= 0 ? 'growth' : 'decline'}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="team" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-h4">
                <Users className="w-5 h-5 mr-3 text-[var(--text-muted)]" />
                Team Activity
              </CardTitle>
              <CardDescription>User engagement across your organization</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <p className="text-body-sm text-[var(--text-secondary)] font-medium">Total Users</p>
                      <p className="text-h2 text-[var(--text-primary)]">{dashboard.team.total_users}</p>
                    </div>
                    <div className="space-y-2">
                      <p className="text-body-sm text-[var(--text-secondary)] font-medium">Active Users</p>
                      <p className="text-h2 text-[var(--text-primary)]">{dashboard.team.active_users}</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <p className="text-body-sm text-[var(--text-secondary)] font-medium">Activity Rate</p>
                      <p className="text-body font-medium text-[var(--text-primary)]">{formatPercent(dashboard.team.user_activity_rate)}</p>
                    </div>
                    <div className="w-full bg-[var(--surface-secondary)] rounded-full h-2">
                      <div
                        className="h-2 bg-[var(--color-primary-500)] rounded-full transition-all duration-500"
                        style={{ width: `${dashboard.team.user_activity_rate}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <p className="text-body-sm text-[var(--text-secondary)] font-medium">Role Distribution</p>
                  <div className="space-y-3">
                    {Object.entries(dashboard.team.role_distribution).map(([role, count]) => (
                      <div key={role} className="flex items-center justify-between py-2">
                        <span className="text-body text-[var(--text-primary)] capitalize">{role}</span>
                        <Badge variant="secondary" className="text-xs">{count}</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="agents" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-h4">
                <Bot className="w-5 h-5 mr-3 text-[var(--text-muted)]" />
                AI Agent Performance
              </CardTitle>
              <CardDescription>Automated execution metrics and success rates</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div className="space-y-4">
                    <div className="text-center p-6 rounded-lg bg-[var(--surface-secondary)]">
                      <p className="text-h1 text-[var(--text-primary)] mb-2">{formatPercent(dashboard.ai_agents.success_rate)}</p>
                      <p className="text-body-sm text-[var(--text-secondary)] font-medium">Success Rate</p>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <p className="text-h3 text-[var(--text-primary)] mb-1">{dashboard.ai_agents.total_agent_runs}</p>
                        <p className="text-caption text-[var(--text-secondary)]">Total Runs</p>
                      </div>
                      <div className="text-center">
                        <p className="text-h3 text-[var(--text-primary)] mb-1">{dashboard.ai_agents.successful_runs}</p>
                        <p className="text-caption text-[var(--text-secondary)]">Successful</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <p className="text-body-sm text-[var(--text-secondary)] font-medium">Execution Breakdown</p>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between py-3 px-4 rounded-lg border border-[var(--border-primary)]">
                      <div className="flex items-center space-x-3">
                        <Target className="h-4 w-4 text-[var(--color-primary-500)]" />
                        <span className="text-body text-[var(--text-primary)]">Prospector Agent</span>
                      </div>
                      <Badge variant="outline" className="text-xs">{dashboard.ai_agents.prospector_runs} runs</Badge>
                    </div>
                    <div className="flex items-center justify-between py-3 px-4 rounded-lg border border-[var(--border-primary)]">
                      <div className="flex items-center space-x-3">
                        <CheckCircle className="h-4 w-4 text-[var(--color-success-500)]" />
                        <span className="text-body text-[var(--text-primary)]">BANT Agent</span>
                      </div>
                      <Badge variant="outline" className="text-xs">{dashboard.ai_agents.bant_runs} runs</Badge>
                    </div>
                    <div className="flex items-center justify-between py-3 px-4 rounded-lg border border-[var(--border-primary)]">
                      <div className="flex items-center space-x-3">
                        <Clock className="h-4 w-4 text-[var(--color-accent-500)]" />
                        <span className="text-body text-[var(--text-primary)]">Scheduler Agent</span>
                      </div>
                      <Badge variant="outline" className="text-xs">{dashboard.ai_agents.scheduler_runs} runs</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}