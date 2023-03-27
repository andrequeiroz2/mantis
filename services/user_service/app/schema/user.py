from pydantic import BaseModel, EmailStr
from fastapi_utils.api_model import APIModel
from typing import List
from uuid import UUID


class UserSchema(BaseModel):
    username: str
    email: str


class UserListSchema(BaseModel):
    users: List[UserSchema]
    total: int


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserDB(BaseModel):
    username: str
    email: str
    password: str


class UserPassSchema(UserSchema):
    hashed_password: str


class UserTokenSchema(UserSchema):
    access_token: str
    token_type: str = "bearer"


class UserUuidSchema(BaseModel):
    user_uuid: UUID


class UserEmailFilter(APIModel):
    user_email: EmailStr


class UserHasSchema(APIModel):
    check: bool
