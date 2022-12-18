from pydantic import BaseModel
from typing import List


class BoardTypeSchema(BaseModel):
    model: str
    version: str
    description: str


class BoardTypeListSchema(BaseModel):
    boards_type: List[BoardTypeSchema]
    total: int
