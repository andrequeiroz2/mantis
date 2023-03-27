from fastapi_utils.api_model import APIModel


class SubscribeSchema(APIModel):
    topic: str
    qos: int
