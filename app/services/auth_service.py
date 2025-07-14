from app.db.session import get_db
from app.models.auth import *
from app.models.response import format_response
from app.utlis.email import forgot_pwd_email_content, invite_email_content, send_email
from app.utlis.generateJwt import create_jwt_token,verify_jwt_token
from app.utlis.verifyPwd import hash_password, verify_password
from fastapi import HTTPException
from fastapi import BackgroundTasks

async def login(loginRequest:LoginRequest):
    with get_db() as cursor:
        query = "SELECT * FROM users WHERE email = %s;"
        cursor.execute(query, (loginRequest.email,))
        user = cursor.fetchone()
        print(user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(loginRequest.password, user['password']):
            raise HTTPException(status_code=400, detail="Invalid Password")
        data={"userId": user['user_id'],"firstName":user['first_name'],"lastName":user['last_name']}
        token = create_jwt_token(data)
        return format_response(200, "Login Successfully",token)

async def signup(userData: SignUpRequest,background_tasks: BackgroundTasks):
    with get_db() as cursor:
        query = "SELECT * FROM users WHERE email = %s;"
        cursor.execute(query, (userData.email,))
        user = cursor.fetchone()
        if user:
            raise HTTPException(status_code=409, detail="User Already Exists")
        data = {
            "firstName":userData.first_name,
            "lastName":userData.last_name,
            "email":userData.email,
            "password":userData.password
        }
        token = create_jwt_token(data)
        email_content = invite_email_content(userData.first_name,token)
        background_tasks.add_task(send_email, userData.email, "Welcome to QB CHAT", email_content)
        return format_response(200, "Verfication Email has send successfully")

async def verify_signup(verifyTokenRequest:VerifyTokenRequest):
    with get_db() as cursor:
        payload = verify_jwt_token(verifyTokenRequest.token)
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid Token")
        email = payload.get('email')
        password = payload.get('password')
        firstName = payload.get('firstName')
        lastName = payload.get('lastName')
        if not email:
            raise HTTPException(status_code=400, detail="Invalid Token Payload")
        
        # Activate the user account and set the password
        hashed_password = hash_password(password)
        query = """INSERT INTO users (email, password, first_name, last_name) 
                       VALUES (%s, %s, %s, %s) RETURNING user_id;"""
        cursor.execute(query, (email, hashed_password, firstName, lastName))
        
        return format_response(200, "Account has been created successfully")

async def forgot_password(background_tasks: BackgroundTasks, resetPasswordRequest: ResetPasswordRequest):
    with get_db() as cursor:
        query = "SELECT * FROM users WHERE email = %s;"
        cursor.execute(query, (resetPasswordRequest.email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=400, detail="User Doesn't Exist")
        token = create_jwt_token(data={"email": resetPasswordRequest.email})
        email_content = forgot_pwd_email_content(token)
        background_tasks.add_task(send_email, resetPasswordRequest.email, "Reset Your Password", email_content)
        return format_response(200, "Password Reset Email has send successfully")

async def verify_reset_token(passwordResetRequest: PasswordResetRequest):
    with get_db() as cursor:
        payload = verify_jwt_token(passwordResetRequest.token)
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid Token")
        email = payload.get('email')
        if not email:
            raise HTTPException(status_code=400, detail="Invalid Token Payload")
        
        # Update the password
        hashed_password = hash_password(passwordResetRequest.new_password)
        query = "UPDATE users SET password = %s WHERE email = %s;"
        cursor.execute(query, (hashed_password, email))
        
        return format_response(200, "Password has been reset successfully")