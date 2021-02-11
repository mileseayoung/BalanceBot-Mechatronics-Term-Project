# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:36:28 2021

@file       main_young.py
@author     Miles Young
@date       02/4/2021
@brief      <b> Temperature Collection Main Script </b> \n
@details    This script is used to collect temperature data for using the built-in 
            NUCLEO temperature sensor and an external Adafruit MCP9808 temperature 
            sensor breakout board. I2C communication is used to collect the external 
            temperature data, and temperature readings are taken every minute. The 
            time since the beginning of data collection, internal NUCLEO temp, 
            and external MCP9808 temp are all saved as one line in an external file 
            for every round of data collection. 
"""

import mcp9808_young
import pyb
import utime

## Create an ADC object measuring internal temperature of NUCLEO
adc = pyb.ADCAll(12,0x70000)

# Tare internal temperature reading
adc.read_vref()

## Define a variable to hold the temperature reading from the ADC object
inTemp = adc.read_core_temp()

## Define an object for I2C communication
i2cObject = pyb.I2C(1)

## Define the I2C bus address of the MCP9808 temperature sensor. Default address sourced from Adafruit spec sheet.
address = 0x18

## Create an MCP9808 object using the mcp9808 class, which takes an I2C object and the address of the temp sensor in the constructor
mcp = mcp9808_young.MCP9808(i2cObject,address)

## Define variable to hold the temperature reading from the MCP9808 temperature sensor
exTemp = mcp.celsius()

## Define variable to hold starting time
startTime = utime.ticks_ms()

## Define variable to hold updated current time
currTime = utime.ticks_ms()

## Define variable to hold time since beginning of data collection
time = utime.ticks_diff(currTime,startTime)

## Define interval between temperature readings
interval = 60

## Define run counter to keep track of temperature collection iterations
run = 1

## Define a limit for runs after which to end data collection (only valid for timed data collection)
#runLimit = 480

# OPERATIONAL CODE

# Check whether a valid I2C connection has been made
mcp.check()

# Open file in which to record internal temperature measurements for NUCLEO
with open ("Temperature.csv","w") as file:
    
    # Write column headers for .csv file
    file.write('Time [ms],Internal Temperature [degC], External Temperature [degC]\n')
    
    # Initiate data collection loop
    while True:
        try:
            # Sleep some amount of time
            utime.sleep(interval)
            # update current time in milliseconds
            currTime = utime.ticks_ms()
            # Update NUCLEO internal temperature measurement
            inTemp = adc.read_core_temp()
            # Print temp for debugging purposes
            #print('Internal Temp: ' + str(inTemp) + ' degC')
            # Update the external temperature measurement from the MCP9808 sensor
            exTemp = mcp.celsius()
            # Print temp for debugging purposes
            #print('External Temp: ' + str(exTemp) + ' degC')
            # Calculate time from beginning of data collection
            time = utime.ticks_diff(currTime,startTime)
            # Add time, internal temperature, and external temperature measurements as a new line in the file
            file.write('{:},{:.2f},{:.2f}\n'.format(time,inTemp,exTemp))
            # Print values to terminal so progress can be observed (only valid for timed data collection)
            #print('Completion {:.1f}%: {:.2f},{:.2f}'.format((run/runLimit)*100,inTemp,exTemp))
            # Update run counter
            run += 1
            
            # Break data collection loop if enough runs have been completed (only valid for timed data collection)
            #if run > runLimit:
                #break
            
        except KeyboardInterrupt:
            # Close the file to avoid loss of stored measurements
            print('Data collection terminated early'+'\r\n'+'File will close to avoid loss of data')
        
print('Data collection complete'+'\r\n'+'File will close automatically')