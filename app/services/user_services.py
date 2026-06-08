from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schema.user_schema import UserCreate, UserUpdate
from app.models.user_model import User


def get_users(db: Session, role=None, is_active=None):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


def create_user(db: Session, user: UserCreate):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"El email {user.email} ya está registrado",
        )
    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, detail="Usuario no encontrado")
    db_user.name = user.name
    db_user.email = user.email
    db_user.role = user.role
    db_user.is_active = user.is_active
    db.commit()
    db.refresh(db_user)
    return db_user



def patch_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, detail="Usuario no encontrado")
    data = user.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(400, detail="Debe enviar al menos un campo para actualizar")
    for key, value in data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    return {"detail": "Usuario eliminado"}
