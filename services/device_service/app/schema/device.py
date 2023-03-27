from fastapi_utils.api_model import APIModel


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
