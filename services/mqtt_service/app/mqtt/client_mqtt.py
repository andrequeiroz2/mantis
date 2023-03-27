import paho.mqtt.client as mqtt
from core.config import settings

MQTTv31 = 3
MQTTv311 = 4
MQTTv5 = 5


client_mqtt = mqtt.Client(
    client_id=settings.MQTT_CLIENT_ID,
    userdata=settings.MQTT_USERDATA,
    protocol=MQTTv5,
    transport=settings.MQTT_TRANSPORT
)


def on_connect(client, userdata, flags, rc, properties=None):
    print("client", client)
    print("rc", rc)
    print("userdata", userdata)
    print("flags", flags)
    ""


def on_message(client, userdata, msg):
    # print(client)
    # print(userdata)
    print(msg.topic+" "+str(msg.payload))


# def on_subscribe(client, userdata, mid, reasonCodes, properties):
#     print(client)
#     print(userdata)
#     print(mid)
#     print(reasonCodes)
#     print(properties)


client_mqtt.connect(
    host=settings.MQTT_HOST,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEP_ALIVE
)

client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message
# client_mqtt.on_subscribe = on_subscribe
