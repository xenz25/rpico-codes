# Raspberry Pi PICO - Volt Meter
# Design By: Zian Jolo Catacutan
# 6/12/2023

from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
from utime import sleep as micro_sleep


# old metadata
oled_width = 128
oled_height = 32
oled_center = (int((oled_width/2) - 1), int((oled_height/2) - 1))
BANNER_TEXT = "Z VOLT"
ONE_CHAR_WIDTH = 5

# declarations
volt_meter_adc = ADC(Pin(28))
i2c_interface = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled_screen = SSD1306_I2C(oled_width, oled_height, i2c_interface)

# utility functions
def read_adc(adc_pin):
    return adc_pin.read_u16()

def read_voltage(adc_pin):
    ADC_VOLTAGE = 3.3
    MAXIMUM_ADC_READING = 65535.0
    REF_RESISTOR = { "R1" : 100000.0, "R2" : 10000.0 }

    # using voltage divider formula
    # vout = vin * R2/R1+R2
    vout = read_adc(adc_pin) * ADC_VOLTAGE / MAXIMUM_ADC_READING
    vin = vout / (REF_RESISTOR["R2"] / (REF_RESISTOR["R1"] + REF_RESISTOR["R2"]))
    return vin

def read_voltage_with_sampling(adc_pin):
    MAX_VOLT_SAMPLES = 10
    ERROR_MARGIN = 0.4
    sample_summation = 0.0
    sample = 0
    
    while sample < MAX_VOLT_SAMPLES:
        sample_summation += read_voltage(adc_pin)
        sample += 1
    
    samples_mean = sample_summation / float(MAX_VOLT_SAMPLES)
    voltage = round(samples_mean, 3) - ERROR_MARGIN
    return float(0) if voltage < 0.999 else voltage


oled_screen.text(BANNER_TEXT, oled_center[0] - int(len(BANNER_TEXT)/2)*ONE_CHAR_WIDTH, oled_center[1])
oled_screen.show()
sleep(3)
oled_screen.fill(0)

while True:
    reading = read_voltage_with_sampling(volt_meter_adc)
    display_text = "Voltage: {0} V".format(reading)
    
    print(display_text)
    oled_screen.text(display_text, 0, 0)
    oled_screen.show()
    
    micro_sleep(0.2)
    oled_screen.fill(0)
    