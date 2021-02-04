# -*- coding: utf-8 -*-
"""
@file Lab04_board_craig.py
@brief this will need to be saved as 'main.py'. This module records core and temperature sensor temperatures at a scheduled interval

@author: craig
"""

import utime
import pyb
import mcp9808.py

#variable for measuring time
starttime = utime.ticks.ms()
# setting up object for measuring board core temperature
adcall = pyb.ADCAll(12,0x70000)
# timing interval. measures in microseconds. Set to 1 min
interval = 60000000
nextime = utime.ticks.add(starttime,interval)

currtime = utime.ticks.ms

runs = 0

with open ("temperature_recording", "w") as log_file:
    while True:
      
        if utime.ticks.dif(currtime,nextime) >=0:
            # using adcall object with "read_core_temp" method to return core temp in celsius
            core_temp = adcall.read_core_temp()
            #will read mcp9808 sensor temperature
            senso_temp = "object.celsius()"
            #Writing the last entry to the file
            log_file.write ("{:},{:}\r\n".format(core_temp,senso_temp))
            runs += 1
            nextime = utime.ticks.add(nextime,interval)
        


with open ("temperature_recording", "w") as a_file:
    for line in lines_of_text:
        a_file.write ("{:},{:}\r\n".format(core_temp,senso_temp), line)
        # ...
print ("The file has by now automatically been closed.")