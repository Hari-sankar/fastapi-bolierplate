from fastapi import APIRouter, BackgroundTasks
from app.models.auth import *
from app.services import auth_service

router = APIRouter()

@router.post("/login")
async def login(loginRequest: LoginRequest):
    return await auth_service.login(loginRequest)

@router.post("/signup")
async def signup(userData: SignUpRequest, background_tasks: BackgroundTasks):
    return await auth_service.signup(userData, background_tasks)

@router.post("/signup/verify")
async def verify_signup(verifyTokenRequest: VerifyTokenRequest):
    return await auth_service.verify_signup(verifyTokenRequest)

@router.post("/forgotPwd")
async def forgot_password(resetPasswordRequest: ResetPasswordRequest, background_tasks: BackgroundTasks):
    return await auth_service.forgot_password(background_tasks, resetPasswordRequest)

@router.post("/forgotPwd/verify")
async def verify_reset_token(passwordResetRequest: PasswordResetRequest):
    return await auth_service.verify_reset_token(passwordResetRequest)
