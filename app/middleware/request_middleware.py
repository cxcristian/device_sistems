import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{elapsed:.4f}"
        response.headers["X-App-Name"] = "device_systems"

        print(f"{request.method} {request.url.path} {response.status_code} [{elapsed:.4f}s]")

        return response