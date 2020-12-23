from props import load_props
from thermistor import Thermistor
from mqtt import MQTT
from wifi import connect_to_wifi
from sleep import deep_sleep_seconds


props = load_props()

connect_to_wifi(props['wifi_sid'], props['wifi_pass'])
mqtt = MQTT(props['client_id'], props['iot_endpoint'], props['iot_topic'])
thermistor = Thermistor()

while True:
    temp = thermistor.get_temp()
    mqtt.send({'temp': temp})
    deep_sleep_seconds(props['sleep_seconds'])
