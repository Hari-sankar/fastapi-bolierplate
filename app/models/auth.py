from pydantic import BaseModel, Field, EmailStr
from app.shared.constants import *

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description=EMAIL_DESC, example=EMAIL_EXAMPLE)
    password: str = Field(..., description=PASSWORD_DESC, example=PASSWORD_EXAMPLE, min_length=8)

class SignUpRequest(BaseModel):
    first_name: str = Field(None, description=FIRST_NAME_DESC, example=FIRST_NAME_EXAMPLE)
    last_name: str = Field(None, description=LAST_NAME_DESC, example=LAST_NAME_EXAMPLE)
    email: EmailStr = Field(..., description=EMAIL_DESC, example=EMAIL_EXAMPLE)
    password: str = Field(..., description=PASSWORD_DESC, example=PASSWORD_EXAMPLE, min_length=8)

class VerifyTokenRequest(BaseModel):
    token: str = Field(..., description=TOKEN_DESC, example=TOKEN_EXAMPLE)

class ResetPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description=EMAIL_DESC, example=EMAIL_EXAMPLE)

class PasswordResetRequest(BaseModel):
    token: str = Field(..., description=PASSWORD_RESET_TOKEN_DESC, example=TOKEN_EXAMPLE)
    new_password: str = Field(..., description=NEW_PASSWORD_DESC, example=NEW_PASSWORD_EXAMPLE, min_length=8)
