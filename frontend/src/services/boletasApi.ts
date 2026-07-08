import { api } from './api';

export const boletasApi = {
  listar: () => api.get('/boletas'),
};
