from typing import Optional

from app.services.json_store import JsonStore


class ReporteService:
    def __init__(self, store: Optional[JsonStore] = None):
        self.store = store or JsonStore()

    def resumen(self) -> dict:
        data = self.store.read()
        empleados_activos = [empleado for empleado in data["empleados"] if empleado.get("activo", True)]

        return {
            "total_empleados": len(empleados_activos),
            "total_pagos": sum(float(boleta["sueldo_neto"]) for boleta in data["boletas"]),
            "total_tardanzas": len([item for item in data["asistencias"] if item["estado"] == "TARDE"]),
            "total_faltas": len([item for item in data["asistencias"] if item["estado"] == "FALTO"]),
        }

    def pagos_por_periodo(self) -> list[dict]:
        data = self.store.read()
        periodos: dict[str, dict] = {}

        for boleta in data["boletas"]:
            periodo = boleta["periodo"]
            item = periodos.setdefault(
                periodo,
                {"periodo": periodo, "cantidad_boletas": 0, "total_pagado": 0},
            )
            item["cantidad_boletas"] += 1
            item["total_pagado"] += float(boleta["sueldo_neto"])

        return list(periodos.values())

    def asistencias_por_empleado(self) -> list[dict]:
        data = self.store.read()
        empleados = {empleado["codigo"]: empleado for empleado in data["empleados"]}
        reportes: dict[str, dict] = {}

        for asistencia in data["asistencias"]:
            codigo = asistencia["empleado_codigo"]
            empleado = empleados.get(codigo, {})
            item = reportes.setdefault(
                codigo,
                {
                    "empleado_codigo": codigo,
                    "empleado_nombre": f'{empleado.get("nombres", "")} {empleado.get("apellidos", "")}'.strip() or codigo,
                    "asistio": 0,
                    "tarde": 0,
                    "falto": 0,
                },
            )

            if asistencia["estado"] == "ASISTIO":
                item["asistio"] += 1
            if asistencia["estado"] == "TARDE":
                item["tarde"] += 1
            if asistencia["estado"] == "FALTO":
                item["falto"] += 1

        return list(reportes.values())
