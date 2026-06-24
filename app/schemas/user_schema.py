from pydantic import BaseModel, Field, EmailStr,
from typing import Literal, Optional

class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    role:  Literal["admin", "support", "user"]
    is_active: bool = True



class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)
    pass

class UserUpdate(UserBase):
    name: str | None = Field(default=None, min_length=3, max_length=30)
    email: EmailStr | None = None
    role:  Literal["admin", "support", "user"] | None = None
    is_active: bool | None = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=20)

class UserDelete(BaseModel):
    detail: str = "Usuario eliminado"

class UserOut(BaseModel):
   
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    class Config:
        from_attributes = True