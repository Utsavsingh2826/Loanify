import React from 'react'
import { CheckCircle, Clock, FileText, AlertCircle } from 'lucide-react'

const STATUS_CONFIG = {
  initiated: { color: 'bg-gray-100 text-gray-800', icon: Clock, label: 'Initiated' },
  documents_pending: { color: 'bg-yellow-100 text-yellow-800', icon: FileText, label: 'Documents Pending' },
  documents_submitted: { color: 'bg-blue-100 text-blue-800', icon: FileText, label: 'Documents Submitted' },
  under_verification: { color: 'bg-purple-100 text-purple-800', icon: Clock, label: 'Under Verification' },
  under_review: { color: 'bg-indigo-100 text-indigo-800', icon: Clock, label: 'Under Review' },
  approved: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Approved' },
  rejected: { color: 'bg-red-100 text-red-800', icon: AlertCircle, label: 'Rejected' },
  sanctioned: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Sanctioned' },
}

export default function ApplicationDashboard({ application }) {
  if (!application) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-500">No application data available</p>
      </div>
    )
  }

  const status = STATUS_CONFIG[application.status] || STATUS_CONFIG.initiated
  const Icon = status.icon

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Header */}
      <div className="bg-primary-600 text-white p-6 rounded-t-lg">
        <h2 className="text-2xl font-bold">Application Dashboard</h2>
        <p className="text-primary-100 mt-1">
          Application #{application.application_number}
        </p>
      </div>

      {/* Status */}
      <div className="p-6 border-b">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Current Status</p>
            <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full mt-1 ${status.color}`}>
              <Icon className="w-5 h-5" />
              <span className="font-medium">{status.label}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Loan Details */}
      <div className="p-6 grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-600">Requested Amount</p>
          <p className="text-xl font-semibold text-gray-900">
            ₹{application.requested_amount?.toLocaleString() || '-'}
          </p>
        </div>
        
        {application.approved_amount && (
          <div>
            <p className="text-sm text-gray-600">Approved Amount</p>
            <p className="text-xl font-semibold text-green-600">
              ₹{application.approved_amount.toLocaleString()}
            </p>
          </div>
        )}

        {application.interest_rate && (
          <div>
            <p className="text-sm text-gray-600">Interest Rate</p>
            <p className="text-xl font-semibold text-gray-900">
              {application.interest_rate}% p.a.
            </p>
          </div>
        )}

        {application.tenure_months && (
          <div>
            <p className="text-sm text-gray-600">Tenure</p>
            <p className="text-xl font-semibold text-gray-900">
              {application.tenure_months} months
            </p>
          </div>
        )}

        {application.credit_score && (
          <div>
            <p className="text-sm text-gray-600">Credit Score</p>
            <p className="text-xl font-semibold text-gray-900">
              {application.credit_score}
            </p>
          </div>
        )}
      </div>

      {/* Timeline */}
      <div className="p-6 bg-gray-50 rounded-b-lg">
        <h3 className="font-semibold text-gray-900 mb-4">Application Timeline</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
              <CheckCircle className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">Application Initiated</p>
              <p className="text-xs text-gray-500">
                {new Date(application.created_at).toLocaleString()}
              </p>
            </div>
          </div>

          {application.submitted_at && (
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Documents Submitted</p>
                <p className="text-xs text-gray-500">
                  {new Date(application.submitted_at).toLocaleString()}
                </p>
              </div>
            </div>
          )}

          {application.approved_at && (
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Loan Approved</p>
                <p className="text-xs text-gray-500">
                  {new Date(application.approved_at).toLocaleString()}
                </p>
              </div>
            </div>
          )}

          {application.sanctioned_at && (
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Sanction Letter Generated</p>
                <p className="text-xs text-gray-500">
                  {new Date(application.sanctioned_at).toLocaleString()}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}


