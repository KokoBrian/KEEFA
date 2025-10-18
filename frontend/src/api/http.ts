// src/api/http.ts
import axios, { type AxiosRequestHeaders } from 'axios';

// Function to safely get token from localStorage (only on client)
function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('authToken');
  }
  return null;
}

// Function to get CSRF token from cookie
function getCsrfToken(): string | null {
  if (typeof document === 'undefined') return null;
  const match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'));
  return match ? decodeURIComponent(match[2]) : null;
}

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // include cookies for CSRF and sessions
});

// Interceptor to add Authorization and CSRF headers if needed
http.interceptors.request.use(
  (config) => {
    const token = getToken();

    if (token) {
      if (!config.headers) {
        config.headers = {} as AxiosRequestHeaders;
      }

      // Add Authorization header
      if (typeof (config.headers as any).set === 'function') {
        (config.headers as any).set('Authorization', `Bearer ${token}`);
      } else {
        (config.headers as AxiosRequestHeaders)['Authorization'] = `Bearer ${token}`;
      }
    }

    // For unsafe HTTP methods, add CSRF token header
    const unsafeMethods = ['post', 'put', 'patch', 'delete'];
    if (config.method && unsafeMethods.includes(config.method.toLowerCase())) {
      const csrfToken = getCsrfToken();
      if (csrfToken) {
        if (!config.headers) {
          config.headers = {} as AxiosRequestHeaders;
        }
        if (typeof (config.headers as any).set === 'function') {
          (config.headers as any).set('X-CSRFToken', csrfToken);
        } else {
          (config.headers as AxiosRequestHeaders)['X-CSRFToken'] = csrfToken;
        }
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default http;
