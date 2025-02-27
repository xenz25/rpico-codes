from machine import Pin
from seven_segment_driver import *
import utime

seven_segment = SevSeg([pin for pin in range(21, 14, -1)], SevSeg.COMMON_ANODE)

while 1:
    seven_segment.test()

        