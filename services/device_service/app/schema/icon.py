from pydantic import BaseModel


class IconSchema(BaseModel):
    name: str
    icon: str
