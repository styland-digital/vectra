// ============================================
// Enums
// ============================================

export enum UserRole {
  OWNER = "owner",
  ADMIN = "admin",
  MANAGER = "manager",
  OPERATOR = "operator",
  VIEWER = "viewer",
  PLATFORM_ADMIN = "platform_admin",
}

export enum CampaignStatus {
  DRAFT = "draft",
  ACTIVE = "active",
  PAUSED = "paused",
  COMPLETED = "completed",
  ARCHIVED = "archived",
}

export enum EmailStatus {
  PENDING = "pending",
  APPROVED = "approved",
  REJECTED = "rejected",
  SENT = "sent",
  DELIVERED = "delivered",
  BOUNCED = "bounced",
}

export enum LeadStatus {
  NEW = "new",
  ENRICHED = "enriched",
  SCORING = "scoring",
  QUALIFIED = "qualified",
  CONTACTED = "contacted",
  MEETING_SCHEDULED = "meeting_scheduled",
  COMPLETED = "completed",
  REJECTED = "rejected",
}

export enum LeadIntent {
  HIGH = "high",
  MEDIUM = "medium",
  LOW = "low",
  UNKNOWN = "unknown",
}

export enum PlanType {
  TRIAL = "trial",
  STARTER = "starter",
  GROWTH = "growth",
  SCALE = "scale",
}

// ============================================
// Auth
// ============================================

export interface Organization {
  id: string
  name: string
  slug: string
  plan: string
  settings: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  role: UserRole
  is_active: boolean
  created_at: string
}

export interface UserWithOrg extends User {
  organization: Organization
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: UserWithOrg
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface RegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
  organization_name: string
}

export interface MessageResponse {
  message: string
}

// ============================================
// Campaigns
// ============================================

export interface CampaignUserInfo {
  id: string
  first_name: string | null
  last_name: string | null
  email: string
}

export interface Campaign {
  id: string
  organization_id: string
  created_by: string | null
  created_by_user: CampaignUserInfo | null
  launched_by: string | null
  launched_by_user: CampaignUserInfo | null
  name: string
  description: string
  status: CampaignStatus
  target_criteria: Record<string, unknown>
  email_template: Record<string, unknown>
  bant_threshold: number
  daily_limit: number
  started_at: string | null
  completed_at: string | null
  created_at: string
  updated_at: string
}

export interface CampaignCreate {
  name: string
  description?: string
  target_criteria?: Record<string, unknown>
  email_template?: Record<string, unknown>
  bant_threshold?: number
  daily_limit?: number
}

export interface CampaignUpdate extends Partial<CampaignCreate> {}

export interface CampaignStats {
  campaign_id: string
  status: CampaignStatus
  leads: Record<string, number>
  emails: Record<string, number>
  bant: Record<string, number>
  started_at: string | null
  completed_at: string | null
}

// ============================================
// Leads
// ============================================

export interface CompanyInfo {
  name: string
  domain: string
  size: string
  industry: string
  location: string
}

export interface JobInfo {
  title: string
  department: string
  seniority: string
}

export interface BANTInfo {
  score: number
  budget: number
  authority: number
  need: number
  timeline: number
  notes: string
}

export interface Lead {
  id: string
  campaign_id: string
  email: string
  first_name: string
  last_name: string
  phone: string | null
  linkedin_url: string | null
  company: CompanyInfo | null
  job: JobInfo | null
  bant: BANTInfo | null
  intent: LeadIntent
  intent_confidence: number
  status: LeadStatus
  email_status: EmailStatus | null
  email_sent_at: string | null
  email_opened_at: string | null
  enriched_at: string | null
  qualified_at: string | null
  created_at: string
}

export interface Interaction {
  id: string
  type: string
  agent_type: string
  data: Record<string, unknown>
  created_at: string
}

export interface LeadDetail extends Lead {
  interactions: Interaction[]
  emails: Email[]
  meetings: Meeting[]
}

export interface LeadListResponse {
  data: Lead[]
  pagination: Pagination
}

export interface Pagination {
  total: number
  skip: number
  limit: number
  has_more: boolean
}

// ============================================
// Emails
// ============================================

export interface LeadSummary {
  email: string
  name: string
  company: string
}

export interface TrackingInfo {
  opened_count: number
  first_opened_at: string | null
  last_opened_at: string | null
  clicked_count: number
  first_clicked_at: string | null
}

export interface Email {
  id: string
  lead_id: string
  campaign_id: string
  lead: LeadSummary
  subject: string
  body_preview: string
  status: EmailStatus
  generated_by: string
  opened_at: string | null
  clicked_at: string | null
  created_at: string
}

export interface EmailDetail {
  id: string
  lead_id: string
  campaign_id: string
  subject: string
  body_html: string
  body_text: string
  from_email: string
  from_name: string
  to_email: string
  status: EmailStatus
  generated_by: string
  generation_model: string
  approved_by: Record<string, unknown> | null
  approved_at: string | null
  sent_at: string | null
  tracking: TrackingInfo | null
  created_at: string
}

export interface EmailListResponse {
  data: Email[]
  pagination: Pagination
}

// ============================================
// Meetings
// ============================================

export interface Meeting {
  id: string
  lead_id: string
  scheduled_at: string
  status: string
  calendly_url: string | null
  notes: string | null
  created_at: string
}

// ============================================
// Billing
// ============================================

export interface PlanFeatures {
  leads_per_month: number
  campaigns_active: number
  users: number
  emails_per_day: number
  support: string
}

export interface Plan {
  id: string
  name: string
  price: number
  currency: string
  interval: string
  features: PlanFeatures
  stripe_price_id: string
}

export interface Subscription {
  id: string
  organization_id: string
  plan: Plan
  status: string
  current_period_start: string
  current_period_end: string
  cancel_at_period_end: boolean
}

export interface CheckoutSessionCreate {
  plan_type: PlanType
  customer_id?: string
  success_url: string
  cancel_url: string
}

export interface CheckoutSessionResponse {
  session_id: string
  session_url: string
}

export interface PortalSessionResponse {
  session_url: string
}

// ============================================
// Analytics
// ============================================

export interface OverviewMetrics {
  active_campaigns: number
  qualified_leads: number
  emails_sent: number
  ai_success_rate: number
}

export interface GrowthMetrics {
  leads_current: number
  leads_previous: number
  leads_change: number
  emails_current: number
  emails_previous: number
  emails_change: number
}

export interface TeamMetrics {
  total_users: number
  active_users: number
  user_activity_rate: number
  role_distribution: Record<string, number>
  period_days: number
}

export interface AIAgentMetrics {
  total_agent_runs: number
  successful_runs: number
  success_rate: number
  prospector_runs: number
  bant_runs: number
  scheduler_runs: number
  period_days: number
}

export interface SubscriptionInfo {
  plan: string
  status: string
  leads_used: number
  leads_limit: number
}

export interface AnalyticsDashboard {
  overview: OverviewMetrics
  growth: GrowthMetrics
  team: TeamMetrics
  ai_agents: AIAgentMetrics
  subscription: SubscriptionInfo
  generated_at: string
}

export interface UsageMetrics {
  campaigns_created: number
  campaigns_active: number
  leads_processed: number
  leads_qualified: number
  qualification_rate: number
  emails_sent: number
  emails_opened: number
  emails_clicked: number
  email_open_rate: number
  email_click_rate: number
  bant_average_score: number
  period_days: number
}

export interface EngagementMetrics {
  total_users: number
  active_users: number
  user_activity_rate: number
  role_distribution: Record<string, number>
  period_days: number
}

// ============================================
// Organization Users
// ============================================

export interface OrganizationUser {
  id: string
  email: string
  first_name: string
  last_name: string
  role: UserRole
  is_active: boolean
  email_verified_at: string | null
  last_login_at: string | null
  created_at: string
}

export interface InviteUserRequest {
  email: string
  role?: string
  first_name: string
  last_name: string
}

export interface CreateUserRequest {
  email: string
  role: string
  password?: string
  first_name: string
  last_name: string
  send_welcome_email?: boolean
}

export interface UpdateUserRoleRequest {
  role: string
}

// ============================================
// Notifications
// ============================================

export interface NotificationResponse {
  success: boolean
  message: string
  sent_count: number
  failed_count: number
}

// ============================================
// Analytics Events
// ============================================

export interface AnalyticsEventTrack {
  event_type: string
  properties?: Record<string, unknown>
  value?: number
}

export interface EventTrackResponse {
  success: boolean
  message: string
}
