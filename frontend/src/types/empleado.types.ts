export type Empleado = {
  id: number;
  codigo: string;
  dni: string;
  correo?: string;
  telefono?: string;
  nombres: string;
  apellidos: string;
  cargo: string;
  sueldo_base: number;
  tipo: TipoEmpleado;
  horas_trabajadas?: number;
  tarifa_por_hora?: number;
  hijos: number;
  fecha_nacimiento?: string;
  fecha_inicio?: string;
  fecha_cese?: string;
  regimen_pensionario: RegimenPensionario;
  foto_url?: string;
  activo: boolean;
};

export type RegimenPensionario = 'ONP' | 'AFP' | 'SIN_REGIMEN';
export type TipoEmpleado = 'tiempo_completo' | 'medio_tiempo';

export type EmpleadoForm = {
  codigo: string;
  dni: string;
  correo: string;
  telefono: string;
  nombres: string;
  apellidos: string;
  cargo: string;
  sueldo_base: number;
  tipo: TipoEmpleado;
  horas_trabajadas?: number;
  tarifa_por_hora?: number;
  hijos: number;
  fecha_nacimiento: string;
  fecha_inicio: string;
  fecha_cese: string;
  regimen_pensionario: RegimenPensionario;
  foto_url: string;
  activo: boolean;
};

export type EmpleadoPayload = Omit<
  EmpleadoForm,
  | 'correo'
  | 'telefono'
  | 'horas_trabajadas'
  | 'tarifa_por_hora'
  | 'fecha_nacimiento'
  | 'fecha_inicio'
  | 'fecha_cese'
  | 'foto_url'
> & {
  correo?: string | null;
  telefono?: string | null;
  horas_trabajadas?: number | null;
  tarifa_por_hora?: number | null;
  fecha_nacimiento?: string | null;
  fecha_inicio?: string | null;
  fecha_cese?: string | null;
  foto_url?: string | null;
};
