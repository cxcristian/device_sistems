from app.data.users_db import users_db, get_next_id
from fastapi import  HTTPException, Query
from app.schema.user_schema import UserCreate, UserUpdate, UserDelete
def get_users(role=None, is_active=None):
    result = users_db
    if role:
        result = [u for u in result if u ["role"] == role]
    if is_active is not None: result = [u for u in result if u ["is_active"] == is_active]
    return result

def get_user_by_id(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

def create_user(user: UserCreate):
    for existing in users_db:
        if existing["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail=f"El email {user.email} ya está registrado",
            )
    new_user = {
        "id": get_next_id(),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    users_db.append(new_user)
    
    return new_user


def update_user(user_id: int, user: UserCreate):
    
    for i, existing in enumerate(users_db):
        
        if existing["id"] == user_id:
    
            users_db[i] = {
                "id": user_id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            }
            return users_db[i]
    raise HTTPException(404, detail="usuario no encontrado")

def patch_user(user_id: int, user: UserUpdate):
    data = user.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(400, detail="Debe enviar al menos un campo para actualizar")
    for i, existing in enumerate(users_db):
        if existing["id"] == user_id:
            for key, value in data.items():
                existing[key] = value
            return existing
    raise HTTPException(404, detail="Usuario no encontrado")

def delete_user(user_id: int):
    for i, existing in enumerate(users_db):
        if existing["id"] == user_id:
            users_db.pop(i)
            return {"detail": "Usuario eliminado"}
    raise HTTPException(404, detail="Usuario no encontrado")
