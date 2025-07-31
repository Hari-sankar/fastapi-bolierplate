# In app/middleware/logging_middleware.py

import json
import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import Message

# Assuming your get_logger is in app.core.logging
from app.core.logging import get_logger

logger = get_logger("app.middleware")

# A helper function to read the request body without consuming it
async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}
    request._receive = receive

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        # Read the request body to make it available for logging in case of an error
        req_body_bytes = await request.body()
        await set_body(request, req_body_bytes)

        # Process the request and correctly handle exceptions
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logger.exception(
                "Unhandled server error",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                    "client_ip": request.client.host,
                }
            )
            # This is critical: return a proper 500 response
            return JSONResponse(
                status_code=500,
                content={"detail": "An internal server error occurred."},
            )

        duration_ms = round((time.time() - start_time) * 1000, 2)
        status_code = response.status_code

        # Determine log level and message based on response status
        log_level = logging.INFO
        log_message = "HTTP request"
        if status_code >= 500:
            log_level = logging.ERROR
            log_message = "HTTP server error"
        elif status_code >= 400:
            log_level = logging.WARNING
            log_message = "HTTP client error"

        log_extra = {
            "method": request.method,
            "path": request.url.path,
            "query": str(request.query_params),
            "status_code": status_code,
            "duration_ms": duration_ms,
            "client_ip": request.client.host,
        }
        
        # Conditionally log the request body for client errors for easier debugging
        if status_code >= 400:
            try:
                # Attempt to parse as JSON for structured logging
                log_extra["request_body"] = json.loads(req_body_bytes.decode())
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Fallback to plain text if not valid JSON
                log_extra["request_body"] = req_body_bytes.decode(errors="ignore")

        # Log the single, consolidated message
        logger.log(log_level, log_message, extra=log_extra)
        
        return response
