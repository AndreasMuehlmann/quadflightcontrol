import time

import board
import busio
import adafruit_bmp280

import config as conf
from iir_filter import IirFilter


class BMP280_Interface():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
        self.bmp280.sea_level_pressure = 1015.43
        self.bmp280.mode = adafruit_bmp280.MODE_NORMAL
        self.bmp280.standby_period = adafruit_bmp280.STANDBY_TC_500
        self.bmp280.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
        self.bmp280.iir_filter = adafruit_bmp280.IIR_FILTER_X16
        self.iir_filter_pos = IirFilter(0.8, 1) 
        self.iir_filter_vel = IirFilter(0.8, 1)

        time.sleep(2)
        self.previous_height = 0
        self.previous_height_vel = 0
        self.base_altitude = self.bmp280.altitude
        self.sampling_per_second = 20
        self.count_for_recalculation = conf.frequency / self.sampling_per_second
        self.count = 0

    def give_altitude(self):
        altitude = (self.bmp280.altitude - self.base_altitude) / 10
        return altitude
        # return self.iir_filter_pos.give_filtered(altitude)

    def give_height_vel(self):
        if self.count >= self.count_for_recalculation:
            height = self.bmp280.altitude - self.base_altitude
            height_vel = (height - self.previous_height) / self.sampling_per_second * 10
            self.previous_height = height
            self.previous_height_vel = height_vel
            self.count = 0
        else:
            height_vel = self.previous_height_vel

        self.count += 1
        return height_vel
        # return self.iir_filter_vel.give_filtered(height_vel) 
