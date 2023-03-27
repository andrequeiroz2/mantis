from itertools import count

from pydantic import BaseModel
from typing import List


class LastWillSchema(BaseModel):
    topic: str


class LastWillListSchema(BaseModel):
    last_wills: List[LastWillSchema]
    count: int
