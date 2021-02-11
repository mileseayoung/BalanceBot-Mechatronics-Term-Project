# -*- coding: utf-8 -*-
"""
@file main_craig.py
@brief this will need to be saved as 'main.py'. This module records core and temperature sensor temperatures at a scheduled interval
@details This module utilizes a class created in mc9808_craig.py to perform I2C communicaiton with a sensor and retreive temperature info of the ambient
environment. this module also records the core temperature of the Nucleo. The module is set to record every minute over a span of 8 hours and store
this data in a CSV file on the nucleo. To terminate the program early the user can press "ctrl+c". To run this program automatically on boot of the board save as "main.py"
Source Code: https://bitbucket.org/MilesYoung/lab-4/src/master/main_craig.py

@author: Craig Kimball
"""

import utime
import pyb
from mcp9808_craig import TempyGet
from pyb import I2C

#variable for measuring time
time = utime.ticks_ms()
# setting up object for measuring board core temperature
adcall = pyb.ADCAll(12,0x70000)
pinA5 = pyb.Pin(pyb.Pin.cpu.A5,pyb.Pin.OUT_PP)
pinA5.low()
#defining class object
Temp = TempyGet()
Concheck = Temp.check()
if Concheck == False:
    print('Connection not established to sensor. Manufactuer ID does not match')
    exit()
else:
    print('Device Connected')

runs = 0
pinA5.high()
with open ("temperature_recording.csv", "w") as log_file:
    file.write('Time [ms],Internal Temperature [degC], External Temperature [degC]\n')
    
    try:
        while True:
          
            utime.sleep(60)
            
            # using adcall object with "read_core_temp" method to return core temp in celsius
            core_temp = adcall.read_core_temp()
            #will read mcp9808 sensor temperature
            senso_temp = Temp.celsius()
            print(senso_temp)
            runs += 1
            #Writing the last entry to the file. Using runs as a timer
            log_file.write ("{:},{:},{:}\n".format(runs,core_temp,senso_temp))
            
              
            
            if runs > 480:
                break
    except KeyboardInterrupt:
        print('User has stopped recording early, The file will now be saved with the recorded data')

print ("The file has by now automatically been closed.")
pinA5.low()