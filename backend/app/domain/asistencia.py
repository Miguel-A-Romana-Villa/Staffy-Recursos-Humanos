from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Asistencia:
    empleado_id: int
    fecha: date
    estado: str
    minutos_tardanza: Optional[int] = None
    comentario: Optional[str] = None
