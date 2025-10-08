from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int 
    name: str
    username: str
    password_hash: str
    role: str = "usuario"
    active: bool = True
    created_at: datetime | None = None
