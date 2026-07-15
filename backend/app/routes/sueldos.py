from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.exceptions import EmpleadoNoEncontradoError, StaffyError
from app.schemas.sueldo_schema import SueldoCalculoRequest, SueldoCalculoResponse
from app.services.sueldo_service import SueldoService

router = APIRouter()


@router.post("/calcular", response_model=SueldoCalculoResponse)
def calcular_sueldo(payload: SueldoCalculoRequest, db: Session = Depends(get_db)):
    try:
        return SueldoService(db).calcular(
            empleado_codigo=payload.empleado_codigo,
            periodo=payload.periodo,
            bonos_extra=payload.bonos,
            descuentos_extra=payload.descuentos,
        )
    except EmpleadoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except StaffyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
