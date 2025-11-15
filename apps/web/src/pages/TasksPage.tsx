import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { tasksApi, leadsApi } from '../services/api'
import { Plus, CheckSquare, X } from 'lucide-react'
import type { Task, TaskStatus, TaskType, TaskPriority, Lead } from '../types'

export default function TasksPage() {
  const [statusFilter, setStatusFilter] = useState<TaskStatus | ''>('')
  const [showModal, setShowModal] = useState(false)

  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['tasks', { status: statusFilter }],
    queryFn: () =>
      tasksApi.getAll({
        page_size: 50,
        status: statusFilter || undefined,
      }),
  })

  const { data: leadsData } = useQuery({
    queryKey: ['leads-list'],
    queryFn: () => leadsApi.getAll({ page_size: 100 }),
    enabled: showModal,
  })

  const createMutation = useMutation({
    mutationFn: tasksApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      setShowModal(false)
    },
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)

    const taskData = {
      lead_id: formData.get('lead_id') as string,
      title: formData.get('title') as string,
      description: formData.get('description') as string || undefined,
      task_type: formData.get('task_type') as TaskType,
      priority: formData.get('priority') as TaskPriority,
      due_date: formData.get('due_date')
        ? new Date(formData.get('due_date') as string).toISOString()
        : undefined,
    }

    createMutation.mutate(taskData)
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={18} />
          Add Task
        </button>
      </div>

      {/* Filter */}
      <div className="card mb-6">
        <select
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as TaskStatus | '')}
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      {/* Tasks List */}
      <div className="space-y-3">
        {isLoading ? (
          <div className="card text-center py-12 text-gray-500">Loading...</div>
        ) : data?.tasks && data.tasks.length > 0 ? (
          data.tasks.map((task: Task) => (
            <div key={task.id} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4 flex-1">
                  <CheckSquare
                    size={20}
                    className={
                      task.status === 'completed' ? 'text-green-600' : 'text-gray-400'
                    }
                  />
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900 mb-1">{task.title}</h3>
                    {task.description && (
                      <p className="text-sm text-gray-600 mb-2">{task.description}</p>
                    )}
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <span className="capitalize">{task.task_type.replace('_', ' ')}</span>
                      {task.due_date && (
                        <span>Due: {new Date(task.due_date).toLocaleDateString()}</span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`badge badge-${getStatusColor(task.status)}`}>
                    {task.status.replace('_', ' ')}
                  </span>
                  <span className={`badge badge-${getPriorityColor(task.priority)}`}>
                    {task.priority}
                  </span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="card text-center py-12 text-gray-500">
            <CheckSquare className="mx-auto mb-2" size={32} />
            <p>No tasks found</p>
          </div>
        )}
      </div>

      {/* Add Task Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4" style={{ zIndex: 1000 }}>
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Add New Task</h2>
              <button
                onClick={() => setShowModal(false)}
                className="modal-close-icon"
                aria-label="Close modal"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Lead <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="lead_id"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select a lead</option>
                    {leadsData?.leads.map((lead: Lead) => (
                      <option key={lead.id} value={lead.id}>
                        {lead.name} - {lead.contact_info.company || 'No Company'}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Title <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="title"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    name="description"
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Task Type <span className="text-red-500">*</span>
                    </label>
                    <select
                      name="task_type"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="call">Call</option>
                      <option value="email">Email</option>
                      <option value="meeting">Meeting</option>
                      <option value="follow_up">Follow Up</option>
                      <option value="demo">Demo</option>
                      <option value="proposal">Proposal</option>
                      <option value="reminder">Reminder</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Priority <span className="text-red-500">*</span>
                    </label>
                    <select
                      name="priority"
                      required
                      defaultValue="medium"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="urgent">Urgent</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                  <input
                    type="datetime-local"
                    name="due_date"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={createMutation.isPending}
                >
                  {createMutation.isPending ? 'Creating...' : 'Create Task'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    pending: 'warning',
    in_progress: 'info',
    completed: 'success',
    cancelled: 'gray',
  }
  return colors[status] || 'gray'
}

function getPriorityColor(priority: string): string {
  const colors: Record<string, string> = {
    low: 'gray',
    medium: 'info',
    high: 'warning',
    urgent: 'danger',
  }
  return colors[priority] || 'gray'
}
