from pydantic import BaseModel
from uuid import UUID


class UserUuidSchema(BaseModel):
    user_uuid: UUID
