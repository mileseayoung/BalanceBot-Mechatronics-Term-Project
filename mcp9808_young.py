# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:09:13 2021

@file       mcp9808_young.py
@author     Miles Young
@date       02/4/2021
@brief      <b> ... </b> \n
@details    ...
"""
from pyb import I2C

class MCP9808:
    '''
    @brief      <b> MCP9808 temperature sensor breakout board class </b> \n
    @details    ...
    '''
    
    def __init__(self,i2cObject,address):
        '''
        @brief              <b> MCP9808 semperature sensor class constructor </b> \n
        @details            ...
        @param i2cObject    The I2C communication protocol object which is to be used for communication between the NUCLEO MCU and MCP9808 temperature sensor
        @param address      The I2C bus address of the MCP9808 temperature sensor 
        '''
        
        ## Define class-specific I2C object from user-specified I2C object
        self.i2c = i2cObject
        
        ## Define I2C bus address for MCP9808 from user-specified address
        self.address = address
        
        ## Construct I2C object for communication with MCP9808
        self.i2c.init(I2C.MASTER)
    
    
    def check(self):
        '''
        @brief      <b> Verify sensor address </b> \n
        @details    ...
        '''
        
        if self.i2c.is_ready(self.address):
            print('Address verified')
        else:
            print('Unable to verify address')
        
        
    def celsius(self):
        '''
        @brief      <b> Return measured temperature in degrees Celcius </b> \n
        @details    ...
        '''
        # Read raw temp data from sensor via I2C
        rawTemp = self.i2c.mem_read(2,addr=self.address,memaddr=5)
        # Convert raw temp data from bytes to integer value
        Temp = int.from_bytes(rawTemp,"big")
        
        return(Temp)
        
    def fahrenheit(self):
        '''
        @brief      <b> Return measured temperature in degrees Fahrenheit </b> \n
        @details    ...
        '''
        
        # Read raw temp data from sensor via I2C
        rawTemp = self.i2c.mem_read(2,addr=24,memaddr=5)
        # Convert raw temp data from bytes to integer value
        Temp = int.from_bytes(rawTemp,"big")
        # Convert temperature reading from degC to degF
        Temp = (Temp*1.8) + 32
        
        return(Temp)
    
 
if __name__ == '__main__':
    # Test code
    one = 1