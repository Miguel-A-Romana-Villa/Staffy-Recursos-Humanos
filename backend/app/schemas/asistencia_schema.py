from datetime import date

from pydantic import BaseModel, ConfigDict


class AsistenciaBase(BaseModel):
    empleado_id: int
    fecha: date
    estado: str
    minutos_tardanza: int | None = None
    comentario: str | None = None


class AsistenciaCreate(AsistenciaBase):
    pass


class AsistenciaResponse(AsistenciaBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)
