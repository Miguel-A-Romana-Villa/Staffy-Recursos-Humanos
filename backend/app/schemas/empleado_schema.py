from pydantic import BaseModel, Field


class EmpleadoBase(BaseModel):
    codigo: str
    dni: str
    nombres: str
    apellidos: str
    cargo: str
    sueldo_base: float = Field(gt=0)
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoResponse(EmpleadoBase):
    id: int | None = None
