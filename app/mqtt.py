from umqtt.simple import MQTTClient
import json

class MQTT:
    def __init__(self, client_id, iot_endpoint, iot_topic):
        mqtt_port = 8883
        self.mqtt_topic = iot_topic
        mqtt_host = iot_endpoint

        private_key = open("/private_key.der").read()
        certificate = open("/cert.der").read()

        mqtt_client = MQTTClient(
            client_id=client_id,
            server=mqtt_host,
            port=mqtt_port,
            keepalive=10000,
            ssl=True,
            ssl_params={
                "cert": certificate,
                "key": private_key}
        )
        print('Connecting to AWS IoT Core...')
        mqtt_client.connect()
        print('Connected.')
        self.client = mqtt_client

    def send(self, message):
        self.client.publish(self.mqtt_topic, json.dumps(message), qos=1)

    def close(self):
        self.client.disconnect()
