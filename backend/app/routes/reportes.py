from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.reporte_schema import (
    ReporteAsistenciaEmpleado,
    ReporteGeneralResponse,
    ReportePagoPeriodo,
    ReporteResumen,
)
from app.security import requerir_usuario
from app.services.reporte_pdf_service import ReportePdfService
from app.services.reporte_service import ReporteService

router = APIRouter(dependencies=[Depends(requerir_usuario)])
periodo_query = Query(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")


@router.get("/general", response_model=ReporteGeneralResponse)
def obtener_reporte_general(periodo: str = periodo_query, db: Session = Depends(get_db)):
    return ReporteService(db).generar(periodo)


@router.get("/resumen", response_model=ReporteResumen)
def obtener_resumen(periodo: str = periodo_query, db: Session = Depends(get_db)):
    return ReporteService(db).resumen(periodo)


@router.get("/pagos", response_model=list[ReportePagoPeriodo])
def listar_pagos_por_periodo(periodo: str = periodo_query, db: Session = Depends(get_db)):
    return ReporteService(db).pagos_por_periodo(periodo)


@router.get("/asistencias", response_model=list[ReporteAsistenciaEmpleado])
def listar_asistencias_por_empleado(periodo: str = periodo_query, db: Session = Depends(get_db)):
    return ReporteService(db).asistencias_por_empleado(periodo)


@router.get("/pdf")
def descargar_reporte_pdf(periodo: str = periodo_query, db: Session = Depends(get_db)):
    contenido = ReportePdfService(db).generar(periodo)
    nombre = f"reporte-staffy-{periodo}.pdf"
    return Response(
        content=contenido,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )
