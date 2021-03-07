# https://circuitpython.readthedocs.io/projects/ads1x15/en/latest/examples.html

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Adc_utils:
    def __init__(self):
        # self.i2c = busio.I2C(board.SCL, board.SDA)
        # self.ads = ADS.ADS1115(i2c)
        # self.chan = AnalogIn(ads, ADS.P0)

        pass

    def
    pass


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C address instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

# posso selezionare i gudagni
# ads.gain=2/3
# ads.gain=1#questo è quello di default
# ads.gain=2
# ads.gain=4
# ads.gain=8
# ads.gain=16

# stampo il valore del guadagno
print(ads.gain)
print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(3)
