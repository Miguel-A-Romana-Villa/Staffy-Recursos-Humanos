import re
from dataclasses import dataclass, field
from math import isfinite
from typing import Optional

from app.domain.concepto_pago import ConceptoPago
from app.domain.empleado import Empleado
from app.domain.exceptions import DatoInvalidoError


@dataclass
class Boleta:
    empleado_codigo: str
    empleado_nombre: str
    dni: str
    cargo: str
    periodo: str
    sueldo_base: float
    bonos: float
    descuentos: float
    conceptos: list[ConceptoPago] = field(default_factory=list, repr=False)
    id: Optional[int] = None

    def __post_init__(self):
        self.empleado_codigo = str(self.empleado_codigo or "").strip()
        self.empleado_nombre = str(self.empleado_nombre or "").strip()
        self.dni = str(self.dni or "").strip()
        self.cargo = str(self.cargo or "").strip()
        self.periodo = self.normalizar_periodo(self.periodo)
        self.sueldo_base = self._validar_monto(self.sueldo_base, "El sueldo base", permite_cero=False)
        self.bonos = self._validar_monto(self.bonos, "Los bonos")
        self.descuentos = self._validar_monto(self.descuentos, "Los descuentos")

        if not self.empleado_codigo or not self.empleado_nombre or not self.dni or not self.cargo:
            raise DatoInvalidoError("Los datos del empleado son obligatorios para generar la boleta")
        if self.calcular_sueldo_neto() < 0:
            raise DatoInvalidoError("El sueldo neto no puede ser negativo")

    @classmethod
    def generar(
        cls,
        empleado: Empleado,
        periodo: str,
        conceptos: list[ConceptoPago],
        bonos_extra: float = 0,
        descuentos_extra: float = 0,
    ) -> "Boleta":
        periodo_limpio = cls.normalizar_periodo(periodo)
        bonos_adicionales = cls._validar_monto(bonos_extra, "Los bonos extra")
        descuentos_adicionales = cls._validar_monto(descuentos_extra, "Los descuentos extra")
        conceptos_periodo = []

        for concepto in conceptos:
            if not concepto.pertenece_al_periodo(periodo_limpio):
                continue
            conceptos_periodo.append(concepto)

        bonos = sum(item.monto for item in conceptos_periodo if item.es_bono())
        descuentos = sum(item.monto for item in conceptos_periodo if item.es_descuento())

        return cls(
            empleado_codigo=empleado.codigo,
            empleado_nombre=empleado.nombre_completo,
            dni=empleado.dni,
            cargo=empleado.cargo,
            periodo=periodo_limpio,
            sueldo_base=empleado.calcular_sueldo_base(),
            bonos=bonos + bonos_adicionales,
            descuentos=descuentos + descuentos_adicionales,
            conceptos=conceptos_periodo,
        )

    @staticmethod
    def normalizar_periodo(periodo: str) -> str:
        periodo_limpio = str(periodo or "").strip()
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", periodo_limpio):
            raise DatoInvalidoError("El periodo debe tener el formato AAAA-MM")
        return periodo_limpio

    @staticmethod
    def _validar_monto(monto: float, nombre: str, permite_cero: bool = True) -> float:
        try:
            valor = float(monto)
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError(f"{nombre} debe ser numerico") from exc
        if not isfinite(valor) or valor < 0 or (not permite_cero and valor == 0):
            condicion = "mayor a cero" if not permite_cero else "mayor o igual a cero"
            raise DatoInvalidoError(f"{nombre} debe ser {condicion}")
        return valor

    def calcular_sueldo_neto(self) -> float:
        return round(self.sueldo_base + self.bonos - self.descuentos, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "empleado_codigo": self.empleado_codigo,
            "empleado_nombre": self.empleado_nombre,
            "dni": self.dni,
            "cargo": self.cargo,
            "periodo": self.periodo,
            "sueldo_base": self.sueldo_base,
            "bonos": self.bonos,
            "descuentos": self.descuentos,
            "sueldo_neto": self.calcular_sueldo_neto(),
        }
