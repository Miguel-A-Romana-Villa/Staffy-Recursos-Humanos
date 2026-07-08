from pydantic import BaseModel


class BoletaBase(BaseModel):
    empleado_codigo: str
    periodo: str
    sueldo_base: float
    bonos: float = 0
    descuentos: float = 0


class BoletaCreate(BoletaBase):
    pass


class BoletaResponse(BoletaBase):
    id: int | None = None
    sueldo_neto: float
