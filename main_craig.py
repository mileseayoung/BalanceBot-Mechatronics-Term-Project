# -*- coding: utf-8 -*-
"""
@file main_craig.py
@brief this will need to be saved as 'main.py'. This module records core and temperature sensor temperatures at a scheduled interval

@author: craig
"""

import utime
import pyb
import mcp9808.py

#variable for measuring time
time = utime.ticks.ms()
# setting up object for measuring board core temperature
adcall = pyb.ADCAll(12,0x70000)
# timing interval. measures in microseconds. Set to 1 min


runs = 0

with open ("temperature_recording", "w") as log_file:
    try:
        while True:
          
            time.sleep(60000000)
            # using adcall object with "read_core_temp" method to return core temp in celsius
            core_temp = adcall.read_core_temp()
            #will read mcp9808 sensor temperature
            senso_temp = "object.celsius()"
            #Writing the last entry to the file
            log_file.write ("{:},{:}\r\n".format(core_temp,senso_temp))
            runs += 1
                
            
            if runs > 480:
                break
    except KeyboardInterrupt:
        print('User has stopped recording early, The file will now be saved with the recorded data')

print ("The file has by now automatically been closed.")