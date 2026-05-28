from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    role:  Literal["admin", "support", "user"]
    is_active: bool = True

class UserCreate(UserBase):
    pass


class UserOut(BaseModel):
   
    id: int
    name: str
    email: str
    role: str
    is_active: bool