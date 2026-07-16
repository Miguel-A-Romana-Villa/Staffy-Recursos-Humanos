import axios from 'axios';
import { limpiarSesion, obtenerToken } from './authSession';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
});

api.interceptors.request.use((config) => {
  const token = obtenerToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      limpiarSesion();
      if (window.location.pathname !== '/login')
        window.location.assign('/login');
    }
    return Promise.reject(error);
  },
);
