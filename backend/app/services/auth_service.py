from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import UsuarioDB
from app.schemas.auth_schema import LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, payload: LoginRequest) -> Optional[UsuarioDB]:
        usuario = self.db.query(UsuarioDB).filter(UsuarioDB.email == payload.email).first()
        if usuario is None or usuario.password != payload.password or not usuario.activo:
            return None

        return usuario

    def asegurar_admin_inicial(self) -> None:
        existe_admin = self.db.query(UsuarioDB).filter(UsuarioDB.email == "admin@staffy.com").first()
        if existe_admin is not None:
            return

        self.db.add(
            UsuarioDB(
                nombres="Administrador",
                email="admin@staffy.com",
                password="123456",
                rol="RRHH",
            )
        )
        self.db.commit()
