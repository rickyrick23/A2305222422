from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import uuid

class RequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        method = request.method
        path = request.url.path
        client_ip = request.client.host
        print(f"[{request_id}] --> {method} request to {path} from {client_ip}")
        response = await call_next(request)
        duration = time.time() - start_time
        status_code = response.status_code
        print(f"[{request_id}] <-- Completed in {duration:.3f}s with status {status_code}")
        return response
