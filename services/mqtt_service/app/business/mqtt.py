from schema.mqtt import SubscribeSchema
from mqtt.client_mqtt import client_mqtt
from fastapi import HTTPException, status


class MqttBusiness:

    @staticmethod
    async def mqtt_subscribe(subscribe_schema: SubscribeSchema):
        try:
            client_mqtt.subscribe(
                topic=subscribe_schema.topic,
                qos=subscribe_schema.qos
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="topic|qos unprocessable",
            )

