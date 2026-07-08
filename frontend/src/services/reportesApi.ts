import { api } from './api';

export const reportesApi = {
  listar: () => api.get('/reportes'),
};
