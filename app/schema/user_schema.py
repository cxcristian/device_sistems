from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class userBase(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    role: str = Literal["admin", "support", "user"]
    is_active: bool = True

class UserCreate(UserBase):
    """Usado para el cuerpo de la petición POST (sin id)."""
    pass


class UserOut(BaseModel):
    """Usado para las respuestas GET/POST (con id). Oculta datos internos."""
    id: int
    name: str
    email: str
    role: str
    is_active: bool