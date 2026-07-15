from abc import ABC, abstractmethod

from app.domain.concepto_pago import ConceptoPago
from app.domain.empleado import Empleado
from app.domain.exceptions import DatoInvalidoError


class EstrategiaSueldo(ABC):
    @abstractmethod
    def calcular(self, empleado: Empleado) -> float:
        raise NotImplementedError


class EstrategiaTiempoCompleto(EstrategiaSueldo):
    def calcular(self, empleado: Empleado) -> float:
        return empleado.calcular_sueldo_base()


class EstrategiaMedioTiempo(EstrategiaSueldo):
    def calcular(self, empleado: Empleado) -> float:
        return empleado.calcular_sueldo_base()


class CalculadoraSueldo:
    def calcular(
        self,
        empleado: Empleado,
        periodo: str,
        conceptos: list[ConceptoPago],
        bonos_extra: float = 0,
        descuentos_extra: float = 0,
    ) -> dict:
        periodo_limpio = periodo.strip()
        if not periodo_limpio:
            raise DatoInvalidoError("El periodo es obligatorio")
        if bonos_extra < 0 or descuentos_extra < 0:
            raise DatoInvalidoError("Bonos y descuentos deben ser mayores o iguales a cero")

        estrategia = self._obtener_estrategia(empleado)
        sueldo_base = estrategia.calcular(empleado)
        bonos = [item for item in conceptos if item.tipo == "BONO"]
        descuentos = [item for item in conceptos if item.tipo == "DESCUENTO"]
        total_bonos = sum(item.monto for item in bonos) + bonos_extra
        total_descuentos = sum(item.monto for item in descuentos) + descuentos_extra
        sueldo_neto = sueldo_base + total_bonos - total_descuentos

        return {
            "empleado_codigo": empleado.codigo,
            "empleado_nombre": empleado.nombre_completo,
            "dni": empleado.dni,
            "cargo": empleado.cargo,
            "periodo": periodo_limpio,
            "sueldo_base": sueldo_base,
            "bonos": total_bonos,
            "descuentos": total_descuentos,
            "sueldo_neto": sueldo_neto,
            "conceptos": conceptos,
        }

    def _obtener_estrategia(self, empleado: Empleado) -> EstrategiaSueldo:
        if empleado.tipo == "medio_tiempo":
            return EstrategiaMedioTiempo()
        return EstrategiaTiempoCompleto()
