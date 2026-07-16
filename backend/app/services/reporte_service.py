from datetime import date

from sqlalchemy import and_, case, func
from sqlalchemy.orm import Session

from app.db.models import AsistenciaDB, BoletaDB, EmpleadoDB
from app.domain.reporte import AsistenciaEmpleado, PagoPorPeriodo, ReporteGeneral, ResumenReporte, normalizar_periodo
from app.services.empleado_service import obtener_rango_periodo


class ReporteService:
    def __init__(self, db: Session):
        self.db = db

    def generar(self, periodo: str) -> ReporteGeneral:
        periodo_limpio = normalizar_periodo(periodo)
        inicio, fin = obtener_rango_periodo(periodo_limpio)
        asistencias = self._asistencias(inicio, fin)
        pago = self._pago(periodo_limpio)
        resumen = ResumenReporte(
            total_empleados=len(asistencias),
            total_pagos=pago.total_pagado,
            total_tardanzas=sum(item.tarde for item in asistencias),
            total_faltas=sum(item.falto for item in asistencias),
        )
        pagos = [] if pago.cantidad_boletas == 0 else [pago]
        return ReporteGeneral(
            periodo=periodo_limpio,
            resumen=resumen,
            pagos=pagos,
            asistencias=asistencias,
        )

    def resumen(self, periodo: str) -> ResumenReporte:
        return self.generar(periodo).resumen

    def pagos_por_periodo(self, periodo: str) -> list[PagoPorPeriodo]:
        return list(self.generar(periodo).pagos)

    def asistencias_por_empleado(self, periodo: str) -> list[AsistenciaEmpleado]:
        return list(self.generar(periodo).asistencias)

    def _pago(self, periodo: str) -> PagoPorPeriodo:
        cantidad, total = (
            self.db.query(func.count(BoletaDB.id), func.coalesce(func.sum(BoletaDB.sueldo_neto), 0.0))
            .filter(BoletaDB.periodo == periodo)
            .one()
        )
        return PagoPorPeriodo(
            periodo=periodo,
            cantidad_boletas=int(cantidad),
            total_pagado=float(total),
        )

    def _asistencias(self, inicio: date, fin: date) -> list[AsistenciaEmpleado]:
        asistio = func.coalesce(func.sum(case((AsistenciaDB.estado == "ASISTIO", 1), else_=0)), 0)
        tarde = func.coalesce(func.sum(case((AsistenciaDB.estado == "TARDE", 1), else_=0)), 0)
        falto = func.coalesce(func.sum(case((AsistenciaDB.estado == "FALTO", 1), else_=0)), 0)
        filas = (
            self.db.query(
                EmpleadoDB.codigo,
                EmpleadoDB.nombres,
                EmpleadoDB.apellidos,
                asistio.label("asistio"),
                tarde.label("tarde"),
                falto.label("falto"),
            )
            .outerjoin(
                AsistenciaDB,
                and_(
                    AsistenciaDB.empleado_id == EmpleadoDB.id,
                    AsistenciaDB.fecha >= inicio,
                    AsistenciaDB.fecha <= fin,
                ),
            )
            .filter(EmpleadoDB.activo.is_(True))
            .filter((EmpleadoDB.fecha_inicio.is_(None)) | (EmpleadoDB.fecha_inicio <= fin))
            .filter((EmpleadoDB.fecha_cese.is_(None)) | (EmpleadoDB.fecha_cese >= inicio))
            .group_by(EmpleadoDB.id, EmpleadoDB.codigo, EmpleadoDB.nombres, EmpleadoDB.apellidos)
            .order_by(EmpleadoDB.codigo)
            .all()
        )
        return [
            AsistenciaEmpleado(
                empleado_codigo=fila.codigo,
                empleado_nombre=f"{fila.nombres} {fila.apellidos}",
                asistio=int(fila.asistio),
                tarde=int(fila.tarde),
                falto=int(fila.falto),
            )
            for fila in filas
        ]
