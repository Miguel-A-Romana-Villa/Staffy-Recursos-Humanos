import type { ConceptoPago } from './concepto.types';

export type SueldoCalculoRequest = {
  empleado_codigo: string;
  periodo: string;
  bonos: number;
  descuentos: number;
};
export type SueldoCalculo = {
  empleado_codigo: string;
  empleado_nombre: string;
  dni: string;
  cargo: string;
  periodo: string;
  sueldo_base: number;
  bonos: number;
  descuentos: number;
  sueldo_neto: number;
  conceptos: Array<Pick<ConceptoPago, 'tipo' | 'concepto' | 'monto' | 'periodo'>>;
};
