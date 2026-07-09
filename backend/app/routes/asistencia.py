from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.asistencia_schema import AsistenciaCreate, AsistenciaResponse
from app.services.asistencia_service import AsistenciaService

router = APIRouter()


@router.get("", response_model=list[AsistenciaResponse])
def listar_asistencias(
    empleado_id: int | None = None,
    periodo: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db),
):
    return AsistenciaService(db).listar(empleado_id=empleado_id, periodo=periodo)


@router.post("", response_model=AsistenciaResponse)
def registrar_asistencia(payload: AsistenciaCreate, db: Session = Depends(get_db)):
    return AsistenciaService(db).registrar_o_actualizar(payload)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asistencia(empleado_id: int, fecha: date, db: Session = Depends(get_db)):
    AsistenciaService(db).eliminar_por_fecha(empleado_id=empleado_id, fecha=fecha)
