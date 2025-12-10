import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { analyticsAPI } from '../services/api'
import { Clock, Users, CheckCircle, TrendingUp } from 'lucide-react'

const COLORS = ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#EF4444']

export default function Analytics() {
  const { data: dashboard } = useQuery({
    queryKey: ['dashboard-analytics'],
    queryFn: () => analyticsAPI.getDashboard(),
  })

  const dashboardData = dashboard?.data || {}
  const agentPerf = dashboardData.agent_performance || {}

  // Prepare agent performance data for charts
  const agentData = Object.entries(agentPerf).map(([agent, stats]) => ({
    agent: agent.charAt(0).toUpperCase() + agent.slice(1),
    interactions: stats.interactions || 0,
    handoffs: stats.handoffs || 0,
  }))

  const timeMetrics = dashboardData.time_metrics || {}

  return (
    <div className="space-y-6">
      {/* Time Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-100 p-3 rounded-lg">
              <Clock className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Avg. Time to Sanction</p>
              <p className="text-2xl font-bold text-gray-900">
                {timeMetrics.avg_time_to_sanction_minutes?.toFixed(0) || 0} min
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3">
            <div className="bg-green-100 p-3 rounded-lg">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Fastest Approval</p>
              <p className="text-2xl font-bold text-gray-900">
                {timeMetrics.min_time_minutes?.toFixed(0) || 0} min
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3">
            <div className="bg-purple-100 p-3 rounded-lg">
              <CheckCircle className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Median Time</p>
              <p className="text-2xl font-bold text-gray-900">
                {timeMetrics.median_time_minutes?.toFixed(0) || 0} min
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Performance Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Agent Performance</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={agentData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="agent" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="interactions" fill="#3B82F6" name="Interactions" />
            <Bar dataKey="handoffs" fill="#10B981" name="Successful Handoffs" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Status Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Application Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Initiated', value: 30 },
                  { name: 'Under Review', value: 25 },
                  { name: 'Approved', value: 20 },
                  { name: 'Sanctioned', value: 15 },
                  { name: 'Rejected', value: 10 },
                ]}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {COLORS.map((color, index) => (
                  <Cell key={`cell-${index}`} fill={color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Insights</h3>
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="bg-green-100 p-2 rounded">
                <TrendingUp className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">40% Improvement</p>
                <p className="text-sm text-gray-600">Conversion rate increased vs traditional process</p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="bg-blue-100 p-2 rounded">
                <Clock className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">95% Faster</p>
                <p className="text-sm text-gray-600">Average time to sanction reduced from days to minutes</p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="bg-purple-100 p-2 rounded">
                <Users className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">60% Cost Reduction</p>
                <p className="text-sm text-gray-600">Manual processing costs significantly decreased</p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="bg-orange-100 p-2 rounded">
                <CheckCircle className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">95% Accuracy</p>
                <p className="text-sm text-gray-600">Document verification accuracy rate</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


