from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import UserCreate, UserOut, UserUpdate, UserDelete
from app.services import user_services as us

router = APIRouter(tags=["users"])


@router.get(
    "/users",
    response_model=list[UserOut],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios. Opcionalmente filtra por rol y estado activo.",
    response_description="Lista de usuarios encontrados",
)
def list_users(role: str | None = Query(None), is_active: bool | None = Query(None)):
    return us.get_users(role, is_active)


@router.get(
    "/users/{user_id}",
    response_model=UserOut,
    summary="Obtener usuario por ID",
    description="Busca un usuario por su ID único.",
    response_description="Usuario encontrado",
)
def get_user(user_id: int):
    return us.get_user_by_id(user_id)


@router.post(
    "/users",
    response_model=UserOut,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario con los datos proporcionados. El email debe ser único.",
    response_description="Usuario creado exitosamente",
)
def create_user(user: UserCreate):
    return us.create_user(user)


@router.put(
    "/users/{user_id}",
    response_model=UserOut,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado exitosamente",
)
def update_user(user_id: int, user: UserCreate):
    return us.update_user(user_id, user)


@router.patch(
    "/users/{user_id}",
    response_model=UserOut,
    summary="Actualizar usuario parcial",
    description="Actualiza solo los campos enviados de un usuario existente.",
    response_description="Usuario actualizado exitosamente",
)
def patch_user(user_id: int, user: UserUpdate):
    return us.patch_user(user_id, user)


@router.delete(
    "/users/{user_id}",
    response_model=UserDelete,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema por su ID.",
    response_description="Usuario eliminado exitosamente",
)
def delete_user(user_id: int):
    return us.delete_user(user_id)
