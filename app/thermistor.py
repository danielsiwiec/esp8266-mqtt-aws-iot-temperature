import time
import math
import machine

class Thermistor:
    def __init__(self):
        self.analog = machine.ADC(0)

    def _get_analog_with_sleep(self, sleep):
        time.sleep_ms(100)
        return self.analog.read()

    def get_analog(self):
        sample_size = 5
        return sum([self._get_analog_with_sleep(100) for _ in range(sample_size)])/sample_size

    def _steinhart_temperature_C(self, r, Ro=10000.0, To=25.0, beta=3950.0):
      steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
      steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
      steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
      return steinhart

    def get_temp(self):
        R = 10000 / (1023/self.get_analog() - 1)
        temp_c = self._steinhart_temperature_C(R)
        temp_f = temp_c * 9/5 + 32
        return temp_f