from pydantic import BaseModel, EmailStr
from fastapi_utils.api_model import APIModel
from uuid import UUID


class UserUuidSchema(BaseModel):
    user_uuid: UUID


class UserEmailFilterSchema(APIModel):
    user_email: EmailStr
