import { useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';

interface WebSocketHookOptions {
  onMessage?: (data: any) => void;
  onError?: (error: Event) => void;
  onClose?: (event: CloseEvent) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
}

/**
 * Custom hook for managing WebSocket connections
 * 
 * Features:
 * - Automatic connection management
 * - Reconnection attempts on disconnection
 * - Message handling
 * - Connection status tracking
 * - Cleanup on unmount
 * 
 * @param {string} url - WebSocket server URL
 * @param {WebSocketHookOptions} options - Configuration options
 * @returns {Object} WebSocket control methods
 */
export const useWebSocket = (
  url: string,
  {
    onMessage,
    onError,
    onClose,
    reconnectAttempts = 5,
    reconnectInterval = 5000
  }: WebSocketHookOptions = {}
) => {
  const ws = useRef<WebSocket | null>(null);
  const reconnectCount = useRef(0);
  const router = useRouter();

  /**
   * Creates a new WebSocket connection
   * Configures event listeners and error handling
   */
  const connect = useCallback(() => {
    try {
      // Get authentication token
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No authentication token found');
        router.push('/login');
        return;
      }

      // Create WebSocket connection with auth token
      ws.current = new WebSocket(`${url}?token=${token}`);

      // Connection opened
      ws.current.onopen = () => {
        console.log('WebSocket Connected');
        reconnectCount.current = 0;
      };

      // Listen for messages
      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        onMessage?.(data);
      };

      // Handle errors
      ws.current.onerror = (error) => {
        console.error('WebSocket Error:', error);
        onError?.(error);
      };

      // Handle connection closing
      ws.current.onclose = (event) => {
        console.log('WebSocket Disconnected');
        onClose?.(event);

        // Attempt reconnection if not at limit
        if (reconnectCount.current < reconnectAttempts) {
          reconnectCount.current += 1;
          setTimeout(connect, reconnectInterval);
        } else {
          console.error('Max reconnection attempts reached');
          router.push('/login');
        }
      };
    } catch (error) {
      console.error('WebSocket Connection Error:', error);
    }
  }, [url, onMessage, onError, onClose, reconnectAttempts, reconnectInterval, router]);

  /**
   * Sends a message through the WebSocket connection
   * 
   * @param {any} data - Data to send (will be JSON stringified)
   * @returns {boolean} Success status of send operation
   */
  const sendMessage = useCallback((data: any): boolean => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data));
      return true;
    }
    return false;
  }, []);

  /**
   * Manually closes the WebSocket connection
   */
  const disconnect = useCallback(() => {
    if (ws.current) {
      ws.current.close();
      ws.current = null;
    }
  }, []);

  // Set up connection on mount and clean up on unmount
  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    sendMessage,
    disconnect,
    connect,
    isConnected: ws.current?.readyState === WebSocket.OPEN
  };
};

export default useWebSocket;
