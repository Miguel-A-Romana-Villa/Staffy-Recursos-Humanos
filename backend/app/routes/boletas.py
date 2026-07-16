from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.exceptions import BoletaDuplicadaError, EmpleadoNoEncontradoError, StaffyError
from app.schemas.boleta_schema import BoletaCreate, BoletaResponse
from app.services.boleta_service import BoletaService

router = APIRouter()


@router.get("", response_model=list[BoletaResponse])
def listar_boletas(db: Session = Depends(get_db)):
    return BoletaService(db).listar()


@router.get("/{empleado_codigo}", response_model=list[BoletaResponse])
def listar_boletas_por_empleado(empleado_codigo: str, db: Session = Depends(get_db)):
    return BoletaService(db).listar_por_empleado(empleado_codigo)


@router.post("/generar", response_model=BoletaResponse)
def generar_boleta(payload: BoletaCreate, db: Session = Depends(get_db)):
    try:
        return BoletaService(db).generar(payload)
    except EmpleadoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BoletaDuplicadaError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except StaffyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
