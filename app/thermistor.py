import time
import math
from machine import Pin, ADC


class Thermistor:
    def __init__(self):
        self.analog = ADC(Pin(34))
        self.analog.atten(ADC.ATTN_11DB)

    def _get_analog_with_sleep(self, sleep):
        time.sleep_ms(100)
        return self.analog.read()

    def _get_analog(self):
        sample_size = 5
        return sum([self._get_analog_with_sleep(100) for _ in range(sample_size)])/sample_size

    def _steinhart_temperature_C(self, r, Ro=10000.0, To=25.0, beta=3950.0):
        steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
        steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
        steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
        return steinhart

    def _get_thermistor_resistance(self, Rnom=10000, adc_resolution=4095):
        return Rnom / (adc_resolution/self._get_analog() - 1)

    def _c_to_f(self, c):
        return c * 9/5 + 32

    def get_temp(self):
        Rt = self._get_thermistor_resistance()
        temp_c = self._steinhart_temperature_C(Rt)
        temp_f = self._c_to_f(temp_c)
        return temp_f
