import React from 'react';
import { formatDistanceToNow } from 'date-fns';

interface NotificationProps {
  notification: {
    id: number;
    title: string;
    message: string;
    notification_type: string;
    read: boolean;
    created_at: string;
  };
  onMarkAsRead: (id: number) => void;
}

/**
 * NotificationItem Component
 * 
 * Displays a single notification with its details and actions.
 * 
 * Features:
 * - Read/unread status indication
 * - Notification type badge
 * - Relative timestamp
 * - Mark as read action
 * 
 * @param {NotificationProps} props - Component props
 */
const NotificationItem: React.FC<NotificationProps> = ({ notification, onMarkAsRead }) => {
  /**
   * Gets the appropriate background color based on notification type
   */
  const getTypeBadgeColor = (type: string): string => {
    switch (type) {
      case 'TASK_UPDATED':
        return 'bg-blue-100 text-blue-800';
      case 'TASK_ASSIGNED':
        return 'bg-green-100 text-green-800';
      case 'TASK_COMPLETED':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  /**
   * Formats the notification type for display
   */
  const formatType = (type: string): string => {
    return type.split('_').map(word => 
      word.charAt(0) + word.slice(1).toLowerCase()
    ).join(' ');
  };

  return (
    <div
      className={`
        p-4 rounded-lg shadow-sm border
        ${notification.read ? 'bg-white' : 'bg-blue-50'}
        transition-colors duration-200
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {/* Notification Header */}
          <div className="flex items-center space-x-2 mb-1">
            <span
              className={`
                px-2 py-1 rounded-full text-xs font-medium
                ${getTypeBadgeColor(notification.notification_type)}
              `}
            >
              {formatType(notification.notification_type)}
            </span>
            <span className="text-gray-500 text-sm">
              {formatDistanceToNow(new Date(notification.created_at), { addSuffix: true })}
            </span>
          </div>

          {/* Notification Content */}
          <h3 className="font-medium text-gray-900 mb-1">
            {notification.title}
          </h3>
          <p className="text-gray-600 text-sm">
            {notification.message}
          </p>
        </div>

        {/* Actions */}
        {!notification.read && (
          <button
            onClick={() => onMarkAsRead(notification.id)}
            className="ml-4 text-sm text-gray-500 hover:text-gray-700"
          >
            Mark as read
          </button>
        )}
      </div>
    </div>
  );
};

export default NotificationItem;
