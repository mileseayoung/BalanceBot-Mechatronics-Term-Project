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
inTemp = adc.read_core_temp()

## Define an object for I2C communication
i2cObject = pyb.I2C(2)

## Define the I2C bus address of the MCP9808 temperature sensor. Default address sourced from Adafruit spec sheet.
address = 0x18

## Create an MCP9808 object using the mcp9808 class, which takes an I2C object and the address of the temp sensor in the constructor
mcp = mcp9808_young.MCP9808(i2cObject,address)

## Define run counter to keep track of temperature collection iterations
run = 0

with open ("InternalTemp.ext","w") as file:
    # Open file in which to record internal temperature measurements for NUCLEO
    while True:
        try:
            # Sleep some amount of time
            utime.sleep(5)
            # Update temperature measurement
            inTemp = adc.read_core_temp()
            # Update the external temperature measurement from the MCP9808 sensor
            exTemp = mcp.celsius()
            # Add this measurement as a new line in the file
            file.write('{:},{:}\r\n'.format(inTemp,exTemp))
            # Update run counter
            run += 1
            
            if run > 4:
                break
            
        except KeyboardInterrupt:
            # Close the file to avoid loss of stored measurements
            print('Data collection terminated early'+'\r\n'+'File will close to avoid loss of data')
            break
        
print('Data collection complete'+'\r\n'+'File will close automatically')