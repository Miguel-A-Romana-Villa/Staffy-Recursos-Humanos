from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.exceptions import EmpleadoNoEncontradoError, StaffyError
from app.schemas.concepto_schema import ConceptoPagoCreate, ConceptoPagoResponse
from app.services.concepto_service import ConceptoPagoService

router = APIRouter()


@router.get("", response_model=list[ConceptoPagoResponse])
def listar_conceptos(
    empleado_id: Optional[int] = None,
    periodo: Optional[str] = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db),
):
    return ConceptoPagoService(db).listar(empleado_id=empleado_id, periodo=periodo)


@router.post("", response_model=ConceptoPagoResponse)
def registrar_concepto(payload: ConceptoPagoCreate, db: Session = Depends(get_db)):
    try:
        return ConceptoPagoService(db).registrar(payload)
    except EmpleadoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except StaffyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
