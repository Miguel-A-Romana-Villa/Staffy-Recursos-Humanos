from dataclasses import dataclass


@dataclass
class Empleado:
    codigo: str
    dni: str
    nombres: str
    apellidos: str
    cargo: str
    sueldo_base: float
    activo: bool = True
