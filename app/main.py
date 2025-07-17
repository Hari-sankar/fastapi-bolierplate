from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.schemas.response import format_response
import logging
import time
from app.redis.redis_instance import r

from app.core.config import Settings
from app.db.migration import migration
from app.routes.health_routes import router as health_router
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.core.logging import  get_logger, setup_logging


# Loading Config
settings = Settings()

# Logging Config
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # StartUp Event

    # Database Migrations
    if settings.MIGRATION:
        migration()
    # flush Redis 
    # r.flushdb()
    logger.info("Application is starting...")

    yield
    # Shutdown Event
    logger.info("Application is shutting down...")


# FastAPI Initialization
app = FastAPI(lifespan=lifespan)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for logging and error handling
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    client_host = request.client.host if request.client else "unknown"
    method = request.method
    path = request.url.path
    query_params = str(request.query_params)
    headers = dict(request.headers)

    logger.info(
        "HTTP Request",
        extra={
            "client_ip": client_host,
            "method": method,
            "path": path,
            "query": query_params,
            "headers": headers,
        }
    )

    try:
        response: Response = await call_next(request)
    except Exception as exc:
        duration = round((time.time() - start_time) * 1000, 2)
        logger.exception(
            "Unhandled server error",
            extra={
                "method": method,
                "path": path,
                "duration_ms": duration,
                "client_ip": client_host
            }
        )
        

    # Optional: read body only for JSON responses (for structured error logs)
    body = None
    if isinstance(response, JSONResponse):
        try:
            body = response.body.decode("utf-8")
        except Exception:
            body = "<unreadable>"

    duration = round((time.time() - start_time) * 1000, 2)

    log_level = "info"
    if response.status_code >= 500:
        log_level = "error"
    elif response.status_code >= 400:
        log_level = "warning"

    logger.log(
        level=getattr(logging, log_level.upper()),
        msg="HTTP Response",
        extra={
            "status_code": response.status_code,
            "duration_ms": duration,
            "method": method,
            "path": path,
            "client_ip": client_host,
            "response_body": body if response.status_code >= 400 else None,
        }
    )

    return response

# Routes
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Custom Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc}")
    return JSONResponse(content=format_response(exc.status_code, exc.detail), status_code=exc.status_code)