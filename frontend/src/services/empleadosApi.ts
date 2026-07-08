import { api } from './api';

export const empleadosApi = {
  listar: () => api.get('/empleados'),
};
