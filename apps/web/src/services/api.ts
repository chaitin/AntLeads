import axios from 'axios'
import type { Lead, LeadStats, FunnelData, Task } from '../types'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const leadsApi = {
  getAll: async (params?: { page?: number; page_size?: number; stage?: string; search?: string }) => {
    const { data } = await api.get('/leads/', { params })
    return data
  },

  getById: async (id: string) => {
    const { data } = await api.get<Lead>(`/leads/${id}`)
    return data
  },

  create: async (lead: Partial<Lead>) => {
    const { data } = await api.post<Lead>('/leads/', lead)
    return data
  },

  update: async (id: string, updates: Partial<Lead>) => {
    const { data } = await api.patch<Lead>(`/leads/${id}`, updates)
    return data
  },

  delete: async (id: string) => {
    await api.delete(`/leads/${id}`)
  },

  getStats: async () => {
    const { data } = await api.get<LeadStats>('/leads/stats/overview')
    return data
  },

  importLeads: async (leads: Partial<Lead>[]) => {
    const { data } = await api.post('/leads/import', { leads, source: 'import' })
    return data
  },
}

export const funnelApi = {
  get: async (params?: { start_date?: string; end_date?: string }) => {
    const { data } = await api.get<FunnelData>('/funnel/', { params })
    return data
  },
}

export const tasksApi = {
  getAll: async (params?: {
    page?: number
    page_size?: number
    lead_id?: string
    status?: string
    assigned_to?: string
  }) => {
    const { data } = await api.get('/tasks/', { params })
    return data
  },

  getById: async (id: string) => {
    const { data } = await api.get<Task>(`/tasks/${id}`)
    return data
  },

  create: async (task: Partial<Task>) => {
    const { data } = await api.post<Task>('/tasks/', task)
    return data
  },

  update: async (id: string, updates: Partial<Task>) => {
    const { data } = await api.patch<Task>(`/tasks/${id}`, updates)
    return data
  },

  delete: async (id: string) => {
    await api.delete(`/tasks/${id}`)
  },
}

export const automationApi = {
  getOverdueTasks: async () => {
    const { data } = await api.get<Task[]>('/automation/overdue')
    return data
  },

  getTasksNeedingReminders: async () => {
    const { data } = await api.get<Task[]>('/automation/reminders')
    return data
  },

  createStaleLeadTasks: async (daysInactive: number = 7) => {
    const { data } = await api.post<Task[]>('/automation/stale-leads', null, {
      params: { days_inactive: daysInactive },
    })
    return data
  },
}
