from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Empleado(ABC):
    id: Optional[int]
    codigo: str
    dni: str
    nombres: str
    apellidos: str
    cargo: str
    sueldo_base: float
    correo: Optional[str] = None
    telefono: Optional[str] = None
    hijos: int = 0
    fecha_nacimiento: Optional[date] = None
    fecha_inicio: Optional[date] = None
    fecha_cese: Optional[date] = None
    regimen_pensionario: str = "AFP"
    foto_url: Optional[str] = None
    activo: bool = True

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}".strip()

    @property
    @abstractmethod
    def tipo(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def calcular_sueldo_base(self) -> float:
        raise NotImplementedError


class EmpleadoTiempoCompleto(Empleado):
    @property
    def tipo(self) -> str:
        return "tiempo_completo"

    def calcular_sueldo_base(self) -> float:
        return float(self.sueldo_base)


class EmpleadoMedioTiempo(Empleado):
    def __init__(self, horas_trabajadas: float, tarifa_por_hora: float, **kwargs):
        super().__init__(**kwargs)
        self.horas_trabajadas = float(horas_trabajadas or 0)
        self.tarifa_por_hora = float(tarifa_por_hora or 0)

    @property
    def tipo(self) -> str:
        return "medio_tiempo"

    def calcular_sueldo_base(self) -> float:
        return self.horas_trabajadas * self.tarifa_por_hora
