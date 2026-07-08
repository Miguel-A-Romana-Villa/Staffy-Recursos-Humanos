from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class UsuarioSesion(BaseModel):
    id: int
    nombres: str
    email: str
    rol: str


class LoginResponse(BaseModel):
    access_token: str
    usuario: UsuarioSesion
