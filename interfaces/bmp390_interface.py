import time

import board
import busio
import adafruit_bmp3xx
import numpy as np

import config as conf
from iir_filter import IirFilter


class BMP390_Interface():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bmp390 = adafruit_bmp3xx.BMP3XX_I2C(i2c)

        self.iir_filter = IirFilter(0.8, 2)

        self.bmp390.sea_level_pressure = 1013.25
        self.bmp390.pressure_oversampling = 8
        self.bmp390.temperature_oversampling = 2

        time.sleep(3)
        self.base_altitude = self._calculate_base_altitude()
        self.altitude = self.bmp390.altitude - self.base_altitude
        self.previous_altitude = self.altitude

    def _calculate_base_altitude(self):
        altitudes = []
        start_time = time.time()
        while time.time() - start_time < 10:
            altitudes.append(self.bmp390.altitude)
        return np.mean(altitudes)


    def give_altitude(self):
        self.previous_altitude = self.altitude
        altitude = self.bmp390.altitude - self.base_altitude
        altitude = self.iir_filter.give_filtered(altitude)
        self.altitude = altitude
        return self.altitude

    def give_vertical_vel(self):
        vertical_vel = (self.altitude - self.previous_altitude) * conf.frequency
        return vertical_vel
