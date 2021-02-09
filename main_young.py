# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:36:28 2021

@file main_young.py
@author     Miles Young
@date       02/4/2021
@brief      <b> ... </b> \n
@details    ...
"""

import mcp9808_young
import pyb
import utime

## Create an ADC object measuring internal temperature of NUCLEO
adc = pyb.ADCAll(12,0x70000)

## Define a variable to hold the temperature reading from the ADC object
inTemp = adc.read_channel(16)

## Define an object for I2C communication
i2cObject = pyb.I2C(1)

## Define the I2C bus address of the MCP9808 temperature sensor. Default address sourced from Adafruit spec sheet.
address = 0x18

## Create an MCP9808 object using the mcp9808 class, which takes an I2C object and the address of the temp sensor in the constructor
mcp = mcp9808_young.MCP9808(i2cObject,address)

with open ("InternalTemp.ext","w") as file:
    # Open file in which to record internal temperature measurements for NUCLEO
    try:
        # Sleep some amount of time
        utime.sleep(10)
        # Update temperature measurement
        inTemp = adc.read_core_temp()
        # Add this measurement as a new line in the file
        file.write('{:}\r\n'.format(inTemp))
    
    except KeyboardInterrupt:
        # Close the file to avoid loss of stored measurements
        file.close()