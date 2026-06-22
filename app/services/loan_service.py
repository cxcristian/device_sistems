from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from datetime import datetime
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


def get_loans(
    db: Session,
    status_filter: str | None = None,
    user_email: str | None = None,
    device_type: str | None = None,
):
    query = db.query(Loan)
    if status_filter:
        query = query.filter(Loan.status == status_filter)
    if user_email:
        query = query.join(User).filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.join(Device).filter(Device.device_type == device_type)
    return query.all()


def get_loan_by_id(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado",
        )
    return loan


def create_loan(db: Session, loan: LoanCreate):
    user = db.query(User).filter(User.id == loan.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )

    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El dispositivo '{device.name}' no está disponible actualmente",
        )

    new_loan = Loan(
        user_id=loan.user_id,
        device_id=loan.device_id,
        status="active",
    )
    device.is_available = False
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan


def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado",
        )

    if loan.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo ya fue devuelto anteriormente",
        )

    loan.status = "returned"
    loan.return_date = datetime.now()

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan


def _build_loan_detail(loan):
    return {
        "loan_id": loan.id,
        "status": loan.status,
        "loan_date": loan.loan_date,
        "return_date": loan.return_date,
        "user": {
            "id": loan.user.id,
            "name": loan.user.name,
            "email": loan.user.email,
        },
        "device": {
            "id": loan.device.id,
            "name": loan.device.name,
            "serial_number": loan.device.serial_number,
            "device_type": loan.device.device_type,
        },
    }


def get_loan_details(db: Session):
    loans = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .all()
    )
    return [_build_loan_detail(loan) for loan in loans]


def get_loans_by_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    loans = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.user_id == user_id)
        .all()
    )
    return [_build_loan_detail(loan) for loan in loans]


def get_loans_by_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    loans = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.device_id == device_id)
        .all()
    )
    return [_build_loan_detail(loan) for loan in loans]
