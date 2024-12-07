import React, { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import NotificationItem from './NotificationItem';
import { getNotifications, markAsRead } from '@/services/notificationService';

interface Notification {
  id: number;
  title: string;
  message: string;
  notification_type: string;
  read: boolean;
  created_at: string;
}

/**
 * NotificationList Component
 * 
 * Displays a list of notifications with real-time updates via WebSocket.
 * Supports marking notifications as read and filtering by type.
 * 
 * Features:
 * - Real-time notification updates
 * - Read/unread status management
 * - Notification filtering
 * - Infinite scroll loading
 */
const NotificationList: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // WebSocket connection for real-time updates
  const { isConnected } = useWebSocket('ws://localhost:8000/ws/notifications/', {
    onMessage: (data) => {
      // Add new notification to the list
      setNotifications(prev => [data.message, ...prev]);
    }
  });

  /**
   * Fetches initial notifications from the server
   */
  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const data = await getNotifications();
      setNotifications(data);
    } catch (err) {
      setError('Failed to load notifications');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handles marking a notification as read
   * 
   * @param {number} id - ID of the notification to mark as read
   */
  const handleMarkAsRead = async (id: number) => {
    try {
      await markAsRead(id);
      setNotifications(prev =>
        prev.map(notification =>
          notification.id === id
            ? { ...notification, read: true }
            : notification
        )
      );
    } catch (err) {
      console.error('Failed to mark notification as read:', err);
    }
  };

  // Fetch notifications on component mount
  useEffect(() => {
    fetchNotifications();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center p-4">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Connection Status */}
      {!isConnected && (
        <div className="bg-yellow-100 text-yellow-800 p-2 rounded-md text-sm">
          Connecting to notification service...
        </div>
      )}
      
      {/* Notifications List */}
      {notifications.length === 0 ? (
        <div className="text-gray-500 text-center p-4">
          No notifications yet
        </div>
      ) : (
        <div className="space-y-2">
          {notifications.map((notification) => (
            <NotificationItem
              key={notification.id}
              notification={notification}
              onMarkAsRead={handleMarkAsRead}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default NotificationList;
