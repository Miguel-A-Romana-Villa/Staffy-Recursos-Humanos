from datetime import date

from pydantic import BaseModel


class AsistenciaBase(BaseModel):
    empleado_codigo: str
    fecha: date
    estado: str


class AsistenciaCreate(AsistenciaBase):
    pass


class AsistenciaResponse(AsistenciaBase):
    id: int | None = None
