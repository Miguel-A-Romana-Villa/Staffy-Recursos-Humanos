import { api } from './api';
import type { Boleta, BoletaCreate } from '../types/boleta.types';

export const boletasApi = {
  listar: () => api.get<Boleta[]>('/boletas'),
  generar: (payload: BoletaCreate) => api.post<Boleta>('/boletas/generar', payload),
};
