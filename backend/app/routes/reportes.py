from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.reporte_schema import ReporteAsistenciaEmpleado, ReportePagoPeriodo, ReporteResumen
from app.services.reporte_service import ReporteService

router = APIRouter()


@router.get("/resumen", response_model=ReporteResumen)
def obtener_resumen(db: Session = Depends(get_db)):
    return ReporteService(db).resumen()


@router.get("/pagos", response_model=list[ReportePagoPeriodo])
def listar_pagos_por_periodo(db: Session = Depends(get_db)):
    return ReporteService(db).pagos_por_periodo()


@router.get("/asistencias", response_model=list[ReporteAsistenciaEmpleado])
def listar_asistencias_por_empleado(db: Session = Depends(get_db)):
    return ReporteService(db).asistencias_por_empleado()
