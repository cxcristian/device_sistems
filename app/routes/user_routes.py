from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import UserCreate, UserOut

router = APIRouter()

users_db: list[dict] = []
next_id = 1


@router.get("/users", response_model=list[UserOut])
def list_users():
    return users_db


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate):
    global next_id

    # Validar email duplicado
    for existing in users_db:
        if existing["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail=f"El email {user.email} ya está registrado",
            )
    new_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    users_db.append(new_user)
    next_id += 1
    return new_user