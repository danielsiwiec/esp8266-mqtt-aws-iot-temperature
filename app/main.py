import sys
import ujson
import uasyncio
import machine

from thermistor import Thermistor
from mqtt import MQTT
from wifi import connect_to_wifi

f = open('props.json')
c = ujson.loads(f.read())

connect_to_wifi(c['client_id'], c['wifi_sid'], c['wifi_pass'], c['iot_topic'])


async def send_temp(thermistor, mqtt):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    while True:
        temp = thermistor.get_temp()
        mqtt.send({'temp': temp})
        rtc.alarm(rtc.ALARM0, 60000)
        machine.deepsleep()


async def main():
    thermistor = Thermistor()
    mqtt = MQTT(c['iot_endpoint'])
    uasyncio.create_task(send_temp(thermistor, mqtt))

loop = uasyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
