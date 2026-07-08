import { api } from './api';

export const asistenciaApi = {
  listar: () => api.get('/asistencia'),
};
