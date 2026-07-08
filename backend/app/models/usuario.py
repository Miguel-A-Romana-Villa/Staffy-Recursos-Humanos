from dataclasses import dataclass


@dataclass
class Usuario:
    nombres: str
    email: str
    rol: str
    activo: bool = True
