from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.database import create_tables

create_tables()

app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios, dispositivos y préstamos del sistema device_systems",
    version="2.0.0",
    contact={
        "name": "Tu nombre",
        "email": "dev@device-sistems.co",
    }
)

@app.middleware("http")
async def custom_header(request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    response.headers["X-API-Institution"] = "Sena CTMA"
    return response

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)