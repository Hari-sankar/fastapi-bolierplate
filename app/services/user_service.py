import json
from fastapi import HTTPException
from app.db.session import get_db
from app.models.user import *
from app.models.response import format_response
from app.redis.redis_instance import r

def list_users(query_params: UserQueryParams):
    with get_db() as cursor:
        limit = query_params.limit or 10
        offset = query_params.offset or 0
        search = query_params.search 
        sort = query_params.sort or "ASC"
        
        query = "SELECT * FROM users"
        conditions = []
        params = []
        
        if search:
            conditions.append("first_name LIKE %s")
            params.append(f"%{search}%")
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        if sort and sort.lower() == 'asc':
            query += " ORDER BY first_name ASC"
        elif sort and sort.lower() == 'desc':
            query += " ORDER BY first_name DESC"
        
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)

        try:
            cursor.execute(query, params)
            users = cursor.fetchall()
            users_data = [UserModel(**user) for user in users]
            print(users_data)
        except Exception as e:
            return format_response(500, str(e))
        return format_response(200, "Users fetched Successfully", users_data)

def read_user(user_id: int):
    with get_db() as cursor:
        cached_user = r.get(f"user:{user_id}")
        if cached_user:
            return format_response(200, "User fetched from cache", json.loads(cached_user.decode("utf-8")))
        try:
            query = "SELECT * FROM users WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            user_row = cursor.fetchone()
            if not user_row:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Convert tuple to dictionary
            column_names = [desc[0] for desc in cursor.description]
            user = dict(zip(column_names, user_row))
            
            r.set(f"user:{user_id}", json.dumps(user))
        except Exception as error:
            return format_response(500, str(error))
        return format_response(200, "User details fetched Successfully", user)

def create_user(user: UserCreate):
    with get_db() as cursor:
        try:
            query = """INSERT INTO users (email, password, first_name, last_name) 
                       VALUES (%s, %s, %s, %s) RETURNING user_id;"""
            cursor.execute(query, (user.email, user.password, user.first_name, user.last_name))
        except Exception as error:
            return format_response(500, str(error))
        return format_response(201, "User inserted Successfully")

def update_user(user_id: int, user_update: UserUpdate):
    with get_db() as cursor:
        try:
            updates = []
            params = []
            if user_update.email:
                updates.append("email = %s")
                params.append(user_update.email)
            if user_update.password:
                updates.append("password = %s")
                params.append(user_update.password)
            if user_update.first_name:
                updates.append("first_name = %s")
                params.append(user_update.first_name)
            if user_update.last_name:
                updates.append("last_name = %s")
                params.append(user_update.last_name)
            
            if updates:
                params.append(user_id)
                query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s;"
                cursor.execute(query, params) 
                r.delete(f"user:{user_id}")
        except Exception as error:
            return format_response(500, str(error))
        return format_response(200, "User details updated successfully")

def delete_user(user_id: int):
    with get_db() as cursor:
        try:
            query = "DELETE FROM users WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            r.delete(f"user:{user_id}")  
        except Exception as error:
            return format_response(500, str(error))
        return format_response(200, "User deleted Successfully")
