import axios from 'axios';

const httpAdmin = axios.create({
  baseURL: process.env.ADMIN_API_BASE_URL || 'http://localhost:8000/api/v1/',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.ADMIN_TOKEN}`, // ADMIN_TOKEN set in your .env file or server environment securely
  },
  withCredentials: true,
});

export default httpAdmin;
