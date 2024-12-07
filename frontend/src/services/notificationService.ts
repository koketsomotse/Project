import axios from 'axios';
import { getAuthToken } from './authService';

const API_URL = 'http://localhost:8000/api';

interface Notification {
  id: number;
  title: string;
  message: string;
  notification_type: string;
  read: boolean;
  created_at: string;
  updated_at: string;
}

interface NotificationPreferences {
  task_updated: boolean;
  task_assigned: boolean;
  task_completed: boolean;
}

/**
 * Notification Service
 * 
 * Provides methods for managing notifications:
 * - Fetching notifications
 * - Marking notifications as read
 * - Managing notification preferences
 */

/**
 * Sets up axios request interceptor with authentication
 */
axios.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * Fetches all notifications for the current user
 * 
 * @returns {Promise<Notification[]>} List of notifications
 * @throws {Error} If fetching notifications fails
 */
export const getNotifications = async (): Promise<Notification[]> => {
  try {
    const response = await axios.get<Notification[]>(
      `${API_URL}/notifications/`
    );
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch notifications');
  }
};

/**
 * Marks a specific notification as read
 * 
 * @param {number} id - ID of the notification to mark as read
 * @returns {Promise<void>}
 * @throws {Error} If marking notification as read fails
 */
export const markAsRead = async (id: number): Promise<void> => {
  try {
    await axios.post(`${API_URL}/notifications/${id}/mark_as_read/`);
  } catch (error) {
    throw new Error('Failed to mark notification as read');
  }
};

/**
 * Marks all notifications as read
 * 
 * @returns {Promise<void>}
 * @throws {Error} If marking notifications as read fails
 */
export const markAllAsRead = async (): Promise<void> => {
  try {
    await axios.post(`${API_URL}/notifications/mark_all_read/`);
  } catch (error) {
    throw new Error('Failed to mark all notifications as read');
  }
};

/**
 * Gets the current user's notification preferences
 * 
 * @returns {Promise<NotificationPreferences>} User's notification preferences
 * @throws {Error} If fetching preferences fails
 */
export const getNotificationPreferences = async (): Promise<NotificationPreferences> => {
  try {
    const response = await axios.get<NotificationPreferences>(
      `${API_URL}/preferences/`
    );
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch notification preferences');
  }
};

/**
 * Updates the user's notification preferences
 * 
 * @param {NotificationPreferences} preferences - New preference settings
 * @returns {Promise<NotificationPreferences>} Updated preferences
 * @throws {Error} If updating preferences fails
 */
export const updateNotificationPreferences = async (
  preferences: NotificationPreferences
): Promise<NotificationPreferences> => {
  try {
    const response = await axios.post<NotificationPreferences>(
      `${API_URL}/preferences/`,
      preferences
    );
    return response.data;
  } catch (error) {
    throw new Error('Failed to update notification preferences');
  }
};
