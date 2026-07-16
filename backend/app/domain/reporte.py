import re
from dataclasses import dataclass, field
from math import isfinite

from app.domain.exceptions import DatoInvalidoError


def normalizar_periodo(periodo: str) -> str:
    periodo_limpio = str(periodo or "").strip()
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", periodo_limpio):
        raise DatoInvalidoError("El periodo debe tener el formato AAAA-MM")
    return periodo_limpio


def validar_entero(valor: int, nombre: str) -> int:
    numero = int(valor)
    if numero < 0:
        raise DatoInvalidoError(f"{nombre} no puede ser negativo")
    return numero


@dataclass(frozen=True)
class ResumenReporte:
    total_empleados: int
    total_pagos: float
    total_tardanzas: int
    total_faltas: int

    def __post_init__(self):
        object.__setattr__(self, "total_empleados", validar_entero(self.total_empleados, "El total de empleados"))
        object.__setattr__(self, "total_tardanzas", validar_entero(self.total_tardanzas, "El total de tardanzas"))
        object.__setattr__(self, "total_faltas", validar_entero(self.total_faltas, "El total de faltas"))
        total_pagos = float(self.total_pagos)
        if not isfinite(total_pagos) or total_pagos < 0:
            raise DatoInvalidoError("El total de pagos no puede ser negativo")
        object.__setattr__(self, "total_pagos", round(total_pagos, 2))


@dataclass(frozen=True)
class PagoPorPeriodo:
    periodo: str
    cantidad_boletas: int
    total_pagado: float

    def __post_init__(self):
        object.__setattr__(self, "periodo", normalizar_periodo(self.periodo))
        object.__setattr__(self, "cantidad_boletas", validar_entero(self.cantidad_boletas, "La cantidad de boletas"))
        total_pagado = float(self.total_pagado)
        if not isfinite(total_pagado) or total_pagado < 0:
            raise DatoInvalidoError("El total pagado no puede ser negativo")
        object.__setattr__(self, "total_pagado", round(total_pagado, 2))


@dataclass(frozen=True)
class AsistenciaEmpleado:
    empleado_codigo: str
    empleado_nombre: str
    asistio: int
    tarde: int
    falto: int

    def __post_init__(self):
        codigo = str(self.empleado_codigo or "").strip()
        nombre = str(self.empleado_nombre or "").strip()
        if not codigo or not nombre:
            raise DatoInvalidoError("Los datos del empleado son obligatorios en el reporte")
        object.__setattr__(self, "empleado_codigo", codigo)
        object.__setattr__(self, "empleado_nombre", nombre)
        object.__setattr__(self, "asistio", validar_entero(self.asistio, "Las asistencias"))
        object.__setattr__(self, "tarde", validar_entero(self.tarde, "Las tardanzas"))
        object.__setattr__(self, "falto", validar_entero(self.falto, "Las faltas"))

    def total_registros(self) -> int:
        return self.asistio + self.tarde + self.falto


@dataclass(frozen=True)
class ReporteGeneral:
    periodo: str
    resumen: ResumenReporte
    pagos: tuple[PagoPorPeriodo, ...] = field(default_factory=tuple)
    asistencias: tuple[AsistenciaEmpleado, ...] = field(default_factory=tuple)

    def __post_init__(self):
        if not isinstance(self.resumen, ResumenReporte):
            raise DatoInvalidoError("El resumen del reporte no es valido")
        pagos = tuple(self.pagos)
        asistencias = tuple(self.asistencias)
        if not all(isinstance(item, PagoPorPeriodo) for item in pagos):
            raise DatoInvalidoError("Los pagos del reporte no son validos")
        if not all(isinstance(item, AsistenciaEmpleado) for item in asistencias):
            raise DatoInvalidoError("Las asistencias del reporte no son validas")
        object.__setattr__(self, "periodo", normalizar_periodo(self.periodo))
        object.__setattr__(self, "pagos", pagos)
        object.__setattr__(self, "asistencias", asistencias)

    def total_registros_asistencia(self) -> int:
        return sum(item.total_registros() for item in self.asistencias)
