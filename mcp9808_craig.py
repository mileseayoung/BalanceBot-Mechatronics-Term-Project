# -*- coding: utf-8 -*-
"""
@file mcp9808.py
@brief This program establishes connection with MCP9808 temp sensor and will read the value

@author: craig
"""

import pyb
from pyb import I2C


class TempyGet:
    
    def __init__(self):
        self.temp_I2C = pyb.I2C(1,pyb.I2C.MASTER)
    
    def check(self):
        '''
        @brief This function checks to make sure the temperature sensor is connected at the given bus address.
        @details this module will check the sensor is connected properly by checking the value in
        the manufacturing ID register
        '''
        raw_id = (self.temp_I2C.mem_read(2,addr=24,memaddr=5))
        read_id = int.from_bytes(raw_id,"big")
        
        if read_id == 84:
            return("Device Connected Correctly")
        else:
            return("Device Connection error expected Manfac id 84 on addr 24 mem addr 6")
        #Code for checking this will be written when the sensor arrives
        
    def celsius(self):
        """
        @brief Reads temperature from sensor in Celsius
        @details Pulls data from mem addr 5 and converts the byte string to an integer
        This integer is then returned by the function. No temperature conversion needs to be done
        since the sensor gives data in Celsius
        """
        raw_temp = (self.temp_I2C.mem_read(2,addr=24,memaddr=5))
        read_temp = int.from_bytes(raw_temp,"big")
        return(read_temp)
    
    def farenheight(self):
        """
        @brief Reads temperature from sensor in Farenheight
        @details Pulls data from mem addr 5 and converts the byte string to an integer
        This integer is then returned by the function. Temperature conversion needs to be done
        since the sensor gives data in Celsius
        """
        raw_Ftemp = (self.temp_I2C.mem_read(2,addr=24,memaddr=5))
        read_Ftemp = int.from_bytes(raw_Ftemp,"big")
        conv_Ftemp = (read_Ftemp * 1.8 ) +32
        return(conv_Ftemp)


## Test code for reading the temperature sensor and printing at an interval of every 1 second
