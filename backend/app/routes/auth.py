from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import LoginRequest, LoginResponse, UsuarioSesion
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    servicio = AuthService(db)
    usuario = servicio.login(payload)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    return LoginResponse(
        access_token=servicio.crear_token(usuario),
        usuario=UsuarioSesion(
            id=usuario.id,
            nombres=usuario.nombres,
            email=usuario.email,
            rol=usuario.rol,
        ),
    )
