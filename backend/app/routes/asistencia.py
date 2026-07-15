from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.exceptions import EmpleadoNoEncontradoError, StaffyError
from app.schemas.asistencia_schema import AsistenciaCreate, AsistenciaResponse
from app.services.asistencia_service import AsistenciaService

router = APIRouter()


@router.get("", response_model=list[AsistenciaResponse])
def listar_asistencias(
    empleado_id: Optional[int] = None,
    periodo: Optional[str] = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db),
):
    return AsistenciaService(db).listar(empleado_id=empleado_id, periodo=periodo)


@router.post("", response_model=AsistenciaResponse)
def registrar_asistencia(payload: AsistenciaCreate, db: Session = Depends(get_db)):
    try:
        return AsistenciaService(db).registrar_o_actualizar(payload)
    except EmpleadoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except StaffyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asistencia(empleado_id: int, fecha: date, db: Session = Depends(get_db)):
    AsistenciaService(db).eliminar_por_fecha(empleado_id=empleado_id, fecha=fecha)
