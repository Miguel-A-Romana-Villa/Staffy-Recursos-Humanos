from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.empleado_schema import EmpleadoCreate, EmpleadoResponse, EmpleadoUpdate
from app.services.empleado_service import EmpleadoService

router = APIRouter()


@router.get("", response_model=list[EmpleadoResponse])
def listar_empleados(search: str | None = None, db: Session = Depends(get_db)):
    return EmpleadoService(db).listar(search)


@router.get("/activos", response_model=list[EmpleadoResponse])
def listar_empleados_activos(periodo: str = Query(..., pattern=r"^\d{4}-\d{2}$"), db: Session = Depends(get_db)):
    return EmpleadoService(db).listar_activos_por_periodo(periodo)


@router.post("", response_model=EmpleadoResponse)
def crear_empleado(payload: EmpleadoCreate, db: Session = Depends(get_db)):
    try:
        return EmpleadoService(db).crear(payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un empleado con ese codigo o DNI",
        ) from exc


@router.put("/{empleado_id}", response_model=EmpleadoResponse)
def actualizar_empleado(empleado_id: int, payload: EmpleadoUpdate, db: Session = Depends(get_db)):
    empleado = EmpleadoService(db).actualizar(empleado_id, payload)
    if empleado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")

    return empleado
