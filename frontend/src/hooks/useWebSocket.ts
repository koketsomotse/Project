import { useEffect } from 'react';

const useWebSocket = (url: string) => {
  useEffect(() => {
    const socket = new WebSocket(url);

    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onmessage = (event) => {
      console.log('Message received:', event.data);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      socket.close();
    };
  }, [url]);
};

export default useWebSocket;
