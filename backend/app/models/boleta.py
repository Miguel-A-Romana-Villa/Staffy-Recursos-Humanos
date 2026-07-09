from dataclasses import dataclass


@dataclass
class Boleta:
    id: int
    empleado_codigo: str
    empleado_nombre: str
    dni: str
    cargo: str
    periodo: str
    sueldo_base: float
    bonos: float
    descuentos: float

    def calcular_sueldo_neto(self) -> float:
        return self.sueldo_base + self.bonos - self.descuentos

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "empleado_codigo": self.empleado_codigo,
            "empleado_nombre": self.empleado_nombre,
            "dni": self.dni,
            "cargo": self.cargo,
            "periodo": self.periodo,
            "sueldo_base": self.sueldo_base,
            "bonos": self.bonos,
            "descuentos": self.descuentos,
            "sueldo_neto": self.calcular_sueldo_neto(),
        }
