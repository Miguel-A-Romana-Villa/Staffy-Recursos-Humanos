export type EstadoAsistencia = 'ASISTIO' | 'TARDE' | 'FALTO';

export type Asistencia = {
  id: number;
  empleadoId: number;
  fecha: string;
  estado: EstadoAsistencia;
};
