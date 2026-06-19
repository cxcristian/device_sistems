from fastapi import APIRouter, HTTPException, Query, Depends
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate, UserDelete
from app.services import user_services as us
from app.dependencies.user_dependencies import get_user_or_404, verify_api_key
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(tags=["users"], dependencies=[Depends(verify_api_key)])


@router.get(
    "/users",
    response_model=list[UserOut],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios. Opcionalmente filtra por rol y estado activo.",
    response_description="Lista de usuarios encontrados",
)
def list_users(db: Session = Depends(get_db), role: str | None = Query(None), is_active: bool | None = Query(None)):
    return us.get_users(db,role, is_active)


@router.get(
    "/users/{user_id}",
    response_model=UserOut,
    summary="Obtener usuario por ID",
    description="Busca un usuario por su ID único.",
    response_description="Usuario encontrado",
)
def get_user(user: dict = Depends(get_user_or_404)):
    return user


@router.post(
    "/users",
    response_model=UserOut,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario con los datos proporcionados. El email debe ser único.",
    response_description="Usuario creado exitosamente",
)
def create_user(user: UserCreate, db: Session = Depends(get_db) ):
    return us.create_user(db, user)

@router.put(
    "/users/{user_id}",
    response_model=UserOut,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado exitosamente",
)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return us.update_user(db ,user_id, user)


@router.patch(
    "/users/{user_id}",
    response_model=UserOut,
    summary="Actualizar usuario parcial",
    description="Actualiza solo los campos enviados de un usuario existente.",
    response_description="Usuario actualizado exitosamente",
)
def patch_user(user_id: int, user: UserUpdate ,db: Session = Depends(get_db), ):
    return us.patch_user(db, user_id, user)


@router.delete(
    "/users/{user_id}",
    response_model=UserDelete,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema por su ID.",
    response_description="Usuario eliminado exitosamente",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return us.delete_user(db, user_id)
