from dataclasses import dataclass
from datetime import date


@dataclass
class Asistencia:
    empleado_codigo: str
    fecha: date
    estado: str
