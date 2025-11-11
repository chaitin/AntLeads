import { useQuery } from '@tanstack/react-query'
import { leadsApi, funnelApi, tasksApi } from '../services/api'
import { TrendingUp, Users, CheckSquare, DollarSign, AlertCircle } from 'lucide-react'

export default function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['lead-stats'],
    queryFn: leadsApi.getStats,
  })

  const { data: funnel } = useQuery({
    queryKey: ['funnel'],
    queryFn: funnelApi.get,
  })

  const { data: tasksData } = useQuery({
    queryKey: ['tasks', { status: 'pending' }],
    queryFn: () => tasksApi.getAll({ status: 'pending', page_size: 5 }),
  })

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={<Users className="text-blue-600" size={24} />}
          title="Total Leads"
          value={stats?.total_leads ?? 0}
          trend="+12% from last month"
        />
        <StatCard
          icon={<TrendingUp className="text-green-600" size={24} />}
          title="Avg Score"
          value={stats?.average_score.toFixed(1) ?? '0'}
          trend="Quality improving"
        />
        <StatCard
          icon={<DollarSign className="text-purple-600" size={24} />}
          title="Est. Value"
          value={`$${((stats?.total_estimated_value ?? 0) / 1000).toFixed(0)}K`}
          trend="Pipeline value"
        />
        <StatCard
          icon={<CheckSquare className="text-orange-600" size={24} />}
          title="Pending Tasks"
          value={tasksData?.total ?? 0}
          trend="Need attention"
        />
      </div>

      {/* Stage Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Leads by Stage</h2>
          <div className="space-y-3">
            {stats?.by_stage &&
              Object.entries(stats.by_stage).map(([stage, count]) => (
                <div key={stage} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${getStageColor(stage)}`} />
                    <span className="text-sm font-medium capitalize">{stage.replace('_', ' ')}</span>
                  </div>
                  <span className="text-sm font-semibold text-gray-900">{count}</span>
                </div>
              ))}
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Leads by Source</h2>
          <div className="space-y-3">
            {stats?.by_source &&
              Object.entries(stats.by_source)
                .slice(0, 6)
                .map(([source, count]) => (
                  <div key={source} className="flex items-center justify-between">
                    <span className="text-sm font-medium capitalize">{source.replace('_', ' ')}</span>
                    <span className="text-sm font-semibold text-gray-900">{count}</span>
                  </div>
                ))}
          </div>
        </div>
      </div>

      {/* Recent Tasks */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Upcoming Tasks</h2>
          <a href="/tasks" className="text-sm text-blue-600 hover:text-blue-700 font-medium">
            View all →
          </a>
        </div>
        {tasksData?.tasks && tasksData.tasks.length > 0 ? (
          <div className="space-y-3">
            {tasksData.tasks.map((task) => (
              <div
                key={task.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <CheckSquare size={18} className="text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{task.title}</p>
                    <p className="text-xs text-gray-500">
                      {task.due_date
                        ? new Date(task.due_date).toLocaleDateString()
                        : 'No due date'}
                    </p>
                  </div>
                </div>
                <span className={`badge badge-${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <AlertCircle className="mx-auto mb-2" size={32} />
            <p>No pending tasks</p>
          </div>
        )}
      </div>
    </div>
  )
}

function StatCard({
  icon,
  title,
  value,
  trend,
}: {
  icon: React.ReactNode
  title: string
  value: string | number
  trend: string
}) {
  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          <p className="text-xs text-gray-500 mt-1">{trend}</p>
        </div>
        <div className="p-2 bg-gray-50 rounded-lg">{icon}</div>
      </div>
    </div>
  )
}

function getStageColor(stage: string): string {
  const colors: Record<string, string> = {
    new: 'bg-blue-500',
    contacted: 'bg-cyan-500',
    qualified: 'bg-purple-500',
    proposal: 'bg-yellow-500',
    negotiation: 'bg-orange-500',
    won: 'bg-green-500',
    lost: 'bg-red-500',
  }
  return colors[stage] || 'bg-gray-500'
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
