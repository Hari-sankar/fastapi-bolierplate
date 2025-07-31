from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import Settings
from app.core.logging import get_logger, setup_logging
from app.db.migration import migration
from app.middleware.logging_midleware import LoggingMiddleware
from app.redis.redis_instance import r
from app.routes.api_router import api_router
from app.schemas.response import format_response

# Loading Config
settings = Settings()

# Logging Config
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # StartUp Event

    # Database Migrations
    if settings.MIGRATION:
        migration()
    # flush Redis 
    try:
        if r is not None:
            r.flushdb()
            logger.info("Redis server flushed successfully")
        else:
            logger.info("Redis server not available, skipping flush")
    except Exception as e:
            logger.warning(f"Redis server not available: {e!s}")
            logger.info("Continuing without Redis ...")
        
    logger.info("Application is starting...")

    yield
    # Shutdown Event
    logger.info("Application is shutting down...")


# FastAPI Initialization
app = FastAPI(lifespan=lifespan)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=settings.CORS_METHOD,
    allow_headers=settings.CORS_HEADER,
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Add Routes
app.include_router(api_router)


# Custom Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc}")
    return JSONResponse(content=format_response(exc.status_code, exc.detail), status_code=exc.status_code)
