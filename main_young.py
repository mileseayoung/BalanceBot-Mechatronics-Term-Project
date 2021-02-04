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
adc = pyb.ADCAll(16,0x70000)

## Define a variable to hold the temperature reading from the ADC object
inTemp = adc.read_channel(16)




with open ("InternalTemp.ext","w") as file:
    # Open file in which to record internal temperature measurements for NUCLEO
    try:
        # Sleep some amount of time
        utime.sleep(10)
        # Update temperature measurement
        temp = adc.read_channel(16)
        # Add this measurement as a new line in the file
        file.write('{:}\r\n'.format(inTemp))
    
    except KeyboardInterrupt:
        # Close the file to avoid loss of stored measurements
        file.close()