from typing import Optional
from fastapi_utils.api_model import APIModel
from uuid import UUID
from pydantic import EmailStr


class TypeDeviceList(APIModel):
    name: str


class TypeSensorListSchema(APIModel):
    id: int
    name: str
    measure: str
    scale: str
    max_scale: int
    min_scale: int
    icon: str


class SensorPostSchema(APIModel):
    user_email: EmailStr
    name: str
    description: str
    location_uuid: UUID
    type_sensor_id: int
    hub_id: Optional[int]
