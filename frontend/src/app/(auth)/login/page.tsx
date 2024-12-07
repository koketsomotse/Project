/**
 * Login Page Component
 * 
 * Provides user authentication functionality with a form interface.
 * Handles login submission, error states, and redirects after successful login.
 * Also initializes WebSocket connection upon successful authentication.
 */
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { signIn } from 'next-auth/react'
import { useWebSocket } from '../../../hooks/useWebSocket';
const WEBSOCKET_URL = 'ws://localhost:8000/ws/notifications/';

/**
 * Login Page Component
 * 
 * Provides user authentication functionality with a form interface.
 * Handles login submission, error states, and redirects after successful login.
 * Also initializes WebSocket connection upon successful authentication.
 */
export default function LoginPage() {
  // State management for error and loading states
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const router = useRouter()
  useWebSocket(WEBSOCKET_URL);

  /**
   * Handles form submission
   * Attempts to authenticate user and establish WebSocket connection
   */
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const formData = new FormData(e.currentTarget)
    const response = await signIn('credentials', {
      username: formData.get('username'),
      password: formData.get('password'),
      redirect: false,
    })

    if (response?.error) {
      setError('Invalid credentials')
      setLoading(false)
    } else {
      router.push('/dashboard')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        
        {/* Login Form */}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="text-red-500 text-sm text-center">
              {error}
            </div>
          )}
          
          {/* Username Field */}
          <div>
            <label htmlFor="username" className="sr-only">
              Username
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Username"
            />
          </div>
          
          {/* Password Field */}
          <div>
            <label htmlFor="password" className="sr-only">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              disabled={loading}
              className="bg-black text-white py-2 px-4 rounded"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
