from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmpleadoBase(BaseModel):
    codigo: str
    dni: str
    correo: Optional[str] = None
    telefono: Optional[str] = None
    nombres: str
    apellidos: str
    cargo: str
    sueldo_base: float = Field(gt=0)
    tipo: str = "tiempo_completo"
    horas_trabajadas: Optional[float] = Field(default=None, gt=0)
    tarifa_por_hora: Optional[float] = Field(default=None, gt=0)
    hijos: int = Field(default=0, ge=0)
    fecha_nacimiento: Optional[date] = None
    fecha_inicio: Optional[date] = None
    fecha_cese: Optional[date] = None
    regimen_pensionario: str = "AFP"
    foto_url: Optional[str] = None
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    codigo: Optional[str] = None
    dni: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    cargo: Optional[str] = None
    sueldo_base: Optional[float] = Field(default=None, gt=0)
    tipo: Optional[str] = None
    horas_trabajadas: Optional[float] = Field(default=None, gt=0)
    tarifa_por_hora: Optional[float] = Field(default=None, gt=0)
    hijos: Optional[int] = Field(default=None, ge=0)
    fecha_nacimiento: Optional[date] = None
    fecha_inicio: Optional[date] = None
    fecha_cese: Optional[date] = None
    regimen_pensionario: Optional[str] = None
    foto_url: Optional[str] = None
    activo: Optional[bool] = None


class EmpleadoResponse(EmpleadoBase):
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
