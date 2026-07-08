export type Boleta = {
  id: number;
  empleadoId: number;
  periodo: string;
  sueldoBase: number;
  bonos: number;
  descuentos: number;
  sueldoNeto: number;
};
