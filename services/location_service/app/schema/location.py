from fastapi_utils.api_model import APIModel
from uuid import UUID
from pydantic import EmailStr


class LocationSchema(APIModel):
    user_email: str
    location_name: str
    description: str
    latitude: float
    longitude: float


class LocationsSchema(APIModel):
    user_email: str
    location_uuid: UUID
    location_name: str
    description: str
    latitude: float
    longitude: float


class LocationPutSchema(APIModel):
    location_name: str
    description: str
    latitude: float
    longitude: float


class LocationFilterSchema(APIModel):
    user_email: EmailStr
    location_uuid: UUID
