import base64
import binascii
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.config import settings
from app.db.models import UsuarioDB
from app.schemas.auth_schema import LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, payload: LoginRequest) -> Optional[UsuarioDB]:
        usuario = self.db.query(UsuarioDB).filter(UsuarioDB.email == payload.email).first()
        if usuario is None or not usuario.activo or not self.verificar_password(payload.password, usuario.password):
            return None

        if not usuario.password.startswith("pbkdf2_sha256$"):
            usuario.password = self.encriptar_password(payload.password)
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def crear_token(self, usuario: UsuarioDB) -> str:
        vence = datetime.now(timezone.utc) + timedelta(hours=settings.auth_token_hours)
        datos = json.dumps(
            {"usuario_id": usuario.id, "exp": int(vence.timestamp())},
            separators=(",", ":"),
        ).encode()
        contenido = self._codificar(datos)
        firma = hmac.new(settings.auth_secret.encode(), contenido.encode(), hashlib.sha256).digest()
        return f"{contenido}.{self._codificar(firma)}"

    def usuario_desde_token(self, token: str) -> Optional[UsuarioDB]:
        try:
            contenido, firma_recibida = token.split(".", 1)
            firma = hmac.new(settings.auth_secret.encode(), contenido.encode(), hashlib.sha256).digest()
            if not hmac.compare_digest(self._codificar(firma), firma_recibida):
                return None
            datos = json.loads(self._decodificar(contenido))
            if int(datos["exp"]) <= int(datetime.now(timezone.utc).timestamp()):
                return None
            usuario_id = int(datos["usuario_id"])
        except (binascii.Error, KeyError, TypeError, ValueError, json.JSONDecodeError):
            return None

        return self.db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id, UsuarioDB.activo.is_(True)).first()

    def asegurar_admin_inicial(self) -> None:
        existe_admin = self.db.query(UsuarioDB).filter(UsuarioDB.email == "admin@staffy.com").first()
        if existe_admin is not None:
            if not existe_admin.password.startswith("pbkdf2_sha256$"):
                existe_admin.password = self.encriptar_password(existe_admin.password)
                self.db.commit()
            return

        self.db.add(
            UsuarioDB(
                nombres="Administrador",
                email="admin@staffy.com",
                password=self.encriptar_password("123456"),
                rol="RRHH",
            )
        )
        self.db.commit()

    @staticmethod
    def encriptar_password(password: str) -> str:
        salt = secrets.token_hex(16)
        clave = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 120_000).hex()
        return f"pbkdf2_sha256${salt}${clave}"

    @staticmethod
    def verificar_password(password: str, password_guardada: str) -> bool:
        if not password_guardada.startswith("pbkdf2_sha256$"):
            return hmac.compare_digest(password, password_guardada)
        try:
            _, salt, clave_guardada = password_guardada.split("$", 2)
            clave = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 120_000).hex()
            return hmac.compare_digest(clave, clave_guardada)
        except ValueError:
            return False

    @staticmethod
    def _codificar(contenido: bytes) -> str:
        return base64.urlsafe_b64encode(contenido).decode().rstrip("=")

    @staticmethod
    def _decodificar(contenido: str) -> bytes:
        relleno = "=" * (-len(contenido) % 4)
        return base64.urlsafe_b64decode(contenido + relleno)
