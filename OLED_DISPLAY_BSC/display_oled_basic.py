from machine import I2C
from ssd1306 import SSD1306_I2C

# old metadata
oled_width = 128
oled_height = 32

i2c_interface = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(oled_width, oled_height, i2c_interface)

oled.text("Hi Zian")
oled.show()

