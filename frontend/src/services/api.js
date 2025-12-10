import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Chat API
export const chatAPI = {
  sendMessage: (data) => api.post('/api/chat/message', data),
  getHistory: (conversationId) => api.get(`/api/chat/history/${conversationId}`),
  getUserConversations: (userId) => api.get(`/api/chat/conversations/user/${userId}`),
}

// Documents API
export const documentsAPI = {
  upload: (formData) => api.post('/api/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  verify: (documentId) => api.post(`/api/documents/verify/${documentId}`),
  getApplicationDocuments: (applicationId) => 
    api.get(`/api/documents/application/${applicationId}`),
  delete: (documentId) => api.delete(`/api/documents/${documentId}`),
}

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/api/analytics/dashboard'),
  getConversionFunnel: (startDate, endDate) => 
    api.get('/api/analytics/conversion-funnel', {
      params: { start_date: startDate, end_date: endDate },
    }),
  getAgentPerformance: (startDate, endDate) =>
    api.get('/api/analytics/agent-performance', {
      params: { start_date: startDate, end_date: endDate },
    }),
  getTimeMetrics: (startDate, endDate) =>
    api.get('/api/analytics/time-metrics', {
      params: { start_date: startDate, end_date: endDate },
    }),
}

// Admin API
export const adminAPI = {
  getApplications: (params) => api.get('/api/admin/applications', { params }),
  getApplication: (applicationId) => 
    api.get(`/api/admin/applications/${applicationId}`),
  updateApplicationStatus: (applicationId, status, notes) =>
    api.put(`/api/admin/applications/${applicationId}/status`, { 
      new_status: status, 
      notes 
    }),
  getUsers: (params) => api.get('/api/admin/users', { params }),
  getConversations: (params) => api.get('/api/admin/conversations', { params }),
  getOverviewStats: () => api.get('/api/admin/stats/overview'),
}

export default api


