# Device Systems API — Guía de implementación

Guía paso a paso para construir una API REST de usuarios con **FastAPI**, **Pydantic v2** y **Uvicorn**.

---

## Estructura final del proyecto

```
device_systems/
├── app/
│   ├── main.py                    # Punto de entrada de la app
│   ├── schema/
│   │   └── user_schema.py         # Modelos Pydantic (validación de datos)
│   └── routes/
│       └── user_routes.py         # Endpoints (GET / POST)
├── .venv/                         # Entorno virtual (creado por uv)
├── pyproject.toml                 # Dependencias del proyecto
├── uv.lock                        # Lock file (versiones exactas)
└── README.md
```

---

## Fase 1 — Crear la app base

### `app/main.py`

Punto de entrada. Crea la instancia de FastAPI, define un middleware para agregar cabeceras personalizadas y conecta las rutas.

```python
from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(title="Device Systems API", version="1.0")

# Middleware: agrega cabeceras personalizadas a TODAS las respuestas
@app.middleware("http")
async def add_custom_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return response

# Conecta las rutas de usuarios
app.include_router(user_router, tags=["users"])
```

**Explicación:**
- `FastAPI()` crea la aplicación.
- `@app.middleware("http")` es un hook que se ejecuta en cada petición. `call_next` procesa la request y devuelve la response. Ahí inyectamos las cabeceras `X-App-Name` y `X-API-Version`.
- `app.include_router()` importa las rutas definidas en otro archivo.

---

## Fase 2 — Modelo de usuario con Pydantic

### `app/schema/user_schema.py`

Define los modelos de datos con validaciones. Pydantic v2 usa validadores de tipo y `field_validator` para lógica personalizada.

```python
import re
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class UserBase(BaseModel):
    """Campos base del usuario (compartidos entre creación y respuesta)."""
    name: str = Field(..., min_length=3)
    email: str
    role: Literal["admin", "support", "user"]
    is_active: bool = True

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError("El email no tiene un formato válido")
        return v


class UserCreate(UserBase):
    """Usado para el cuerpo de la petición POST (sin id)."""
    pass


class UserOut(BaseModel):
    """Usado para las respuestas GET/POST (con id). Oculta datos internos."""
    id: int
    name: str
    email: str
    role: str
    is_active: bool
```

**Explicación:**
- `Field(..., min_length=3)` — `...` significa obligatorio. `min_length` valida longitud mínima automáticamente.
- `Literal["admin", "support", "user"]` — restringe el valor a exactamente esos strings.
- `field_validator("email")` — valida el formato del email con una expresión regular. Se ejecuta automáticamente al crear una instancia del modelo.
- `UserCreate` hereda de `UserBase`, no agrega nada nuevo. Se usa para diferenciar semánticamente entrada vs salida.
- `UserOut` es un modelo separado que incluye `id` y NO hereda de `UserBase`, para no exponer campos internos.

---

## Fase 3 y 4 — Endpoints GET y POST

### `app/routes/user_routes.py`

Define los endpoints REST. Usa una lista en memoria como base de datos.

```python
from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import UserCreate, UserOut

router = APIRouter()

# "Base de datos" en memoria
users_db: list[dict] = []
next_id = 1


@router.get("/users", response_model=list[UserOut])
def list_users(
    role: str | None = Query(None),
    is_active: bool | None = Query(None),
):
    """
    GET /users — Lista todos los usuarios.
    GET /users?role=admin — Filtra por rol.
    GET /users?is_active=true — Filtra por estado activo/inactivo.
    """
    results = users_db
    if role is not None:
        results = [u for u in results if u["role"] == role]
    if is_active is not None:
        results = [u for u in results if u["is_active"] == is_active]
    return results


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """GET /users/{user_id} — Obtiene un usuario por ID."""
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate):
    """POST /users — Crea un nuevo usuario."""
    global next_id

    # Validar email duplicado
    for existing in users_db:
        if existing["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail=f"El email {user.email} ya está registrado",
            )

    new_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    users_db.append(new_user)
    next_id += 1
    return new_user
```

**Explicación:**
- `APIRouter()` permite agrupar rutas en un módulo separado y luego importarlas en `main.py` con `include_router()`.
- `Query(None)` hace que el parámetro sea opcional. Si no se envía, vale `None` y no filtra.
- `response_model=list[UserOut]` — FastAPI usa este tipo para serializar la respuesta y documentar el schema en Swagger.
- `HTTPException` — lanza un error HTTP con el código y mensaje que elijas.
- La validación duplicado recorre la lista comparando emails.

---

## Fase 5 — Response Models y cabeceras

Ya está implementado en las fases anteriores:

| Concepto | Dónde se implementa |
|---|---|
| `response_model=UserOut` | En cada endpoint (`app/routes/user_routes.py`) |
| Cabeceras `X-App-Name` y `X-API-Version` | Middleware en `app/main.py` |
| Ocultar datos no necesarios | `UserOut` solo expone `id`, `name`, `email`, `role`, `is_active` |

**¿Por qué `UserOut` separado de `UserCreate`?**
- `UserCreate` tiene validaciones de entrada (`min_length`, email, roles).
- `UserOut` podría no necesitar ciertos campos internos (como contraseñas, etc.).
- Si el modelo de datos cambia, los cambios en input y output son independientes.

---

## Cómo ejecutar

```bash
uv run uvicorn app.main:app --reload
```

- `uv run` — ejecuta dentro del entorno virtual sin necesidad de activarlo.
- `--reload` — reinicia el servidor automáticamente al detectar cambios en el código.

Servidor en: http://127.0.0.1:8000

Documentación automática:
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Ejemplos de prueba con curl

```bash
# Crear usuario
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Juan Perez\",\"email\":\"juan@example.com\",\"role\":\"admin\",\"is_active\":true}"

# Listar todos
curl http://127.0.0.1:8000/users

# Filtrar por rol
curl "http://127.0.0.1:8000/users?role=admin"

# Obtener por ID
curl http://127.0.0.1:8000/users/1

# Ver cabeceras personalizadas
curl -I http://127.0.0.1:8000/users
```
