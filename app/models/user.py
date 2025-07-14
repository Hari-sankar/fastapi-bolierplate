from pydantic import BaseModel, Field, EmailStr, constr, conint
from typing import Optional, Literal
from app.shared.constants import *

class UserModel(BaseModel):
    user_id: int
    email: str
    password: str
    first_name: str 
    last_name: str
    isactive: bool

class UserCreate(BaseModel):
    email: EmailStr = Field(...,
                            description=EMAIL_DESC,
                            example=EMAIL_EXAMPLE,
                            error_messages={
                                "value_error.missing": EMAIL_MISSING_ERROR,
                                "value_error.email": INVALID_EMAIL_ERROR
                            })
    password: str = Field(...,
                          description=PASSWORD_DESC,
                          example=PASSWORD_EXAMPLE,
                          min_length=8,
                          error_messages={
                              "value_error.missing": PASSWORD_MISSING_ERROR,
                              "value_error.any_str.min_length": PASSWORD_LENGTH_ERROR
                          })
    first_name: str = Field(description=FIRST_NAME_DESC, example=FIRST_NAME_EXAMPLE)
    last_name: str = Field(description=LAST_NAME_DESC, example=LAST_NAME_EXAMPLE)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description=EMAIL_DESC, example=EMAIL_EXAMPLE, error_messages={"value_error.email": INVALID_EMAIL_ERROR})
    password: Optional[constr(min_length=8)] = Field(None, description=PASSWORD_DESC, example=PASSWORD_EXAMPLE)
    first_name: Optional[str] = Field(None, description=FIRST_NAME_DESC, example=FIRST_NAME_EXAMPLE)
    last_name: Optional[str] = Field(None, description=LAST_NAME_DESC, example=LAST_NAME_EXAMPLE)

class UserQueryParams(BaseModel):
    limit: Optional[conint(gt=0)] = Field(None, description=LIMIT_DESC, example=LIMIT_EXAMPLE)
    offset: Optional[conint(ge=0)] = Field(None, description=OFFSET_DESC, example=OFFSET_EXAMPLE)
    search: Optional[str] = Field(None, description=SEARCH_DESC)
    sort: Optional[Literal["ASC", "DESC"]] = Field(None, description=SORT_DESC, example=SORT_EXAMPLE)
