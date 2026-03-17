"""
Rate Limiting Middleware
Limits requests per IP address. Returns 429 if limit exceeded.
Note: Uses in-memory store; for production, use Redis or similar.
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from typing import Dict
import threading

RATE_LIMIT = 60  # requests
TIME_WINDOW = 60  # seconds

# In-memory store: {ip: [timestamps]}
_request_times: Dict[str, list] = {}
_lock = threading.Lock()

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        with _lock:
            times = _request_times.get(client_ip, [])
            # Remove timestamps outside the window
            times = [t for t in times if now - t < TIME_WINDOW]
            if len(times) >= RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Try again later."}
                )
            times.append(now)
            _request_times[client_ip] = times
        return await call_next(request)

# Usage: Add to FastAPI app with app.add_middleware(RateLimitMiddleware)
