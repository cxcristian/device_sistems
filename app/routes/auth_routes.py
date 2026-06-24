from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.schemas.user_schema import UserOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/register", response_model=UserOut, status_code=201)
def register(user: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user)
@router.get("/me", response_model=UserOut)
def get_me(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.split("Bearer ")[-1]
    return auth_service.get_current_user(db, token)