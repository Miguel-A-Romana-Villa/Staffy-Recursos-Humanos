from app.domain.boleta import Boleta
from app.domain.concepto_pago import ConceptoPago
from app.domain.empleado import Empleado


class CalculadoraSueldo:
    def calcular(
        self,
        empleado: Empleado,
        periodo: str,
        conceptos: list[ConceptoPago],
        bonos_extra: float = 0,
        descuentos_extra: float = 0,
    ) -> Boleta:
        return Boleta.generar(
            empleado=empleado,
            periodo=periodo,
            conceptos=conceptos,
            bonos_extra=bonos_extra,
            descuentos_extra=descuentos_extra,
        )
