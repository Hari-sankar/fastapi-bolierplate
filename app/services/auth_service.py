from fastapi import HTTPException

from app.db.session import get_db
from app.schemas.auth import *
from app.schemas.response import format_response
from app.utlis.generateJwt import create_jwt_token
from app.utlis.verifyPwd import hash_password, verify_password
from app.core.logging import get_logger

logger = get_logger(__name__)

async def login(loginRequest:LoginRequest):
    with get_db() as cursor:
        query = "SELECT * FROM users WHERE email = %s;"
        cursor.execute(query, (loginRequest.email,))
        user = cursor.fetchone()
        print(user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(loginRequest.password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid Password")
        data={"userId": user["user_id"],"firstName":user["first_name"],"lastName":user["last_name"]}
        token = create_jwt_token(data)
        return format_response(200, "Login Successfully",token)

async def signup(userData: SignUpRequest):
    with get_db() as cursor:
        try:
            query = "SELECT * FROM users WHERE email = %s;"
            cursor.execute(query, (userData.email,))
            user = cursor.fetchone()
            if user:
                raise HTTPException(status_code=409, detail="User Already Exists")
            hashed_password = hash_password(userData.password)
            query = """INSERT INTO users (email, password, first_name, last_name) 
                        VALUES (%s, %s, %s, %s) RETURNING user_id;"""
            cursor.execute(query, (userData.email, hashed_password, userData.first_name, userData.last_name))
            
            return format_response(200, "Account has been created successfully")
        
        except Exception as e:
            logger.error("Error creating new user", error=str(e))
            return format_response(500, "Error creating new user")

