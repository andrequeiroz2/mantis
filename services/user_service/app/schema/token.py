from pydantic import BaseModel
from typing import Union


class TokenSchema(BaseModel):
    token: str


class TokenDataSchema(BaseModel):
    username: Union[str, None] = None
