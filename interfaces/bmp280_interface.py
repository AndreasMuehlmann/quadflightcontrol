import board
import busio
import adafruit_bmp280


class BMP280_Interface():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
        self.bmp280.sea_level_pressure = 1013.25
        self.bmp280.mode = adafruit_bmp280.MODE_NORMAL
        self.bmp280.standby_period = adafruit_bmp280.STANDBY_TC_500
        self.bmp280.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
        self.bmp280.iir_filter = adafruit_bmp280.IIR_FILTER_X16

    def give_altitude(self, base_altitude):
        return self.bmp280.altitude - base_altitude
