from fastapi import APIRouter, Query, Depends, Request
from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanDetailResponse,
)
from app.services import loan_service as ls
from app.dependencies.user_dependencies import verify_api_key
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependency import(get_current_active_user, require_admin, require_admin_or_support)
from app.dependencies.rate_limit import limiter
from app.models.user_model import User

router = APIRouter(tags=["Loans"], dependencies=[Depends(verify_api_key), Depends(get_current_active_user)])


@router.get(
    "/loans",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Obtiene todos los préstamos. Filtra por estado, email de usuario o tipo de dispositivo.",
    response_description="Lista de préstamos encontrados",
)
def list_loans(
    db: Session = Depends(get_db),
    status: str | None = Query(None),
    user_email: str | None = Query(None),
    device_type: str | None = Query(None),

):
    return ls.get_loans(db, status, user_email, device_type)


@router.get(
    "/loans/details",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con detalles",
    description="Obtiene todos los préstamos con información del usuario y del dispositivo.",
    response_description="Lista de préstamos con detalles",
    
)
def loan_details(db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_support)):
    return ls.get_loan_details(db)


@router.get(
    "/loans/{loan_id}",
    response_model=LoanResponse,
    summary="Obtener préstamo por ID",
    description="Busca un préstamo por su ID único.",
    response_description="Préstamo encontrado",
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    return ls.get_loan_by_id(db, loan_id)


@router.post(
    "/loans",
    response_model=LoanResponse,
    status_code=201,
    summary="Crear préstamo",
    description="Crea un nuevo préstamo. Valida que el usuario y dispositivo existan, y que el dispositivo esté disponible.",
    response_description="Préstamo creado exitosamente",
)
@limiter.limit("10/minute")
def create_loan(request: Request, loan: LoanCreate, db: Session = Depends(get_db)):
    return ls.create_loan(db, loan)


@router.patch(
    "/loans/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Marca el préstamo como devuelto, asigna fecha de devolución y cambia el dispositivo a disponible.",
    response_description="Dispositivo devuelto exitosamente",
)
def return_loan(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_support)):
    return ls.return_loan(db, loan_id)


@router.get(
    "/users/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Préstamos de un usuario",
    description="Obtiene todos los préstamos de un usuario específico.",
    response_description="Lista de préstamos del usuario",
)
def user_loans(user_id: int, db: Session = Depends(get_db)):
    return ls.get_loans_by_user(db, user_id)


@router.get(
    "/devices/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Obtiene todo el historial de préstamos de un dispositivo específico.",
    response_description="Historial de préstamos del dispositivo",
)
def device_loans(device_id: int, db: Session = Depends(get_db)):
    return ls.get_loans_by_device(db, device_id)
