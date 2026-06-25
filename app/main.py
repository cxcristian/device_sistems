from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.routes.auth_routes import router as auth_router
from app.database import create_tables
from app.middleware.request_middleware import RequestLogMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.dependencies.rate_limit import limiter

create_tables()

app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios, dispositivos y préstamos del sistema device_systems",
    version="2.0.0",
    contact={
        "name": "Cris 3114227",
        "email": "dev@device-sistems.co",
    }
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(RequestLogMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(auth_router)