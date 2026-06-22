from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def get_devices(
    db: Session,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
            )
        )
    return query.all()


def get_device_by_id(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    return device


def create_device(db: Session, device: DeviceCreate):
    existing = (
        db.query(Device)
        .filter(Device.serial_number == device.serial_number)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El número de serie {device.serial_number} ya está registrado",
        )
    new_device = Device(
        name=device.name,
        serial_number=device.serial_number,
        device_type=device.device_type,
        brand=device.brand,
        is_available=device.is_available,
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


def update_device(db: Session, device_id: int, device: DeviceCreate):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    if device.serial_number != db_device.serial_number:
        existing = (
            db.query(Device)
            .filter(Device.serial_number == device.serial_number)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El número de serie {device.serial_number} ya está registrado",
            )
    db_device.name = device.name
    db_device.serial_number = device.serial_number
    db_device.device_type = device.device_type
    db_device.brand = device.brand
    db_device.is_available = device.is_available
    db.commit()
    db.refresh(db_device)
    return db_device


def patch_device(db: Session, device_id: int, device: DeviceUpdate):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    data = device.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar",
        )
    if "serial_number" in data and data["serial_number"] != db_device.serial_number:
        existing = (
            db.query(Device)
            .filter(Device.serial_number == data["serial_number"])
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El número de serie {data['serial_number']} ya está registrado",
            )
    for key, value in data.items():
        setattr(db_device, key, value)
    db.commit()
    db.refresh(db_device)
    return db_device


def delete_device(db: Session, device_id: int):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    db.delete(db_device)
    db.commit()
    return {"detail": "Dispositivo eliminado"}
