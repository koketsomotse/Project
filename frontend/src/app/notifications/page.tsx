import React, { useEffect, useState } from 'react';
import axios from 'axios';
import useWebSocket from '../hooks/useWebSocket';

const NotificationManagement = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Establish WebSocket connection
    const { lastMessage } = useWebSocket('ws://localhost:8000/ws/notifications/');

    useEffect(() => {
        const fetchNotifications = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/notifications/');
                setNotifications(response.data);
            } catch (err) {
                setError('Failed to fetch notifications');
            } finally {
                setLoading(false);
            }
        };

        fetchNotifications();
    }, []);

    // Handle incoming WebSocket messages
    useEffect(() => {
        if (lastMessage !== null) {
            const newNotification = JSON.parse(lastMessage.data);
            setNotifications((prevNotifications) => [newNotification, ...prevNotifications]);
        }
    }, [lastMessage]);

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:8000/api/notifications/${id}/`);
            setNotifications(notifications.filter(notification => notification.id !== id));
        } catch (err) {
            setError('Failed to delete notification');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>Notification Management</h1>
            <ul>
                {notifications.map(notification => (
                    <li key={notification.id}>
                        {notification.message}
                        <button onClick={() => handleDelete(notification.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default NotificationManagement;
