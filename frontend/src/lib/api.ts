import axios from 'axios'
import { getSession } from 'next-auth/react'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

// Add auth token to requests
api.interceptors.request.use(async (config) => {
  const session = await getSession()
  if (session?.user?.token) {
    config.headers.Authorization = `Bearer ${session.user.token}`
  }
  return config
})

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401) {
      // Redirect to login or refresh token
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const notifications = {
  getAll: () => api.get('/api/notifications/'),
  markAsRead: (id: string) => api.post(`/api/notifications/${id}/read/`),
  delete: (id: string) => api.delete(`/api/notifications/${id}/`),
  markAllAsRead: () => api.post('/api/notifications/mark-all-read/'),
}

export const preferences = {
  getAll: () => api.get('/api/preferences/'),
  update: (id: string, data: any) => api.patch(`/api/preferences/${id}/`, data),
}

export default api
