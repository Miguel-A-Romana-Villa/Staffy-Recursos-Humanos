from dataclasses import dataclass


@dataclass
class Boleta:
    empleado_codigo: str
    periodo: str
    sueldo_base: float
    bonos: float
    descuentos: float

    def calcular_sueldo_neto(self) -> float:
        return self.sueldo_base + self.bonos - self.descuentos
