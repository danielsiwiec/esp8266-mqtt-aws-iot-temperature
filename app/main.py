import machine

from props import load_props
from thermistor import Thermistor
from mqtt import MQTT
from wifi import connect_to_wifi

props = load_props()

connect_to_wifi(props['wifi_sid'], props['wifi_pass'])
mqtt = MQTT(props['client_id'], props['iot_endpoint'], props['iot_topic'])
thermistor = Thermistor()

while True:
    temp = thermistor.get_temp()
    mqtt.send({'temp': temp})
    machine.deepsleep(5*60*1000)
