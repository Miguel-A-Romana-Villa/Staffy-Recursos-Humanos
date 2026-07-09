from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class UsuarioCreate(BaseModel):
    nombres: str
    email: str
    password: str
    rol: str = "RRHH"


class UsuarioSesion(BaseModel):
    id: int
    nombres: str
    email: str
    rol: str


class LoginResponse(BaseModel):
    access_token: str
    usuario: UsuarioSesion
