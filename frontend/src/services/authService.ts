import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

interface LoginData {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

interface AuthResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
  };
}

/**
 * Authentication Service
 * 
 * Provides methods for user authentication operations:
 * - Login
 * - Registration
 * - Token management
 */

/**
 * Attempts to log in a user
 * 
 * @param {LoginData} data - User login credentials
 * @returns {Promise<AuthResponse>} Authentication response with token
 * @throws {Error} If login fails
 */
export const loginUser = async (data: LoginData): Promise<AuthResponse> => {
  try {
    const response = await axios.post<AuthResponse>(
      `${API_URL}/auth/login/`,
      data
    );
    
    // Store authentication token
    localStorage.setItem('token', response.data.token);
    
    return response.data;
  } catch (error) {
    throw new Error('Login failed');
  }
};

/**
 * Registers a new user
 * 
 * @param {RegisterData} data - User registration data
 * @returns {Promise<AuthResponse>} Authentication response
 * @throws {Error} If registration fails
 */
export const registerUser = async (data: RegisterData): Promise<AuthResponse> => {
  try {
    const response = await axios.post<AuthResponse>(
      `${API_URL}/auth/register/`,
      data
    );
    return response.data;
  } catch (error) {
    throw new Error('Registration failed');
  }
};

/**
 * Logs out the current user
 * Removes authentication token and other user data
 */
export const logoutUser = (): void => {
  localStorage.removeItem('token');
};

/**
 * Gets the current authentication token
 * 
 * @returns {string | null} Authentication token if exists
 */
export const getAuthToken = (): string | null => {
  return localStorage.getItem('token');
};

/**
 * Checks if a user is currently authenticated
 * 
 * @returns {boolean} True if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  return !!token;
};

/**
 * Configures axios with authentication headers
 * 
 * @param {string} token - Authentication token
 */
export const setAuthHeader = (token: string): void => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};
