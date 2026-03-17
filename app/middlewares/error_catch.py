"""
Global Error Catching Middleware
Catches unhandled exceptions and returns a standardized JSON error response.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import logging

class ErrorCatchMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logging.error(f"Unhandled error: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error.",
                    "error": str(exc)  # Remove or mask in production
                }
            )

# Usage: Add to FastAPI app with app.add_middleware(ErrorCatchMiddleware)
