import React, { useEffect, useState } from 'react';
import { useWebSocketStore } from '../services/websocketService';

interface Notification {
    id: number;
    title: string;
    message: string;
    notification_type: string;
    created_at: string;
    is_read: boolean;
}

const NotificationComponent: React.FC = () => {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const { connect, disconnect, socket } = useWebSocketStore();

    useEffect(() => {
        // Connect to WebSocket when component mounts
        connect();

        // Fetch existing notifications
        fetchNotifications();

        return () => {
            // Disconnect when component unmounts
            disconnect();
        };
    }, []);

    useEffect(() => {
        if (socket) {
            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                setNotifications(prev => [data.message, ...prev]);
            };
        }
    }, [socket]);

    const fetchNotifications = async () => {
        try {
            const response = await fetch('/api/notifications');
            const data = await response.json();
            setNotifications(data);
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    };

    const markAsRead = async (id: number) => {
        try {
            await fetch(`/api/notifications/${id}/mark_read/`, {
                method: 'POST',
            });
            setNotifications(prev =>
                prev.map(notif =>
                    notif.id === id ? { ...notif, is_read: true } : notif
                )
            );
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    };

    return (
        <div className="max-w-md mx-auto p-4">
            <h2 className="text-2xl font-bold mb-4">Notifications</h2>
            <div className="space-y-4">
                {notifications.map((notification) => (
                    <div
                        key={notification.id}
                        className={`p-4 rounded-lg shadow ${
                            notification.is_read ? 'bg-gray-100' : 'bg-white border-l-4 border-blue-500'
                        }`}
                    >
                        <div className="flex justify-between items-start">
                            <h3 className="font-semibold">{notification.title}</h3>
                            {!notification.is_read && (
                                <button
                                    onClick={() => markAsRead(notification.id)}
                                    className="text-sm text-blue-500 hover:text-blue-700"
                                >
                                    Mark as read
                                </button>
                            )}
                        </div>
                        <p className="text-gray-600 mt-1">{notification.message}</p>
                        <div className="mt-2 text-sm text-gray-500">
                            {new Date(notification.created_at).toLocaleString()}
                        </div>
                    </div>
                ))}
                {notifications.length === 0 && (
                    <p className="text-gray-500 text-center">No notifications</p>
                )}
            </div>
        </div>
    );
};

export default NotificationComponent;
