from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.empleado import Empleado


class EstrategiaSueldo(ABC):
    @abstractmethod
    def calcular(self, empleado: "Empleado") -> float:
        raise NotImplementedError


class SueldoFijo(EstrategiaSueldo):
    def calcular(self, empleado: "Empleado") -> float:
        return float(empleado.sueldo_base)


class SueldoPorHoras(EstrategiaSueldo):
    def calcular(self, empleado: "Empleado") -> float:
        horas_trabajadas = float(getattr(empleado, "horas_trabajadas", 0))
        tarifa_por_hora = float(getattr(empleado, "tarifa_por_hora", 0))
        return horas_trabajadas * tarifa_por_hora
