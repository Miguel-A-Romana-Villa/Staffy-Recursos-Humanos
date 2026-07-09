export type EstadoAsistencia = 'ASISTIO' | 'TARDE' | 'FALTO';

export type Asistencia = {
  id: number;
  empleado_id: number;
  fecha: string;
  estado: EstadoAsistencia;
  minutos_tardanza?: number;
  comentario?: string;
};

export type Periodo = {
  anio: number;
  mes: number;
  etiqueta: string;
};

export type ReglasAsistencia = {
  hora_ingreso: string;
  hora_salida: string;
  tardanzas_permitidas: number;
};
