import React, { useState, useEffect } from 'react'
import { MessageCircle, FileText, TrendingUp, Shield } from 'lucide-react'
import ChatInterface from '../components/ChatInterface'
import DocumentUpload from '../components/DocumentUpload'
import ApplicationDashboard from '../components/ApplicationDashboard'

export default function Home() {
  const [userId] = useState(() => {
    // Get or create user ID
    let id = localStorage.getItem('userId')
    if (!id) {
      id = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      localStorage.setItem('userId', id)
    }
    return id
  })

  const [activeTab, setActiveTab] = useState('chat')
  const [applicationId] = useState(() => {
    return `app_${Date.now()}`
  })

  const tabs = [
    { id: 'chat', label: 'Chat', icon: MessageCircle },
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">LoaniFi</h1>
              <p className="text-gray-600">AI-Powered Personal Loan Assistant</p>
            </div>
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-green-600" />
              <span className="text-sm text-gray-600">Secure & Encrypted</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Features Banner */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-100 p-3 rounded-lg">
                <MessageCircle className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">AI Assistance</h3>
                <p className="text-sm text-gray-600">24/7 intelligent support</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-green-100 p-3 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Fast Approval</h3>
                <p className="text-sm text-gray-600">Minutes, not days</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-purple-100 p-3 rounded-lg">
                <Shield className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">100% Secure</h3>
                <p className="text-sm text-gray-600">Bank-grade encryption</p>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow mb-4">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                      activeTab === tab.id
                        ? 'border-primary-600 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            {activeTab === 'chat' && (
              <div className="h-[600px]">
                <ChatInterface userId={userId} />
              </div>
            )}

            {activeTab === 'documents' && (
              <DocumentUpload 
                userId={userId} 
                applicationId={applicationId}
                onUploadSuccess={() => {
                  console.log('Document uploaded successfully')
                }}
              />
            )}

            {activeTab === 'dashboard' && (
              <ApplicationDashboard 
                application={{
                  application_number: 'APP12345678',
                  status: 'under_verification',
                  requested_amount: 500000,
                  tenure_months: 36,
                  credit_score: 750,
                  created_at: new Date().toISOString(),
                }}
              />
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Your Application</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Status</span>
                  <span className="text-sm font-medium text-blue-600">In Progress</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Documents</span>
                  <span className="text-sm font-medium text-gray-900">0/6</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Completion</span>
                  <span className="text-sm font-medium text-gray-900">15%</span>
                </div>
              </div>
            </div>

            {/* Help Card */}
            <div className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg shadow p-6 text-white">
              <h3 className="font-semibold mb-2">Need Help?</h3>
              <p className="text-sm text-primary-100 mb-4">
                Our AI assistant is here to guide you through every step of the process.
              </p>
              <button 
                onClick={() => setActiveTab('chat')}
                className="bg-white text-primary-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-50 transition-colors"
              >
                Start Chat
              </button>
            </div>

            {/* Features List */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Why Choose Us?</h3>
              <ul className="space-y-3">
                <li className="flex items-start space-x-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <span className="text-sm text-gray-600">Instant eligibility check</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <span className="text-sm text-gray-600">Competitive interest rates</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <span className="text-sm text-gray-600">Flexible repayment options</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <span className="text-sm text-gray-600">No hidden charges</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            © 2024 LoaniFi. All rights reserved. | Powered by AI
          </p>
        </div>
      </footer>
    </div>
  )
}


