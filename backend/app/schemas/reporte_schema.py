from pydantic import BaseModel, ConfigDict, Field


class ReporteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReporteResumen(ReporteSchema):
    total_empleados: int = Field(ge=0)
    total_pagos: float = Field(ge=0)
    total_tardanzas: int = Field(ge=0)
    total_faltas: int = Field(ge=0)


class ReportePagoPeriodo(ReporteSchema):
    periodo: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    cantidad_boletas: int = Field(ge=0)
    total_pagado: float = Field(ge=0)


class ReporteAsistenciaEmpleado(ReporteSchema):
    empleado_codigo: str
    empleado_nombre: str
    asistio: int = Field(ge=0)
    tarde: int = Field(ge=0)
    falto: int = Field(ge=0)


class ReporteGeneralResponse(ReporteSchema):
    periodo: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    resumen: ReporteResumen
    pagos: list[ReportePagoPeriodo]
    asistencias: list[ReporteAsistenciaEmpleado]
