# -*- coding: utf-8 -*-
"""
@file mcp9808.py
@brief This program establishes connection with MCP9808 temp sensor and will read the value
@details This program opens a line of I2C communication with the sensor and makes sure that it is the master device.
It gives the user three functions. They can check that the sensor is connected to the right adress my usinf the check funciton and
seeing if the manufacture ID is returned correctly. Once confirmed the function can then either return temperature measured from the sensor
in degrees Farenheight or Celsius. 
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
        
        if read_id != None:
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
        
        #Storing Upper Byte
        cel_upper = raw_temp[0]
        #Storing Lower Byte
        cel_lower = raw_temp[1]
        #Clearing Flag Bits
        cel_upper = cel_upper & 0x1F
        #Checking if Ta < 0deg C
        if cel_upper & 0x10:
            #Clear sign bit
            cel_upper = cel_upper & 0x0F
            read_temp = 256 - (cel_upper * 16 + cel_lower/16)
        else:
            read_temp = (cel_upper * 16 + cel_lower/16)
        return(read_temp)
    
    def farenheight(self):
        """
        @brief Reads temperature from sensor in Farenheight
        @details Pulls data from mem addr 5 and converts the byte string to an integer
        This integer is then returned by the function. Temperature conversion needs to be done
        since the sensor gives data in Celsius
        """
        raw_Ftemp = (self.temp_I2C.mem_read(2,addr=24,memaddr=5))
        #Storing Upper Byte
        far_upper = raw_Ftemp[0]
        #Storing Lower Byte
        far_lower = raw_Ftemp[1]
        #Clearing Flag Bits
        far_upper = far_upper & 0x1F
        #Checking if Ta < 0deg C
        if far_upper & 0x10:
            #Clear sign bit
            far_upper = far_upper & 0x0F
            read_temp = 256 - (far_upper * 16 + far_lower/16)
            #Converitng to Farenheight 
            read_temp = (read_temp * 1.8) + 32
        else:
            read_temp = (far_upper * 16 + far_lower/16)
            #Converting to Farenheight
            read_temp = (read_temp * 1.8) + 32
        return(read_temp)


## Test code for reading the temperature sensor and printing at an interval of every 1 second
