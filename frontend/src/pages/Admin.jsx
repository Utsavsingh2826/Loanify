import React, { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { 
  Users, FileText, TrendingUp, DollarSign, 
  Activity, BarChart3, PieChart, ArrowUpRight 
} from 'lucide-react'
import { adminAPI, analyticsAPI } from '../services/api'
import ConversionFunnel from '../components/ConversionFunnel'
import Analytics from '../components/Analytics'

export default function Admin() {
  const [activeView, setActiveView] = useState('overview')

  // Fetch overview stats
  const { data: stats, isLoading } = useQuery({
    queryKey: ['overview-stats'],
    queryFn: () => adminAPI.getOverviewStats(),
  })

  const overviewData = stats?.data || {}

  const StatCard = ({ title, value, icon: Icon, trend, color }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {trend && (
            <div className="flex items-center space-x-1 mt-2">
              <ArrowUpRight className={`w-4 h-4 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`} />
              <span className={`text-sm ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {Math.abs(trend)}%
              </span>
            </div>
          )}
        </div>
        <div className={`p-4 rounded-lg ${color}`}>
          <Icon className="w-8 h-8" />
        </div>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
              <p className="text-gray-600">LoaniFi Analytics & Management</p>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setActiveView('overview')}
                className={`px-4 py-2 rounded-md ${
                  activeView === 'overview'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveView('applications')}
                className={`px-4 py-2 rounded-md ${
                  activeView === 'applications'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Applications
              </button>
              <button
                onClick={() => setActiveView('analytics')}
                className={`px-4 py-2 rounded-md ${
                  activeView === 'analytics'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Analytics
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeView === 'overview' && (
          <>
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <StatCard
                title="Total Conversations"
                value={overviewData.total?.conversations || 0}
                icon={Users}
                trend={15}
                color="bg-blue-100 text-blue-600"
              />
              <StatCard
                title="Total Applications"
                value={overviewData.total?.applications || 0}
                icon={FileText}
                trend={22}
                color="bg-green-100 text-green-600"
              />
              <StatCard
                title="Sanctioned Loans"
                value={overviewData.total?.sanctioned || 0}
                icon={DollarSign}
                trend={18}
                color="bg-purple-100 text-purple-600"
              />
              <StatCard
                title="Conversion Rate"
                value={`${overviewData.conversion_rate?.toFixed(1) || 0}%`}
                icon={TrendingUp}
                trend={12}
                color="bg-orange-100 text-orange-600"
              />
            </div>

            {/* Today's Stats */}
            <div className="bg-white rounded-lg shadow p-6 mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Today's Activity</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-gray-600">Conversations</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">
                    {overviewData.today?.conversations || 0}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Applications</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">
                    {overviewData.today?.applications || 0}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Active Conversations</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">
                    {overviewData.active_conversations || 0}
                  </p>
                </div>
              </div>
            </div>

            {/* Conversion Funnel */}
            <ConversionFunnel />
          </>
        )}

        {activeView === 'applications' && (
          <ApplicationsList />
        )}

        {activeView === 'analytics' && (
          <Analytics />
        )}
      </main>
    </div>
  )
}

// Applications List Component
function ApplicationsList() {
  const { data, isLoading } = useQuery({
    queryKey: ['applications'],
    queryFn: () => adminAPI.getApplications({ limit: 50 }),
  })

  const applications = data?.data || []

  if (isLoading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b">
        <h2 className="text-xl font-semibold text-gray-900">Recent Applications</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Application #
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {applications.map((app) => (
              <tr key={app.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {app.application_number}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    {app.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ₹{app.loan_amount?.toLocaleString() || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(app.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-primary-600 hover:text-primary-900">
                  <button>View Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}


