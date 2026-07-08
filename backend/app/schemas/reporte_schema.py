from pydantic import BaseModel


class ReporteResponse(BaseModel):
    nombre: str
    descripcion: str
