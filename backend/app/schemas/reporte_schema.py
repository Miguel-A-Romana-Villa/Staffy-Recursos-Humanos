from pydantic import BaseModel


class ReporteResumen(BaseModel):
    total_empleados: int
    total_pagos: float
    total_tardanzas: int
    total_faltas: int


class ReportePagoPeriodo(BaseModel):
    periodo: str
    cantidad_boletas: int
    total_pagado: float


class ReporteAsistenciaEmpleado(BaseModel):
    empleado_codigo: str
    empleado_nombre: str
    asistio: int
    tarde: int
    falto: int
