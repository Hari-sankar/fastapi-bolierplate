from fastapi import APIRouter
from app.routes.auth_routes import router as auth_router
from app.routes.health_routes import router as health_router
from app.routes.user_routes import router as user_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(user_router, prefix="/user", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])