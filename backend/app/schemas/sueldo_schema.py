from pydantic import BaseModel, Field


class SueldoCalculoRequest(BaseModel):
    empleado_codigo: str = Field(min_length=1)
    periodo: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    bonos: float = Field(default=0, ge=0, allow_inf_nan=False)
    descuentos: float = Field(default=0, ge=0, allow_inf_nan=False)


class ConceptoSueldoResponse(BaseModel):
    tipo: str
    concepto: str
    monto: float
    periodo: str


class SueldoCalculoResponse(BaseModel):
    empleado_codigo: str
    empleado_nombre: str
    dni: str
    cargo: str
    periodo: str
    sueldo_base: float
    bonos: float
    descuentos: float
    sueldo_neto: float
    conceptos: list[ConceptoSueldoResponse] = Field(default_factory=list)
