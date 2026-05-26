from fastapi import FastAPI
from app.routes.user_routes import router as ur

app = FastAPI(title="Device Systems API", version="1.0")


@app.middleware("http")
async def custom_header(request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return response


#Aqui importamos las rutas definidas en user_routes.py
app.include_router(ur, tags=["users"])