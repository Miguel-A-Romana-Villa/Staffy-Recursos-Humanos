import { api } from './api';
import type { SueldoCalculo, SueldoCalculoRequest } from '../types/sueldo.types';

export const sueldosApi = {
  calcular: (payload: SueldoCalculoRequest) => api.post<SueldoCalculo>('/sueldos/calcular', payload),
};
