from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.auth.security import get_password_hash, verify_password, create_access_token

def register_user(db: Session, user: UserRegister):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(400, detail="Email ya registrado")
    
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, email: str, password: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(401, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(db: Session, token: str):
    from app.auth.security import decode_access_token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(401, detail="Token inválido o expirado")
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(404, detail="Usuario no encontrado")
    return user