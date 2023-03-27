from fastapi import FastAPI
from core.config import settings
from mqtt.client_mqtt import client_mqtt
from endpoint.mqtt import mqtt_router
import uvicorn


app = FastAPI()


app.include_router(mqtt_router, tags=["Mqtt"], prefix="/api/mqttservice")


if __name__ == "__main__":
    client_mqtt.loop_start()
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOGLEVEL)


