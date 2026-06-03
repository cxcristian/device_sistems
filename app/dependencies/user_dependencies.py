from fastapi import HTTPException, Header
from app.services import user_services as us


def get_user_or_404(user_id: int):
    return us.get_user_by_id(user_id)


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "contraseña":
        raise HTTPException(403, detail="API Key inválida. Usa 'contraseña'")
    return x_api_key
