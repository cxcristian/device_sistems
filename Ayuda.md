# Reto Integrador – Usuarios, Dispositivos y Préstamos con FastAPI, SQLAlchemy y Alembic

## Objetivo del reto

Evolucionar la API REST **device_systems** para gestionar usuarios, dispositivos y préstamos, aplicando relaciones entre modelos, migraciones de base de datos y consultas con joins.

La API debe permitir:

- Crear usuarios.
- Crear dispositivos.
- Asociar dispositivos a usuarios mediante préstamos.
- Consultar dispositivos asignados a un usuario.
- Consultar préstamos registrados.
- Filtrar préstamos por usuario, dispositivo, estado o fecha.
- Realizar búsquedas usando filtros avanzados.
- Aplicar migraciones de base de datos con Alembic.
- Documentar la API mediante Swagger/OpenAPI.

---

## Relación de temas aplicados

| Tema | Aplicación en el proyecto |
|---|---|
| Alembic para migraciones | Versionar cambios estructurales de la base de datos y aplicar migraciones de forma controlada |
| Asociaciones de modelos | Relacionar `User`, `Device` y `Loan` usando `ForeignKey()` y `relationship()` |
| One-to-Many y Many-to-One | Un usuario puede tener muchos préstamos; un dispositivo puede estar asociado a varios registros históricos de préstamo |
| Consultas con joins | Consultar usuarios con dispositivos prestados y préstamos con información relacionada |
| Filtros avanzados | Buscar por nombre, correo, tipo de dispositivo, estado del préstamo o disponibilidad |
| Integridad referencial | Garantizar que un préstamo siempre pertenezca a un usuario y a un dispositivo existente |

---

## Estructura del proyecto

```
device_systems/
│── app/
│ │── main.py
│ │
│ │── auth/
│ │ │── auth_routes.py
│ │ │── auth_service.py
│ │ │── security.py
│ │
│ │── database/
│ │ │── __init__.py
│ │ │── connection.py
│ │
│ │── models/
│ │ │── __init__.py
│ │ │── user_model.py
│ │ │── device_model.py
│ │ │── loan_model.py
│ │
│ │── schemas/
│ │ │── user_schema.py
│ │ │── device_schema.py
│ │ │── loan_schema.py
│ │ │── auth_schema.py
│ │
│ │── routes/
│ │ │── user_routes.py
│ │ │── device_routes.py
│ │ │── loan_routes.py
│ │
│ │── services/
│ │ │── user_service.py
│ │ │── device_service.py
│ │ │── loan_service.py
│ │
│ │── dependencies/
│ │ │── user_dependencies.py
│
│── alembic/
│ │── versions/
│ │── env.py
│ │── script.py.mako
│ │── README
│
│── alembic.ini
│── requirements.txt
│── pyproject.toml
│── uv.lock
│── README.md
```

---

## Fase 1 – Retomar el proyecto anterior

Partir del proyecto **device_systems** con:

- [x] FastAPI configurado.
- [x] SQLAlchemy conectado a base de datos.
- [x] Modelo `User`.
- [x] Schemas Pydantic.
- [x] CRUD completo de usuarios.
- [x] Manejo de errores.
- [x] Swagger/OpenAPI funcional.

En esta nueva versión se debe **conservar el recurso `users`** y ampliar el sistema con los recursos `devices` y `loans`.

---

## Fase 2 – Actualizar la estructura del proyecto

La estructura del proyecto se actualizó a la mostrada arriba. Cada módulo tiene su responsabilidad bien definida.

---

## Fase 3 – Instalar y configurar Alembic

### 3.1 Instalar Alembic

Con `pip`:
```bash
pip install alembic
```

Con `uv` (recomendado para este proyecto):
```bash
uv add alembic
```

Agregarlo al archivo `requirements.txt`:
```bash
uv export --format requirements-txt -o requirements.txt
```

### 3.2 Inicializar Alembic

```bash
alembic init alembic
```

Con `uv`:
```bash
uv run alembic init alembic
```

Esto genera:
- `alembic.ini` → archivo de configuración principal.
- `alembic/env.py` → script de entorno para las migraciones.
- `alembic/script.py.mako` → template para los archivos de migración.
- `alembic/versions/` → directorio donde se almacenan las migraciones.
- `alembic/README` → instrucciones básicas.

### 3.3 Configurar Alembic

**`alembic.ini`** — línea 89, cambiar la URL de conexión:
```ini
sqlalchemy.url = sqlite:///./device_systems.db
```

**`alembic/env.py`** — agregar imports y configurar metadata:

```python
# Después de fileConfig(...)
from app.database import Base
from app.models import user_model, device_model, loan_model

# Cambiar target_metadata
target_metadata = Base.metadata
```

> **⚠️ Importante:** `Base.metadata` contiene las tablas de todos los modelos que se hayan importado antes de acceder a él. Por eso es necesario importar `user_model`, `device_model` y `loan_model` explícitamente.

> **💡 Sugerencia:** Si tienes problemas con `ModuleNotFoundError: No module named 'app'`, agrega lo siguiente al inicio de `env.py`:
> ```python
> import sys
> from pathlib import Path
> sys.path.append(str(Path(__file__).resolve().parents[1]))
> ```

### 3.4 Generar migración

```bash
alembic revision --autogenerate -m "create devices and loans tables"
```

Con `uv`:
```bash
uv run alembic revision --autogenerate -m "create devices and loans tables"
```

Esto crea un archivo en `alembic/versions/` con el nombre `{hash}_create_devices_and_loans_tables.py`.

### 3.5 Aplicar la migración

```bash
alembic upgrade head
```

Con `uv`:
```bash
uv run alembic upgrade head
```

### 3.6 Consultar historial de migraciones

```bash
alembic history
```

Con `uv`:
```bash
uv run alembic history
```

**Salida esperada:**
```
<hash> -> <hash> (head), create devices and loans tables
```

### 3.7 Ver el estado actual

```bash
alembic current
```

Muestra qué migración está aplicada actualmente en la base de datos.

### 3.8 Revertir una migración (si es necesario)

```bash
alembic downgrade -1   # retrocede 1 versión
alembic downgrade <hash>  # retrocede a una versión específica
```

---

## Fase 4 – Crear el modelo Device

**Archivo:** `app/models/device_model.py`

El modelo `Device` representa los equipos tecnológicos disponibles para préstamo.

| Campo | Tipo | Restricción |
|---|---|---|
| `id` | Integer | Primary Key |
| `name` | String | Obligatorio |
| `serial_number` | String | Único y obligatorio |
| `device_type` | String | Obligatorio |
| `brand` | String | Opcional |
| `is_available` | Boolean | Valor por defecto `True` |
| `created_at` | DateTime | Fecha de creación |

**Ejemplo del modelo:**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False, index=True)
    device_type = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
```

**Ejemplos de tipos de dispositivo:**
- `laptop`
- `tablet`
- `proyector`
- `cámara`
- `router`
- `monitor`

---

## Fase 5 – Crear el modelo Loan

**Archivo:** `app/models/loan_model.py`

El modelo `Loan` representa el préstamo de un dispositivo a un usuario.

| Campo | Tipo | Restricción |
|---|---|---|
| `id` | Integer | Primary Key |
| `user_id` | Integer | Foreign Key a `users.id` |
| `device_id` | Integer | Foreign Key a `devices.id` |
| `loan_date` | DateTime | Fecha de préstamo |
| `return_date` | DateTime | Opcional |
| `status` | String | Obligatorio |

**Estados sugeridos:**
- `active` — préstamo activo
- `returned` — dispositivo devuelto
- `overdue` — préstamo vencido

**Ejemplo del modelo:**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    loan_date = Column(DateTime, server_default=func.now())
    return_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="active")

    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")
```

---

## Fase 6 – Definir asociaciones entre modelos

### Relaciones esperadas

**User ↔ Loan** (One-to-Many):
```python
# En user_model.py
loans = relationship("Loan", back_populates="user")

# En loan_model.py
user = relationship("User", back_populates="loans")
```

**Device ↔ Loan** (One-to-Many):
```python
# En device_model.py
loans = relationship("Loan", back_populates="device")

# En loan_model.py
device = relationship("Device", back_populates="loans")
```

### Modelo User actualizado

Agregar la relación `loans` al modelo `User`:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relación con préstamos
    loans = relationship("Loan", back_populates="user")
```

> **💡 Sugerencia:** Usa `back_populates` en lugar de `backref`. Aunque `backref` es más corto, `back_populates` hace las relaciones explícitas en ambos modelos, lo que mejora la legibilidad y el mantenimiento.

---

## Fase 7 – Crear schemas Pydantic

### dispositivos (`app/schemas/device_schema.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class DeviceBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    serial_number: str = Field(min_length=3, max_length=50)
    device_type: Literal["laptop", "tablet", "proyector", "cámara", "router", "monitor"]
    brand: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    serial_number: Optional[str] = Field(default=None, min_length=3, max_length=50)
    device_type: Optional[Literal["laptop", "tablet", "proyector", "cámara", "router", "monitor"]] = None

class DeviceResponse(DeviceBase):
    id: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

### préstamos (`app/schemas/loan_schema.py`)

Incluir schemas anidados para mostrar información relacionada:

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class DeviceBasic(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    class Config:
        from_attributes = True

class LoanCreate(BaseModel):
    user_id: int
    device_id: int

class LoanUpdate(BaseModel):
    status: Optional[str] = None

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True

class LoanDetailResponse(BaseModel):
    id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]
    user: UserBasic
    device: DeviceBasic

    class Config:
        from_attributes = True
```

> **💡 Sugerencia:** Los schemas anidados (`UserBasic`, `DeviceBasic`) evitan exponer campos sensibles o irrelevantes dentro de la respuesta de un préstamo.

---

## Fase 8 – Implementar CRUD de dispositivos

### Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/devices` | Listar dispositivos (con filtros) |
| `GET` | `/devices/{device_id}` | Obtener dispositivo por ID |
| `POST` | `/devices` | Crear dispositivo |
| `PUT` | `/devices/{device_id}` | Actualizar dispositivo completo |
| `PATCH` | `/devices/{device_id}` | Actualizar dispositivo parcial |
| `DELETE` | `/devices/{device_id}` | Eliminar dispositivo |

### Filtros disponibles

```bash
GET /devices?device_type=laptop
GET /devices?is_available=true
GET /devices?brand=lenovo
GET /devices?search=thinkpad
```

### Ejemplo de servicio con filtros

```python
def get_devices(db: Session, device_type=None, is_available=None, brand=None, search=None):
    query = db.query(Device)

    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            Device.name.ilike(f"%{search}%") |
            Device.serial_number.ilike(f"%{search}%") |
            Device.brand.ilike(f"%{search}%")
        )

    return query.all()
```

---

## Fase 9 – Implementar gestión de préstamos

### Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/loans` | Listar préstamos |
| `GET` | `/loans/{loan_id}` | Obtener préstamo por ID |
| `POST` | `/loans` | Crear préstamo |
| `PATCH` | `/loans/{loan_id}/return` | Devolver dispositivo |

### Reglas de negocio: `POST /loans`

1. Validar que el usuario exista.
2. Validar que el dispositivo exista.
3. Validar que el dispositivo esté disponible (`is_available == True`).
4. Crear el préstamo con estado `active`.
5. Cambiar `is_available` del dispositivo a `False`.

```python
def create_loan(db: Session, loan_data: LoanCreate):
    user = db.query(User).filter(User.id == loan_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not device.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no está disponible")

    new_loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active"
    )
    device.is_available = False

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan
```

### Reglas de negocio: `PATCH /loans/{loan_id}/return`

1. Validar que el préstamo exista.
2. Validar que el préstamo esté `active` (no devuelto ya).
3. Marcar el préstamo como `returned`.
4. Asignar fecha de devolución (`return_date = now()`).
5. Cambiar `is_available` del dispositivo a `True`.

```python
def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="El préstamo ya fue devuelto")

    loan.status = "returned"
    loan.return_date = datetime.now()

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan
```

---

## Fase 10 – Implementar consultas con joins y filtros

### Endpoints sugeridos

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/loans/details` | Todos los préstamos con info de usuario y dispositivo |
| `GET` | `/users/{user_id}/loans` | Préstamos de un usuario específico |
| `GET` | `/devices/{device_id}/loans` | Historial de préstamos de un dispositivo |
| `GET` | `/loans?status=active` | Filtrar préstamos por estado |
| `GET` | `/loans?user_email=...` | Filtrar préstamos por email del usuario |
| `GET` | `/loans?device_type=laptop` | Filtrar préstamos por tipo de dispositivo |

### Ejemplo de consulta con joins

```python
def get_loans_with_details(db: Session, status=None, user_email=None, device_type=None):
    query = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
    )

    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type == device_type)

    return query.all()
```

### Ejemplo de respuesta JSON

```json
{
    "loan_id": 1,
    "status": "active",
    "loan_date": "2026-06-18T10:00:00",
    "return_date": null,
    "user": {
        "id": 1,
        "name": "Ana Pérez",
        "email": "ana@sena.edu.co"
    },
    "device": {
        "id": 3,
        "name": "Laptop Lenovo ThinkPad",
        "serial_number": "LEN-2024-001",
        "device_type": "laptop"
    }
}
```

### Funciones de SQLAlchemy utilizadas

| Función | Uso |
|---|---|
| `join()` | Combinar tablas por FK |
| `where()` / `filter()` | Condiciones de búsqueda |
| `like()` / `ilike()` | Búsqueda parcial (insensible a mayúsculas) |
| `and_()` / `or_()` | Condiciones múltiples |
| `in_()` | Filtrar por lista de valores |

---

## Fase 11 – Manejo de errores

### Códigos de respuesta

| Caso | Código |
|---|---|
| Registro creado | `201 Created` |
| Consulta exitosa | `200 OK` |
| Devolución exitosa | `200 OK` |
| Eliminación exitosa | `204 No Content` |
| Recurso no encontrado | `404 Not Found` |
| Dato duplicado | `400 Bad Request` |
| Regla de negocio incumplida | `409 Conflict` |
| Error de validación | `422 Unprocessable Entity` |

### Casos manejados

- Usuario inexistente.
- Dispositivo inexistente.
- Dispositivo no disponible.
- Préstamo inexistente.
- Intento de devolver un préstamo ya devuelto.
- Número de serie duplicado.
- Filtros inválidos.
- Error al aplicar migraciones.

---

## Fase 12 – Documentación Swagger/OpenAPI

La documentación automática está organizada por **tags**:

- **Users** — endpoints de usuarios
- **Devices** — endpoints de dispositivos
- **Loans** — endpoints de préstamos

Cada endpoint incluye:
- `summary` — resumen breve
- `description` — descripción detallada
- `response_description` — descripción de la respuesta
- Códigos de respuesta esperados
- Ejemplos en schemas Pydantic (con `json_schema_extra` o `Field(example=...)`)

### Acceso

| URL | Descripción |
|---|---|
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |

---

## Fase 13 – Pruebas funcionales mínimas

Escenarios a probar y documentar:

1. [ ] Ejecutar migraciones con Alembic.
2. [ ] Crear usuario.
3. [ ] Crear dispositivo.
4. [ ] Crear préstamo.
5. [ ] Intentar prestar un dispositivo no disponible.
6. [ ] Listar préstamos con información de usuario y dispositivo.
7. [ ] Filtrar préstamos por estado.
8. [ ] Filtrar préstamos por tipo de dispositivo.
9. [ ] Consultar préstamos de un usuario.
10. [ ] Devolver un dispositivo.
11. [ ] Validar que el dispositivo vuelva a estar disponible.
12. [ ] Consultar historial de préstamos del dispositivo.

---

## Ambiente requerido

- Computador con Python 3.10+ instalado.
- Visual Studio Code o editor similar.
- FastAPI.
- Uvicorn.
- SQLAlchemy.
- Alembic.
- Pydantic v2.
- SQLite.
- Git y GitHub.
- Postman o Thunder Client (para pruebas de API).

---

## Evidencias de aprendizaje

### Repositorio individual en GitHub con:

- [ ] Proyecto **device_systems** actualizado.
- [ ] Rama `device_systems_alembic_relaciones` unificada con `main`.
- [ ] Configuración de Alembic.
- [ ] Carpeta `alembic/versions/` con migraciones generadas.
- [ ] Modelos `User`, `Device` y `Loan`.
- [ ] Asociaciones entre modelos.
- [ ] Schemas Pydantic.
- [ ] CRUD de usuarios y dispositivos.
- [ ] Gestión de préstamos.
- [ ] Consultas con joins y filtros.
- [ ] Manejo de errores.
- [ ] README.md actualizado.

### Documento README.md con capturas:

- [ ] Captura de ejecución de `alembic init`.
- [ ] Captura de creación de migración con `alembic revision --autogenerate`.
- [ ] Captura de aplicación de migración con `alembic upgrade head`.
- [ ] Captura de estructura de tablas generadas.
- [ ] Capturas de Swagger UI.
- [ ] Evidencia de creación de usuario, dispositivo y préstamo.
- [ ] Evidencia de consultas con joins.
- [ ] Evidencia de filtros aplicados.
- [ ] Evidencia de devolución de dispositivo.
- [ ] Reflexión sobre la importancia de migraciones, relaciones y consultas avanzadas.

---

## Reflexión final (guía para socialización)

Cada aprendiz deberá explicar en máximo 5 minutos:

1. **¿Qué cambios realizaste respecto a la versión anterior de device_systems?**
   - Nuevos modelos: Device y Loan.
   - Rutas y servicios para dispositivos y préstamos.
   - Migraciones con Alembic.
   - Consultas con joins y filtros avanzados.

2. **¿Cómo configuraste Alembic?**
   - `alembic init alembic`.
   - Configuración de `alembic.ini` (URL de BD).
   - Configuración de `env.py` (import de modelos y `target_metadata`).

3. **¿Qué migraciones generaste?**
   - Migración inicial o de actualización para crear tablas `devices` y `loans`.
   - Comandos: `revision --autogenerate`, `upgrade head`, `history`.

4. **¿Cómo relacionaste User, Device y Loan?**
   - `ForeignKey` en `Loan` hacia `User` y `Device`.
   - `relationship()` con `back_populates` en ambos lados.

5. **¿Cómo funcionan las consultas con joins?**
   - `join()` entre `Loan`, `User` y `Device`.
   - Respuestas con schemas anidados (`UserBasic`, `DeviceBasic`).

6. **¿Cómo aplicaste filtros avanzados?**
   - Parámetros opcionales en los endpoints.
   - `ilike()` para búsquedas parciales.
   - Condiciones con `and_()` / `or_()`.

7. **¿Qué aprendiste sobre modelado relacional en APIs REST?**
   - Importancia de la integridad referencial.
   - Separación de responsabilidades (modelos, schemas, rutas, servicios).
   - Versionamiento de BD con migraciones.
   - Potencia de las consultas combinadas.

---

## Sugerencias y comandos útiles

### Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

Con `uv`:
```bash
uv run uvicorn app.main:app --reload
```

### Alembic — comandos rápidos

```bash
uv run alembic init alembic              # Inicializar
uv run alembic revision --autogenerate -m "mensaje"  # Crear migración
uv run alembic upgrade head              # Aplicar migraciones
uv run alembic downgrade -1              # Revertir última migración
uv run alembic history                    # Ver historial
uv run alembic current                    # Ver estado actual
```

### Posibles errores y soluciones

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` | `sys.path` no incluye la raíz | Agregar `sys.path` en `env.py` |
| `Target database is not up to date.` | Hay migraciones sin aplicar | Ejecutar `alembic upgrade head` |
| `FAILED: No migrations to apply.` | `target_metadata` es `None` | Configurar `target_metadata = Base.metadata` en `env.py` |
| `sqlalchemy.exc.OperationalError: no such table` | Migración no ejecutada | Ejecutar `alembic upgrade head` |

### Links de referencia

- [FastAPI — Documentación oficial](https://fastapi.tiangolo.com/)
- [SQLAlchemy — Documentación oficial](https://docs.sqlalchemy.org/)
- [Alembic — Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Pydantic v2 — Documentación](https://docs.pydantic.dev/latest/)
- [Material de apoyo del curso](https://educated-show-144.notion.site/Guia-de-aprendizaje-Material-de-apoyo-2414671e02a180eebe92d827e2f7c8d1)
