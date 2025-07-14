from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.models.response import format_response
import logging
from app.redis.redis_instance import r

from app.core.config import Settings
from app.db.migration import migration
from app.routes.health_routes import router as health_router
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router


# Loading Config
settings = Settings()

# Logging Config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI Initialization
app = FastAPI()

# StartUp Event
@app.on_event("startup")
async def startup_event():
    # Database Migrations
    migration()
    # flush Redis 
    r.flushdb()
    logger.info("Application is starting...")

# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down...")

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
async def middleware(request: Request, call_next):
    # Logging request details
    logger.info(f"Request from : {request.client}")
    logger.info(f"End Point : {request.url}")
    
    response = await call_next(request)

    # Logging response details
    logger.info(f"Response status code: {response.status_code}")

    # Error Handling
    if response.status_code >= 400:
        if isinstance(response, JSONResponse):
            logger.error(f"Error: {response.status_code} - {response.content.decode('utf-8')}")
        else:
            logger.error(f"Error: {response.status_code}")
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