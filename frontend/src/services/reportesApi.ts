import { api } from './api';
import type {
  ReporteAsistenciaEmpleado,
  ReporteGeneral,
  ReportePagoPeriodo,
  ReporteResumen,
} from '../types/reporte.types';

export const reportesApi = {
  general: (periodo: string) =>
    api.get<ReporteGeneral>('/reportes/general', { params: { periodo } }),
  resumen: (periodo: string) =>
    api.get<ReporteResumen>('/reportes/resumen', { params: { periodo } }),
  pagos: (periodo: string) =>
    api.get<ReportePagoPeriodo[]>('/reportes/pagos', { params: { periodo } }),
  asistencias: (periodo: string) =>
    api.get<ReporteAsistenciaEmpleado[]>('/reportes/asistencias', {
      params: { periodo },
    }),
  descargarPdf: (periodo: string) =>
    api.get<Blob>('/reportes/pdf', {
      params: { periodo },
      responseType: 'blob',
    }),
};
