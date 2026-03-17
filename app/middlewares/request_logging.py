"""
Request Logging Middleware
Logs HTTP method, path, response status, and execution time for each request.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # ms
        logging.info(
            f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}ms"
        )
        return response


# Usage: Add to FastAPI app with app.add_middleware(RequestLoggingMiddleware)
