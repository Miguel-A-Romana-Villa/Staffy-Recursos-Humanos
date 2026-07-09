export type ReporteResumen = {
  total_empleados: number;
  total_pagos: number;
  total_tardanzas: number;
  total_faltas: number;
};

export type ReportePagoPeriodo = {
  periodo: string;
  cantidad_boletas: number;
  total_pagado: number;
};

export type ReporteAsistenciaEmpleado = {
  empleado_codigo: string;
  empleado_nombre: string;
  asistio: number;
  tarde: number;
  falto: number;
};
