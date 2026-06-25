from fastapi import APIRouter, Query, Depends, Security
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service as ds
from app.dependencies.auth_dependency import (
    security,
    get_current_active_user,
    require_admin,
    require_admin_or_support,)  
from app.dependencies.user_dependencies import verify_api_key
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
    dependencies=[Security(security), Depends(get_current_active_user), Depends(verify_api_key)],
)


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Obtiene todos los dispositivos. Filtra por tipo, disponibilidad, marca o búsqueda textual.",
    response_description="Lista de dispositivos encontrados",
)
def list_devices(
    db: Session = Depends(get_db),
    device_type: str | None = Query(None),
    is_available: bool | None = Query(None),
    brand: str | None = Query(None),
    search: str | None = Query(None),
):
    return ds.get_devices(db, device_type, is_available, brand, search)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID",
    description="Busca un dispositivo por su ID único.",
    response_description="Dispositivo encontrado",
)
def get_device(device_id: int, db: Session = Depends(get_db)):
    return ds.get_device_by_id(db, device_id)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=201,
    summary="Crear dispositivo",
    description="Crea un nuevo dispositivo. El número de serie debe ser único.",
    response_description="Dispositivo creado exitosamente",
)
def create_device(device: DeviceCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_support)):
    return ds.create_device(db, device)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo",
    description="Reemplaza todos los datos de un dispositivo existente.",
    response_description="Dispositivo actualizado exitosamente",
)
def update_device(device_id: int, device: DeviceCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_support)):
    return ds.update_device(db, device_id, device)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcial",
    description="Actualiza solo los campos enviados de un dispositivo existente.",
    response_description="Dispositivo actualizado exitosamente",
)
def patch_device(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db),current_user: User = Depends(require_admin_or_support)):
    return ds.patch_device(db, device_id, device)


@router.delete(
    "/{device_id}",
    status_code=204,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo del sistema por su ID.",
    response_description="Dispositivo eliminado exitosamente",
)
def delete_device(device_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    ds.delete_device(db, device_id)
