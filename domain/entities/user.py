from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    nombre: str
    username: str
    password_hash: str
    rol: str
    activo: bool
    fecha_creacion: datetime
