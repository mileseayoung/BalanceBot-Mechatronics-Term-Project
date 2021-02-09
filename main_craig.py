# -*- coding: utf-8 -*-
"""
@file main_craig.py
@brief this will need to be saved as 'main.py'. This module records core and temperature sensor temperatures at a scheduled interval
@details This module utilizes a class created in mc9808_craig.py to perform I2C communicaiton with a sensor and retreive temperature info of the ambient
environment. this module also records the core temperature of the Nucleo. The module is set to record every minute over a span of 8 hours and store
this data in a CSV file on the nucleo. To terminate the program early the user can press "ctrl+c"

@author: craig
"""

import utime
import pyb
from mcp9808_craig import TempyGet
from pyb import I2C

#variable for measuring time
time = utime.ticks_ms()
# setting up object for measuring board core temperature
adcall = pyb.ADCAll(12,0x70000)
# timing interval. measures in microseconds. Set to 1 min
Temp = TempyGet()
Concheck = Temp.check()
print(Concheck)
runs = 0

with open ("temperature_recording.csv", "w") as log_file:
    try:
        while True:
          
            utime.sleep(60)
            # using adcall object with "read_core_temp" method to return core temp in celsius
            core_temp = adcall.read_core_temp()
            #will read mcp9808 sensor temperature
            senso_temp = Temp.celsius()
            print(senso_temp)
            #Writing the last entry to the file
            log_file.write ("{:},{:}\r\n".format(core_temp,senso_temp))
            runs += 1
              
            
            if runs > 480:
                break
    except KeyboardInterrupt:
        print('User has stopped recording early, The file will now be saved with the recorded data')

print ("The file has by now automatically been closed.")