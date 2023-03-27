from fastapi_utils.inferring_router import InferringRouter
from schema.mqtt import SubscribeSchema
from fastapi_utils.cbv import cbv
from fastapi import status

from business.mqtt import MqttBusiness


mqtt_router = InferringRouter()


@cbv(mqtt_router)
class MqttRouter:

    @mqtt_router.post("/subscribe", status_code=status.HTTP_201_CREATED)
    async def mqtt_subscribe(self, subscribe_schema: SubscribeSchema):
        await MqttBusiness().mqtt_subscribe(
            subscribe_schema
        )
