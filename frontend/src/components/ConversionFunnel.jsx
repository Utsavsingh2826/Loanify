import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { analyticsAPI } from '../services/api'
import { TrendingDown } from 'lucide-react'

export default function ConversionFunnel() {
  const { data, isLoading } = useQuery({
    queryKey: ['conversion-funnel'],
    queryFn: () => analyticsAPI.getConversionFunnel(),
  })

  const funnel = data?.data || {}

  const stages = [
    { 
      key: 'total_conversations', 
      label: 'Total Conversations',
      value: funnel.total_conversations || 0,
      color: 'bg-blue-500'
    },
    { 
      key: 'qualified_leads', 
      label: 'Qualified Leads',
      value: funnel.qualified_leads || 0,
      rate: funnel.conversion_rates?.qualification_rate,
      color: 'bg-green-500'
    },
    { 
      key: 'documents_submitted', 
      label: 'Documents Submitted',
      value: funnel.documents_submitted || 0,
      rate: funnel.conversion_rates?.document_submission_rate,
      color: 'bg-purple-500'
    },
    { 
      key: 'applications_submitted', 
      label: 'Applications Submitted',
      value: funnel.applications_submitted || 0,
      color: 'bg-orange-500'
    },
    { 
      key: 'approved', 
      label: 'Approved',
      value: funnel.approved || 0,
      rate: funnel.conversion_rates?.approval_rate,
      color: 'bg-indigo-500'
    },
    { 
      key: 'sanctioned', 
      label: 'Sanctioned',
      value: funnel.sanctioned || 0,
      rate: funnel.conversion_rates?.overall_conversion,
      color: 'bg-green-600'
    },
  ]

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Conversion Funnel</h2>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <span>Overall Conversion:</span>
          <span className="font-semibold text-green-600">
            {funnel.conversion_rates?.overall_conversion?.toFixed(1) || 0}%
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {stages.map((stage, index) => {
          const maxValue = stages[0].value || 1
          const widthPercent = (stage.value / maxValue) * 100
          
          return (
            <div key={stage.key} className="relative">
              {/* Funnel Bar */}
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">{stage.label}</span>
                    <span className="text-sm font-semibold text-gray-900">{stage.value}</span>
                  </div>
                  <div className="relative">
                    <div className="h-12 bg-gray-100 rounded-lg overflow-hidden">
                      <div
                        className={`h-full ${stage.color} transition-all duration-500 flex items-center justify-end px-4`}
                        style={{ width: `${widthPercent}%` }}
                      >
                        {stage.rate && (
                          <span className="text-white text-xs font-medium">
                            {stage.rate.toFixed(1)}%
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Drop-off Indicator */}
              {index < stages.length - 1 && stages[index + 1].value < stage.value && (
                <div className="flex items-center justify-center mt-2 text-xs text-red-600">
                  <TrendingDown className="w-4 h-4 mr-1" />
                  <span>
                    {((stage.value - stages[index + 1].value) / stage.value * 100).toFixed(1)}% drop-off
                  </span>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}


