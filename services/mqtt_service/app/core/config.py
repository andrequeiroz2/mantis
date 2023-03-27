from pydantic import BaseSettings
from dotenv import find_dotenv, load_dotenv
from functools import lru_cache
import os


class Settings(BaseSettings):

    load_dotenv(find_dotenv(".env.mqtt"), override=True)

    # API
    HOST = os.environ.get("HOST")
    PORT = int(os.environ.get("PORT"))
    LOGLEVEL = os.environ.get("LOGLEVEL")
    APITITLE = os.environ.get("APITITLE")
    DEBUG = os.environ.get("DEBUG")


    # Broker Mqtt
    MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID")
    MQTT_CLEAN_SESSION = bool(os.environ.get("MQTT_CLEAN_SESSION"))
    MQTT_USERDATA = os.environ.get("MQTT_USERDATA")
    MQTTv5 = 5
    MQTT_PROTOCOL = MQTTv5
    MQTT_TRANSPORT = os.environ.get("MQTT_TRANSPORT")

    # Connect Mqtt
    MQTT_HOST = os.environ.get("MQTT_HOST")
    MQTT_PORT = int(os.environ.get("MQTT_PORT"))
    MQTT_KEEP_ALIVE = int(os.environ.get("MQTT_KEEP_ALIVE"))


@lru_cache
def settings_get() -> Settings:
    return Settings()


settings = settings_get()

