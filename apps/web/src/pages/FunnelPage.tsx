import { useQuery } from '@tanstack/react-query'
import { funnelApi } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { TrendingDown } from 'lucide-react'

export default function FunnelPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['funnel'],
    queryFn: funnelApi.get,
  })

  const chartData = data?.stages.map((stage) => ({
    stage: stage.stage.toUpperCase(),
    count: stage.count,
    value: stage.total_value,
    conversionRate: stage.conversion_rate,
  }))

  const colors = {
    new: '#3b82f6',
    contacted: '#06b6d4',
    qualified: '#8b5cf6',
    proposal: '#eab308',
    negotiation: '#f97316',
    won: '#10b981',
    lost: '#ef4444',
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Sales Funnel</h1>

      {/* Summary Stats */}
      {data && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <p className="text-sm font-medium text-gray-600 mb-1">Total Leads</p>
            <p className="text-3xl font-bold text-gray-900">{data.total_leads}</p>
          </div>
          <div className="card">
            <p className="text-sm font-medium text-gray-600 mb-1">Pipeline Value</p>
            <p className="text-3xl font-bold text-gray-900">
              ${(data.total_value / 1000).toFixed(0)}K
            </p>
          </div>
          <div className="card">
            <p className="text-sm font-medium text-gray-600 mb-1">Conversion Rate</p>
            <p className="text-3xl font-bold text-gray-900">
              {data.overall_conversion_rate.toFixed(1)}%
            </p>
          </div>
        </div>
      )}

      {/* Funnel Visualization */}
      <div className="card mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">Lead Count by Stage</h2>
        {isLoading ? (
          <div className="text-center py-12 text-gray-500">Loading...</div>
        ) : chartData && chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis
                type="number"
                tick={{ fill: '#6b7280', fontSize: 12 }}
                tickLine={{ stroke: '#e5e7eb' }}
              />
              <YAxis
                dataKey="stage"
                type="category"
                width={100}
                tick={{ fill: '#6b7280', fontSize: 12 }}
                tickLine={{ stroke: '#e5e7eb' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
                labelStyle={{
                  fontWeight: 600,
                  color: '#111827',
                  marginBottom: '4px'
                }}
              />
              <Bar
                dataKey="count"
                radius={[0, 8, 8, 0]}
                animationDuration={800}
                animationBegin={100}
                animationEasing="ease-out"
              >
                {chartData.map((entry, index) => {
                  const stageKey = data?.stages[index].stage as keyof typeof colors
                  return <Cell key={`cell-${index}`} fill={colors[stageKey] || '#6b7280'} />
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="text-center py-12 text-gray-500">No data available</div>
        )}
      </div>

      {/* Stage Details */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Stage Breakdown</h2>
        <div className="space-y-4">
          {data?.stages.map((stage, index) => {
            const stageKey = stage.stage as keyof typeof colors
            return (
              <div key={stage.stage} className="relative">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: colors[stageKey] || '#6b7280' }}
                    />
                    <span className="font-medium text-gray-900 capitalize">
                      {stage.stage.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm text-gray-600">
                      {stage.count} leads
                    </span>
                    <span className="text-sm font-semibold text-gray-900">
                      ${(stage.total_value / 1000).toFixed(0)}K
                    </span>
                    {stage.conversion_rate !== null && stage.conversion_rate !== undefined && (
                      <div className="flex items-center gap-1 text-sm text-gray-600">
                        <TrendingDown size={14} />
                        {stage.conversion_rate.toFixed(1)}%
                      </div>
                    )}
                  </div>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full transition-all"
                    style={{
                      width: `${(stage.count / (data.total_leads || 1)) * 100}%`,
                      backgroundColor: colors[stageKey] || '#6b7280',
                    }}
                  />
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
