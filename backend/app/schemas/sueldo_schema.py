from pydantic import BaseModel, Field


class SueldoCalculoRequest(BaseModel):
    empleado_codigo: str
    periodo: str
    bonos: float = 0
    descuentos: float = 0


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
