import re
from dataclasses import dataclass
from math import isfinite
from typing import Optional

from app.domain.exceptions import DatoInvalidoError


@dataclass
class ConceptoPago:
    empleado_id: int
    tipo: str
    concepto: str
    monto: float
    periodo: str
    id: Optional[int] = None

    def __post_init__(self):
        self.tipo = str(self.tipo or "").strip().upper()
        self.concepto = str(self.concepto or "").strip()
        self.periodo = str(self.periodo or "").strip()
        try:
            self.monto = float(self.monto)
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError("El monto del concepto debe ser numerico") from exc

        if self.tipo not in ["BONO", "DESCUENTO"]:
            raise DatoInvalidoError("El tipo de concepto debe ser BONO o DESCUENTO")
        if not self.concepto:
            raise DatoInvalidoError("El concepto es obligatorio")
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", self.periodo):
            raise DatoInvalidoError("El periodo debe tener el formato AAAA-MM")
        if not isfinite(self.monto) or self.monto <= 0:
            raise DatoInvalidoError("El monto del concepto debe ser mayor a cero")

    def es_bono(self) -> bool:
        return self.tipo == "BONO"

    def es_descuento(self) -> bool:
        return self.tipo == "DESCUENTO"

    def pertenece_al_periodo(self, periodo: str) -> bool:
        return self.periodo == periodo.strip()
