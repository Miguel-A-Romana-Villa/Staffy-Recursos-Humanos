from fastapi import APIRouter

from app.schemas.reporte_schema import ReporteAsistenciaEmpleado, ReportePagoPeriodo, ReporteResumen
from app.services.reporte_service import ReporteService

router = APIRouter()


@router.get("/resumen", response_model=ReporteResumen)
def obtener_resumen():
    return ReporteService().resumen()


@router.get("/pagos", response_model=list[ReportePagoPeriodo])
def listar_pagos_por_periodo():
    return ReporteService().pagos_por_periodo()


@router.get("/asistencias", response_model=list[ReporteAsistenciaEmpleado])
def listar_asistencias_por_empleado():
    return ReporteService().asistencias_por_empleado()
