from fastapi import APIRouter, Depends
from app.schemas.response import DataResponse
from app.schemas.user import UserCreate, UserQueryParams, UserUpdate
from typing import List
import app.services.user_service as user_service
from app.redis.redis_instance import r

router = APIRouter()

@router.get("", response_model=DataResponse) 
def list_users(query_params: UserQueryParams = Depends()):
    return user_service.list_users(query_params)

@router.get("/{user_id}")
def read_user(user_id: int):
    return user_service.read_user(user_id)

@router.post("")
def create_user(user: UserCreate):
    return user_service.create_user(user)

@router.patch("/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    return user_service.update_user(user_id, user_update)

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return user_service.delete_user(user_id)



