from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, EmailStr
import re
from typing import Optional, Literal
class UserRegister(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["admin", "support", "user"] = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Mínimo 8 caracteres")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Debe contener al menos una mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("Debe contener al menos una minúscula")
        if not re.search(r"\d", value):
            raise ValueError("Debe contener al menos un número")
        if " " in value:
            raise ValueError("No debe contener espacios")
        return value
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    user_id: int | None = None
    role: Literal["admin", "support", "user"] | None = None