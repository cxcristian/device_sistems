from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session
from app.services import user_services as us
from app.database import get_db


def get_user_or_404(user_id: int, db: Session = Depends(get_db)):
    return us.get_user_by_id(db, user_id)


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "contraseña":
        raise HTTPException(403, detail="API Key inválida. Usa 'contraseña'")
    return x_api_key
