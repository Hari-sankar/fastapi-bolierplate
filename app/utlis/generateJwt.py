import jwt
import datetime
from typing import Optional, Dict
from fastapi import HTTPException

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"  

def create_jwt_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1) 
    token = jwt.encode({"exp": expiration, **data}, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt_token(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
