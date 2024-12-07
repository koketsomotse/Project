/**
 * Registration Page Component
 * 
 * Provides user registration functionality with form validation.
 * Handles new user registration and redirects to login upon success.
 */
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import Link from 'next/link';
import useWebSocket from '../../../hooks/useWebSocket';

const WEBSOCKET_URL = 'ws://localhost:8000/ws/notifications/';

/**
 * Register Page Component
 * 
 * Handles user registration with form validation and submission.
 */
export default function RegisterPage() {
  // State management for form data and loading state
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  useWebSocket(WEBSOCKET_URL);

  /**
   * Handles form submission
   * Validates form data and attempts to register new user
   */
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);
    const userData = {
      username: formData.get('username'),
      email: formData.get('email'),
      password: formData.get('password'),
    };

    try {
      // Attempt to register user
      // Replace with your Django backend URL
      await axios.post('http://localhost:8000/api/auth/register/', userData);
      
      // Redirect to login page on success
      router.push('/login');
    } catch (error: any) {
      setError(error.response?.data?.message || 'Registration failed');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
        </div>
        
        {/* Registration Form */}
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
          
          {/* Email Field */}
          <div>
            <label htmlFor="email" className="sr-only">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Email address"
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
              {loading ? 'Creating account...' : 'Register'}
            </button>
          </div>
          
          {/* Login Link */}
          <div className="text-sm text-center">
            <Link
              href="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Already have an account? Sign in
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
