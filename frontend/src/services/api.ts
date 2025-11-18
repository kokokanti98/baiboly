import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

/**
 * Base API client configuration for Baiboly application.
 * Handles all HTTP requests to the Flask backend with proper error handling.
 */

// Get API base URL from environment
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

/**
 * Request interceptor - Add any auth tokens or modify requests
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Add authentication token if available (future enhancement)
    // const token = localStorage.getItem('authToken');
    // if (token && config.headers) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor - Handle errors globally with Malagasy messages
 */
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Format error with Malagasy messages
    let errorMessage = 'Nisy olana'; // Default: "There was a problem"

    if (error.response) {
      // Server responded with error status
      switch (error.response.status) {
        case 400:
          errorMessage = 'Fangatahana tsy marina'; // Bad request
          break;
        case 401:
          errorMessage = 'Tsy manana alalana'; // Unauthorized
          break;
        case 403:
          errorMessage = 'Rarana'; // Forbidden
          break;
        case 404:
          errorMessage = 'Tsy hita'; // Not found
          break;
        case 500:
          errorMessage = 'Nisy olana tao amin\'ny mpizara'; // Server error
          break;
        case 503:
          errorMessage = 'Tsy afaka mividy ankehitriny'; // Service unavailable
          break;
        default:
          errorMessage = 'Nisy olana tamin\'ny fangatahana'; // Request error
      }
    } else if (error.request) {
      // Request made but no response received
      errorMessage = 'Mamariko ny fifandraisanao amin\'ny Internet'; // Check internet connection
    } else {
      // Something happened in setting up the request
      errorMessage = 'Nisy olana tamin\'ny fandefasana fangatahana'; // Error sending request
    }

    // Attach formatted error message
    const formattedError = {
      ...error,
      message: errorMessage,
      originalError: error.message,
    };

    return Promise.reject(formattedError);
  }
);

/**
 * API client interface for type-safe requests
 */
export const api = {
  /**
   * GET request
   */
  get: <T = any>(url: string, config = {}) => {
    return apiClient.get<T>(url, config);
  },

  /**
   * POST request
   */
  post: <T = any>(url: string, data?: any, config = {}) => {
    return apiClient.post<T>(url, data, config);
  },

  /**
   * PUT request
   */
  put: <T = any>(url: string, data?: any, config = {}) => {
    return apiClient.put<T>(url, data, config);
  },

  /**
   * PATCH request
   */
  patch: <T = any>(url: string, data?: any, config = {}) => {
    return apiClient.patch<T>(url, data, config);
  },

  /**
   * DELETE request
   */
  delete: <T = any>(url: string, config = {}) => {
    return apiClient.delete<T>(url, config);
  },
};

export default api;
