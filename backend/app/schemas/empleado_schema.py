from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class EmpleadoBase(BaseModel):
    codigo: str
    dni: str
    correo: str | None = None
    telefono: str | None = None
    nombres: str
    apellidos: str
    cargo: str
    sueldo_base: float = Field(gt=0)
    hijos: int = Field(default=0, ge=0)
    fecha_nacimiento: date | None = None
    fecha_inicio: date | None = None
    fecha_cese: date | None = None
    regimen_pensionario: str = "AFP"
    foto_url: str | None = None
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    codigo: str | None = None
    dni: str | None = None
    correo: str | None = None
    telefono: str | None = None
    nombres: str | None = None
    apellidos: str | None = None
    cargo: str | None = None
    sueldo_base: float | None = Field(default=None, gt=0)
    hijos: int | None = Field(default=None, ge=0)
    fecha_nacimiento: date | None = None
    fecha_inicio: date | None = None
    fecha_cese: date | None = None
    regimen_pensionario: str | None = None
    foto_url: str | None = None
    activo: bool | None = None


class EmpleadoResponse(EmpleadoBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)
