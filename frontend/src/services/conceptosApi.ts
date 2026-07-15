import { api } from './api';
import type { ConceptoPago, ConceptoPagoCreate } from '../types/concepto.types';

export const conceptosApi = {
  listar: (params?: { empleado_id?: number; periodo?: string }) => api.get<ConceptoPago[]>('/conceptos', { params }),
  registrar: (payload: ConceptoPagoCreate) => api.post<ConceptoPago>('/conceptos', payload),
};
