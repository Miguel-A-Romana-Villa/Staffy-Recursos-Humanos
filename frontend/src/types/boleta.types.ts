export type Boleta = {
  id: number;
  empleado_codigo: string;
  empleado_nombre: string;
  dni: string;
  cargo: string;
  periodo: string;
  sueldo_base: number;
  bonos: number;
  descuentos: number;
  sueldo_neto: number;
};

export type BoletaCreate = {
  empleado_codigo: string;
  periodo: string;
  bonos: number;
  descuentos: number;
};
