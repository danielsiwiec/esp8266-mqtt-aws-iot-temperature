import ujson

from thermistor import Thermistor
from mqtt import MQTT
from wifi import connect_to_wifi
from sleep import deep_sleep_seconds

with open('props.json') as f:
    c = ujson.loads(f.read())

connect_to_wifi(c['wifi_sid'], c['wifi_pass'])
thermistor = Thermistor()
mqtt = MQTT(c['client_id'], c['iot_endpoint'], c['iot_topic'])

while True:
    temp = thermistor.get_temp()
    mqtt.send({'temp': temp})
    deep_sleep_seconds(c['sleep_seconds'])
