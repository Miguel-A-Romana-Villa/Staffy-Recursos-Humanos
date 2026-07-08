import type { LoginRequest, LoginResponse } from '../types/auth.types';
import { api } from './api';

export const authApi = {
  login: (payload: LoginRequest) => api.post<LoginResponse>('/auth/login', payload),
};
