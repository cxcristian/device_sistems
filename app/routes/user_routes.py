from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import UserCreate, UserOut

router = APIRouter()

users_db: list[dict] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user", "is_active": True},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "support", "is_active": False},
    {"id": 4, "name": "Diana", "email": "diana@example.com", "role": "user", "is_active": True},
    {"id": 5, "name": "Eve", "email": "eve@example.com", "role": "admin", "is_active": False},
]
next_id = 6


@router.get("/users", response_model=list[UserOut])
def list_users(role: str | None = Query(None), is_active: bool | None =Query(None)):
    result = users_db
    if role:
        result = [u for u in result if u ["role"] == role]
    if is_active is not None: result = [u for u in result if u ["is_active"] == is_active]
    return result


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate):
    global next_id

    
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