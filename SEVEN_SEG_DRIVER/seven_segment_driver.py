#-------------------------------------------------------------------------------
# Name:        seven_segment_driver
# Purpose: A library that handles all communications to a 7 segment Display
#
# Author:      Zian Jolo M. Catacutan
#
# Created:     28/10/2021
# Copyright:   (c) xenxi 2021
#-------------------------------------------------------------------------------

from machine import Pin

class SevSeg:
    #constants
    COMMON_CATHODE = 0
    COMMON_ANODE = 1
    
    #codes for the seven segment display in common cathode and common anode
    __COMMON_CATHODE_CODES = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x67, 0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71]
    __COMMON_ANODE_CODES = [0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x98, 0x88, 0x83, 0xc6, 0xa1, 0x86, 0x8e]
    __ALLOWABLE_NUMBER_OF_PINS = 7
    
    def __init__(self, seven_seg_pins = [], segment_type = COMMON_ANODE):
        '''seven_seg_pins - Pins shoud be in order that maps a-g. Decimal Point is not supported
           segment_type - must be one of the SevSeg.COMMON_ANODE or SevSeg.COMMON_CATHODE'''
        if len(seven_seg_pins) < self.__ALLOWABLE_NUMBER_OF_PINS:
            raise Exception("insufficient number of pins provided")
        self.seven_seg_pins = seven_seg_pins
        self.segment_type = segment_type
        self.__init_pins() #call initialize pins
        
    def __init_pins(self):
        '''Internal method that initialize the pins to output'''
        for i in range(len(self.seven_seg_pins)):
            self.seven_seg_pins[i] = Pin(self.seven_seg_pins[i], Pin.OUT)
        
    def fill(self, value = 0):
        '''Control all segment state, if 0 all segments are off, if 1 all segments are on.
           Both conditions are true in COMMON ANODE and COMMON CATHODE'''
        if self.segment_type == self.COMMON_ANODE:
            value = not value
        for pin in self.seven_seg_pins:
            pin.value(value)
            
    def __bitRead(self, bit, value):
        '''Internal methood that read the bit at position bit of the provided value'''
        return 1 if (value >> bit) & 1 else 0
            
    def writeNumeric(self, num = 0):
        '''Display the provided num value into the seven segment display. 10-15 are hex coded'''
        if num < 0 or num > 15:
            raise Exception("0-15 is the only permitted value")
        for segment in range(0, self.__ALLOWABLE_NUMBER_OF_PINS):
            self.seven_seg_pins[segment].value(self.__bitRead(segment, self.__COMMON_ANODE_CODES[num] if self.segment_type == self.COMMON_ANODE else self.__COMMON_CATHODE_CODES[num]))
    
    def test(self, speed = 200):
        '''A utility function to test the 7 segment display'''
        import utime
        for i in range(0, 16):
            self.writeNumeric(i)
            utime.sleep_ms(speed)
