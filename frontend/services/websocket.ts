class NotificationWebSocket {
    private socket: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;

    connect() {
        const token = localStorage.getItem('token');
        if (!token) return;

        this.socket = new WebSocket(`ws://localhost:8000/ws/notifications/?token=${token}`);

        this.socket.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
        };

        this.socket.onmessage = (event) => {
            const notification = JSON.parse(event.data);
            this.handleNotification(notification);
        };

        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            this.reconnect();
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            // Additional logging for debugging
            if (error instanceof ErrorEvent) {
                console.error('Error message:', error.message);
            } else {
                console.error('Error details:', error);
            }
        };
    }

    private reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => {
                this.connect();
            }, 1000 * this.reconnectAttempts);
        }
    }

    private handleNotification(notification: any) {
        // Implement notification handling
        console.log('New notification:', notification);
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
}

export const notificationWS = new NotificationWebSocket(); 