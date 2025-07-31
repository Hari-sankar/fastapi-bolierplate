from typing import Literal

from pydantic import BaseModel, EmailStr, Field, conint, constr

from app.shared.constants import (
    EMAIL_DESC,
    EMAIL_EXAMPLE,
    EMAIL_MISSING_ERROR,
    FIRST_NAME_DESC,
    FIRST_NAME_EXAMPLE,
    INVALID_EMAIL_ERROR,
    LAST_NAME_DESC,
    LAST_NAME_EXAMPLE,
    LIMIT_DESC,
    LIMIT_EXAMPLE,
    OFFSET_DESC,
    OFFSET_EXAMPLE,
    PASSWORD_DESC,
    PASSWORD_EXAMPLE,
    PASSWORD_LENGTH_ERROR,
    PASSWORD_MISSING_ERROR,
    SEARCH_DESC,
    SORT_DESC,
    SORT_EXAMPLE,
)


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
    email: EmailStr | None = Field(None, description=EMAIL_DESC, example=EMAIL_EXAMPLE, error_messages={"value_error.email": INVALID_EMAIL_ERROR})
    password: constr(min_length=8) | None = Field(None, description=PASSWORD_DESC, example=PASSWORD_EXAMPLE)
    first_name: str | None = Field(None, description=FIRST_NAME_DESC, example=FIRST_NAME_EXAMPLE)
    last_name: str | None = Field(None, description=LAST_NAME_DESC, example=LAST_NAME_EXAMPLE)

class UserQueryParams(BaseModel):
    limit: conint(gt=0) | None = Field(None, description=LIMIT_DESC, example=LIMIT_EXAMPLE)
    offset: conint(ge=0) | None = Field(None, description=OFFSET_DESC, example=OFFSET_EXAMPLE)
    search: str | None = Field(None, description=SEARCH_DESC)
    sort: Literal["ASC", "DESC"] | None = Field(None, description=SORT_DESC, example=SORT_EXAMPLE)
