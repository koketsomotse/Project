import { useEffect, useRef } from 'react'
import { useSession } from 'next-auth/react'
import useWebSocket, { ReadyState } from 'react-use-websocket'

export function useWebSocket() {
  const { data: session } = useSession()
  const didUnmount = useRef(false)

  // Replace with your WebSocket server URL
  const socketUrl = `ws://localhost:8000/ws/notifications/`
  
  const { lastMessage, readyState, sendMessage } = useWebSocket(socketUrl, {
    shouldReconnect: (closeEvent) => {
      return !didUnmount.current
    },
    reconnectAttempts: 10,
    reconnectInterval: 3000,
    // Add token to WebSocket connection
    protocols: session?.user?.token ? [session.user.token] : undefined,
  })

  useEffect(() => {
    return () => {
      didUnmount.current = true
    }
  }, [])

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState]

  return {
    lastMessage,
    connectionStatus,
    isConnected: readyState === ReadyState.OPEN,
    sendMessage,
  }
}
