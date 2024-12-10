import { useEffect, useState } from 'react';
import { notificationApi } from '../services/api';
import { notificationWS } from '../services/websocket';

interface Notification {
    id: number;
    title: string;
    message: string;
    read: boolean;
    created_at: string;
}

export default function Home() {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Connect to WebSocket
        notificationWS.connect();

        // Load initial notifications
        loadNotifications();

        return () => {
            notificationWS.disconnect();
        };
    }, []);

    const loadNotifications = async () => {
        try {
            const response = await notificationApi.getNotifications();
            setNotifications(response.data);
        } catch (error) {
            console.error('Error loading notifications:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-2xl font-bold mb-4">Notifications</h1>
            <div className="space-y-4">
                {notifications.map((notification) => (
                    <div 
                        key={notification.id}
                        className={`p-4 rounded-lg shadow ${notification.read ? 'bg-gray-50' : 'bg-white border-l-4 border-blue-500'}`}
                    >
                        <h2 className="font-semibold">{notification.title}</h2>
                        <p className="text-gray-600">{notification.message}</p>
                        <span className="text-sm text-gray-500">
                            {new Date(notification.created_at).toLocaleDateString()}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
} 