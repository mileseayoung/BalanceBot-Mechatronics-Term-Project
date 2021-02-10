# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:09:13 2021

@file       mcp9808_young.py
@author     Miles Young
@date       02/4/2021
@brief      <b> MCP9808 temperature sensor breakout board I2C class </b> \n
@details    This script defines a class for I2C communication with the Adafruit 
            MCP9808 temperature sensor breakout board, as well as lines of test 
            code which initiate only when the script is run independently.
"""
from pyb import I2C

class MCP9808:
    '''
    @brief      <b> MCP9808 temperature sensor breakout board I2C class </b> \n
    @details    This class is used for I2C communication between the NUCLEO and 
                the MCP9808 temperature sensor breakout board. It has methods for 
                checking the validity of the I2C connection between the NUCLEO 
                and MCP9808, reading the temperature in degC, and reading the temperature 
                in degF.
    '''
    
    def __init__(self,i2cObject,address):
        '''
        @brief              <b> MCP9808 semperature sensor class constructor </b> \n
        @details            Two inputs are required to construct an MCP9808 breakout 
                            board temperature sensor I2C communication object: 
                            first, a pyb.I2C object, and second, the address of 
                            the MCP9808 in the I2C bus. The constructor then defines 
                            a class-specific I2C object, defined as a "master" (yuck), 
                            and a class-specific variable to hold the MCP9808 address.
        @param i2cObject    The I2C communication protocol object which is to be 
                            used for communication between the NUCLEO MCU and MCP9808 
                            temperature sensor
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
        @details    This method uses the pyb.I2C class method is_ready(addr), 
                    with the sensor I2C address as an input, to verify if a valid 
                    connection has been made between the NUCLEO and sensor.
        '''
        
        if self.i2c.is_ready(self.address):
            print('Address ' + str(self.address) + ' verified')
        else:
            print('Unable to verify address ' + str(self.address))
        
        
    def celsius(self):
        '''
        @brief      <b> Return measured temperature in degrees Celcius </b> \n
        @details    This method uses the pyb.I2C class method mem_read() to read 
                    the sensor temperature into a 2-byte bytearray. The address 
                    of the sensor and the memory address for the data is also 
                    specified. It then manipulates the raw byte data to represent 
                    the temperature in degrees Celsius.
        '''
        # Read raw temp data from sensor via I2C
        rawTemp = self.i2c.mem_read(2,addr=24,memaddr=5)
        # Parse raw data from 2-byte bytearray
        upperByte = rawTemp[0]
        lowerByte = rawTemp[1]
        
        # THIS CODE IS BASED ON C CODE PROVIDED IN ADAFRUIT MCP9808 DATA SHEET
        # Check flag bits
        if upperByte & 0x80 == 0x80:
            pass
        elif upperByte & 0x40 == 0x40:
            pass
        elif upperByte & 0x20 == 0x20:
            pass
        # Clear flag bits
        upperByte &= 0x1F
        
        # If Ta < 0 degC
        if upperByte & 0x10 == 0x10:
            # Clear sign
            upperByte &= 0x0F
            # Calculate temperature reading in degC
            temp = 256 - (upperByte*16 + lowerByte/16)
        # If Ta >= 0 degC
        else:
            # Calculate temperature reading in degC
            temp = (upperByte*16 + lowerByte/16)
        
        return(temp)
        
    def fahrenheit(self):
        '''
        @brief      <b> Return measured temperature in degrees Fahrenheit </b> \n
        @details    his method uses the pyb.I2C class method mem_read() to read 
                    the sensor temperature into a 2-byte bytearray. The address 
                    of the sensor and the memory address for the data is also 
                    specified. It then manipulates the raw byte data to represent 
                    the temperature in degrees Fahrenheit.
        '''
        
        # Read raw temp data from sensor via I2C
        rawTemp = self.i2c.mem_read(2,addr=24,memaddr=5)
        # Parse raw data from 2-byte bytearray
        upperByte = rawTemp[0]
        lowerByte = rawTemp[1]
        
        # THIS CODE IS BASED ON C CODE PROVIDED IN ADAFRUIT MCP9808 DATA SHEET
        # Check flag bits
        if upperByte & 0x80 == 0x80:
            pass
        elif upperByte & 0x40 == 0x40:
            pass
        elif upperByte & 0x20 == 0x20:
            pass
        # Clear flag bits
        upperByte &= 0x1F
        
        # If Ta < 0 degC
        if upperByte & 0x10 == 0x10:
            # Clear sign
            upperByte &= 0x0F
            # Calculate temperature reading in degC
            temp = 256 - (upperByte*16 + lowerByte/16)
        # If Ta >= 0 degC
        else:
            # Calculate temperature reading in degC
            temp = (upperByte*16 + lowerByte/16)
        
        # Convert temp from degC to degF
        temp = (temp * 1.8) + 32
        
        return(temp)
    
 
if __name__ == '__main__':
    # Test code
    
    # Create I2C object using BUS 1
    i2c = I2C(1)
    # Define I2C address for MCP9808 sensor
    address = 0x18
    # Create object in class MCP9808
    mcp = MCP9808(i2c,address)
    # Check if valid connection has been made
    mcp.check()
    # Test temp reading in degC
    print(str(mcp.celsius()))
    # test temp reading in degF
    print(str(mcp.fahrenheit()))
    
    