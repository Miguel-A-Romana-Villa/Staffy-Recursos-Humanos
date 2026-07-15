from dataclasses import dataclass
from typing import Optional


@dataclass
class ConceptoPago:
    empleado_id: int
    tipo: str
    concepto: str
    monto: float
    periodo: str
    id: Optional[int] = None
