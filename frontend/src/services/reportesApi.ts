import { api } from './api';
import type {
  ReporteAsistenciaEmpleado,
  ReportePagoPeriodo,
  ReporteResumen,
} from '../types/reporte.types';

export const reportesApi = {
  resumen: () => api.get<ReporteResumen>('/reportes/resumen'),
  pagos: () => api.get<ReportePagoPeriodo[]>('/reportes/pagos'),
  asistencias: () => api.get<ReporteAsistenciaEmpleado[]>('/reportes/asistencias'),
};
