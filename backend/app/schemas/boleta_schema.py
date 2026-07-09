from typing import Optional

from pydantic import BaseModel


class BoletaBase(BaseModel):
    empleado_codigo: str
    periodo: str
    bonos: float = 0
    descuentos: float = 0


class BoletaCreate(BoletaBase):
    pass


class BoletaResponse(BoletaBase):
    id: Optional[int] = None
    empleado_nombre: str
    dni: str
    cargo: str
    sueldo_base: float
    sueldo_neto: float
