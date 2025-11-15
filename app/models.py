
from typing import Optional
from pydantic import BaseModel, constr

class LoginRequest(BaseModel):
    # Исправлено: добавлены ограничения длины и формата
    username: constr(strip_whitespace=True, min_length=3, max_length=48, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: constr(min_length=3, max_length=128)

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
