import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: `${API_URL}/api`,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for adding auth token
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const notificationApi = {
    getNotifications: () => api.get('/notifications/'),
    markAsRead: (id: number) => api.post(`/notifications/${id}/mark_read/`),
    getPreferences: () => api.get('/preferences/'),
    updatePreferences: (preferences: any) => api.post('/preferences/', preferences),
};

export default api; 