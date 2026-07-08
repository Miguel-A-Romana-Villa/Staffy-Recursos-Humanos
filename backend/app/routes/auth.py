from fastapi import APIRouter

from app.schemas.auth_schema import LoginRequest, LoginResponse, UsuarioSesion

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    return LoginResponse(
        access_token="token-pendiente-de-implementar",
        usuario=UsuarioSesion(
            id=1,
            nombres="Administrador",
            email=payload.email,
            rol="RRHH",
        ),
    )
