import board
import busio
import adafruit_bmp280

import config as conf


class BMP280_Interface():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        bmp.sea_level_pressure = 1013.25
        self.previous_height = bmp.altitude

    def give_height_vel(self):
        height = bmp.altitude
        height_vel = (height - self.previous_height) * conf.frequency
        self.previous_height = height
        print("Höhe = {:.2f} m".format(altitude))
        return height_vel
