from sqlalchemy.orm import Session

from app.db.models import AsistenciaDB, BoletaDB, EmpleadoDB


class ReporteService:
    def __init__(self, db: Session):
        self.db = db

    def resumen(self) -> dict:
        empleados = self.db.query(EmpleadoDB).filter(EmpleadoDB.activo.is_(True)).all()
        boletas = self.db.query(BoletaDB).all()
        asistencias = self.db.query(AsistenciaDB).all()

        return {
            "total_empleados": len(empleados),
            "total_pagos": sum(float(item.sueldo_neto) for item in boletas),
            "total_tardanzas": len([item for item in asistencias if item.estado == "TARDE"]),
            "total_faltas": len([item for item in asistencias if item.estado == "FALTO"]),
        }

    def pagos_por_periodo(self) -> list[dict]:
        periodos: dict[str, dict] = {}
        for boleta in self.db.query(BoletaDB).all():
            item = periodos.setdefault(
                boleta.periodo,
                {"periodo": boleta.periodo, "cantidad_boletas": 0, "total_pagado": 0},
            )
            item["cantidad_boletas"] += 1
            item["total_pagado"] += float(boleta.sueldo_neto)
        return list(periodos.values())

    def asistencias_por_empleado(self) -> list[dict]:
        empleados = self.db.query(EmpleadoDB).order_by(EmpleadoDB.id).all()
        reportes = []
        for empleado in empleados:
            asistencias = empleado.asistencias
            reportes.append(
                {
                    "empleado_codigo": empleado.codigo,
                    "empleado_nombre": f"{empleado.nombres} {empleado.apellidos}",
                    "asistio": len([item for item in asistencias if item.estado == "ASISTIO"]),
                    "tarde": len([item for item in asistencias if item.estado == "TARDE"]),
                    "falto": len([item for item in asistencias if item.estado == "FALTO"]),
                }
            )
        return reportes
