from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AsistenciaBase(BaseModel):
    empleado_id: int
    fecha: date
    estado: str
    minutos_tardanza: Optional[int] = None
    comentario: Optional[str] = None


class AsistenciaCreate(AsistenciaBase):
    pass


class AsistenciaResponse(AsistenciaBase):
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
