// src/api/http.ts
import axios, { type AxiosRequestHeaders } from 'axios';

// Function to safely get token from localStorage (only on client)
function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('authToken');
  }
  return null;
}

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // include cookies if backend uses sessions
});

// Interceptor to add Authorization header if token exists
http.interceptors.request.use(
  (config) => {
    const token = getToken();

    if (token) {
      if (!config.headers) {
        config.headers = {} as AxiosRequestHeaders;
      }

      // Axios v1+ uses AxiosHeaders with .set method
      if (typeof (config.headers as any).set === 'function') {
        (config.headers as any).set('Authorization', `Bearer ${token}`);
      } else {
        // fallback for plain object headers
        (config.headers as AxiosRequestHeaders)['Authorization'] = `Bearer ${token}`;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default http;
