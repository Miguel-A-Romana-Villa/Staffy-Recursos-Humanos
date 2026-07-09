import { api } from './api';
import type { Asistencia } from '../types/asistencia.types';

export const asistenciaApi = {
  listar: (params?: { empleado_id?: number; periodo?: string }) => api.get<Asistencia[]>('/asistencia', { params }),
  registrar: (payload: Omit<Asistencia, 'id'>) => api.post<Asistencia>('/asistencia', payload),
  eliminar: (params: { empleado_id: number; fecha: string }) => api.delete('/asistencia', { params }),
};
