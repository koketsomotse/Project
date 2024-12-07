import { create } from 'zustand';

interface WebSocketStore {
    socket: WebSocket | null;
    connect: () => void;
    disconnect: () => void;
    isConnected: boolean;
}

const WEBSOCKET_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws/notifications/';

export const useWebSocketStore = create<WebSocketStore>((set) => ({
    socket: null,
    isConnected: false,
    connect: () => {
        const socket = new WebSocket(WEBSOCKET_URL);

        socket.onopen = () => {
            console.log('WebSocket Connected');
            set({ isConnected: true });
        };

        socket.onclose = () => {
            console.log('WebSocket Disconnected');
            set({ isConnected: false });
        };

        socket.onerror = (error) => {
            console.error('WebSocket Error:', error);
        };

        set({ socket });
    },
    disconnect: () => {
        const { socket } = useWebSocketStore.getState();
        if (socket) {
            socket.close();
            set({ socket: null, isConnected: false });
        }
    },
}));
