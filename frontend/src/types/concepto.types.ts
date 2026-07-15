export type TipoConcepto = 'BONO' | 'DESCUENTO';

export type ConceptoPago = {
  id: number;
  empleado_id: number;
  tipo: TipoConcepto;
  concepto: string;
  monto: number;
  periodo: string;
};

export type ConceptoPagoCreate = Omit<ConceptoPago, 'id'>;
