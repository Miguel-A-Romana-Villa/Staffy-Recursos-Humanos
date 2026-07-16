from typing import Optional

from pydantic import BaseModel, Field


class BoletaBase(BaseModel):
    empleado_codigo: str = Field(min_length=1)
    periodo: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    bonos: float = Field(default=0, ge=0, allow_inf_nan=False)
    descuentos: float = Field(default=0, ge=0, allow_inf_nan=False)


class BoletaCreate(BoletaBase):
    pass


class BoletaResponse(BoletaBase):
    id: Optional[int] = None
    empleado_nombre: str
    dni: str
    cargo: str
    sueldo_base: float
    sueldo_neto: float
