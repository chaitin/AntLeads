/**
 * Lead types matching backend API
 */

export enum LeadSource {
  GOOGLE_ADS = 'google_ads',
  META_ADS = 'meta_ads',
  TIKTOK_ADS = 'tiktok_ads',
  LANDING_PAGE = 'landing_page',
  WEB_FORM = 'web_form',
  EVENT = 'event',
  IMPORT = 'import',
  REFERRAL = 'referral',
  DIRECT = 'direct',
  OTHER = 'other',
}

export enum LeadStage {
  NEW = 'new',
  CONTACTED = 'contacted',
  QUALIFIED = 'qualified',
  PROPOSAL = 'proposal',
  NEGOTIATION = 'negotiation',
  WON = 'won',
  LOST = 'lost',
}

export enum LeadPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface ContactInfo {
  email?: string
  phone?: string
  company?: string
  title?: string
  website?: string
}

export interface Lead {
  id: string
  name: string
  source: LeadSource
  stage: LeadStage
  priority: LeadPriority
  score: number
  contact_info: ContactInfo
  tags: string[]
  product_interest?: string
  estimated_value?: number
  notes?: string
  utm_source?: string
  utm_medium?: string
  utm_campaign?: string
  referrer_url?: string
  assigned_to?: string
  created_at: string
  updated_at: string
  contacted_at?: string
  closed_at?: string
}

export interface LeadStats {
  total_leads: number
  by_stage: Record<string, number>
  by_source: Record<string, number>
  by_priority: Record<string, number>
  average_score: number
  total_estimated_value: number
}

export interface FunnelStageData {
  stage: LeadStage
  count: number
  total_value: number
  conversion_rate?: number
  average_days?: number
}

export interface FunnelData {
  stages: FunnelStageData[]
  total_leads: number
  total_value: number
  overall_conversion_rate: number
  period_start?: string
  period_end?: string
}

export enum TaskType {
  CALL = 'call',
  EMAIL = 'email',
  MEETING = 'meeting',
  FOLLOW_UP = 'follow_up',
  DEMO = 'demo',
  PROPOSAL = 'proposal',
  REMINDER = 'reminder',
  OTHER = 'other',
}

export enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface Task {
  id: string
  lead_id: string
  title: string
  description?: string
  task_type: TaskType
  status: TaskStatus
  priority: TaskPriority
  assigned_to?: string
  due_date?: string
  reminder_at?: string
  completed_at?: string
  completed_by?: string
  created_at: string
  updated_at: string
}
