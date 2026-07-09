from fastapi import APIRouter

from app.schemas.boleta_schema import BoletaCreate, BoletaResponse
from app.services.boleta_service import BoletaService

router = APIRouter()


@router.get("", response_model=list[BoletaResponse])
def listar_boletas():
    return BoletaService().listar()


@router.get("/{empleado_codigo}", response_model=list[BoletaResponse])
def listar_boletas_por_empleado(empleado_codigo: str):
    return BoletaService().listar_por_empleado(empleado_codigo)


@router.post("/generar", response_model=BoletaResponse)
def generar_boleta(payload: BoletaCreate):
    return BoletaService().generar(payload.dict())
