# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:05:54 2021

@file       TempSensor_young.py
@author     Miles Young
@date       02/4/2021
@brief      <b> ... </b> \n
@details    ...
"""
import pyb
import utime

## Create an ADC object measuring internal temperature of NUCLEO
adc = pyb.ADCAll(12,0x70000)

## Define a variable to hold the temperature reading from the ADC object
temp = adc.read_channel(16)

## Define variable to hold starting time
startTime = utime.ticks_ms()

## Define interval between temperature readings
interval = 60000

## Define variable to hold updated current time
currTime = utime.ticks_ms()

## Define variable to 

with open ("InternalTemp.ext","w") as file:
    # Open file in which to record internal temperature measurements for NUCLEO
    try:
        # Sleep some amount of time
        utime.sleep(5)
        # Update temperature measurement
        temp = adc.read_core_temp()
        # Add this measurement as a new line in the file
        file.write('{:}\r\n'.format(temp))
    
    except KeyboardInterrupt:
        # Close the file to avoid loss of stored measurements
        file.close()
    