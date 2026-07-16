from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.db.models import UsuarioDB
from app.services.auth_service import AuthService

portador = HTTPBearer(auto_error=False)


def requerir_usuario(
    credenciales: Optional[HTTPAuthorizationCredentials] = Depends(portador),
    db: Session = Depends(get_db),
) -> UsuarioDB:
    usuario = None
    if credenciales is not None and credenciales.scheme.lower() == "bearer":
        usuario = AuthService(db).usuario_desde_token(credenciales.credentials)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesion invalida o vencida",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario
