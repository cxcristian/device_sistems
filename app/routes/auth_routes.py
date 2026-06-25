from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.schemas.user_schema import UserOut
from app.services import auth_service
from app.dependencies.rate_limit import limiter
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
@limiter.limit("3/minute")
def register(request: Request, user: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user.email, user.password)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user