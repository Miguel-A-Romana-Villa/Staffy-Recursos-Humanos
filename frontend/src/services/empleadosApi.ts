import { api } from './api';
import type { Empleado, EmpleadoPayload } from '../types/empleado.types';

export const empleadosApi = {
  listar: (search?: string) =>
    api.get<Empleado[]>('/empleados', { params: { search } }),
  listarActivos: (periodo: string) =>
    api.get<Empleado[]>('/empleados/activos', { params: { periodo } }),
  crear: (payload: EmpleadoPayload) =>
    api.post<Empleado>('/empleados', payload),
  actualizar: (id: number, payload: EmpleadoPayload) =>
    api.put<Empleado>(`/empleados/${id}`, payload),
};
