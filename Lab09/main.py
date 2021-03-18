# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:11:55 2021

@file       main.py
@author     Miles Young, Craig Kimball
@date       03/10/2021
@brief      <b> Balancing Platform Main Controller </b> \n
@details    This main script contains the controller programming for the balance bot system. \n
            Source -- https://bitbucket.org/MilesYoung/lab-4-term-project/src/master/Lab09/main.py
"""

from pyb import Pin
from TouchDriver import TouchDriver
from MotorDriver import MotorDriver
from EncoderDriver import EncoderDriver
from CLDRiver import CLDriver
from CLTask import CLTask

# INITIALIZING COMPONENT DRIVER OBJECTS
###############################################################################

# MOTOR OBJECTS
## Enable/disable pin
pinSleep = Pin(Pin.cpu.A15)
## Fault pin for motor 1
pinFault1 = Pin(Pin.cpu.B2)
## Fault pin for motor 2
pinFault2 = Pin(Pin.cpu.C13)

## Forward driving pin for motor 1
pinIN1 = Pin(Pin.cpu.B4)
## Reverse driving pin for motor 1
pinIN2 = Pin(Pin.cpu.B5)
## Forward driving pin for motor 2
pinIN3 = Pin(Pin.cpu.B0)
## Reverse driving pin for motor 2
pinIN4 = Pin(Pin.cpu.B1)
## Timer number for motor 1 & 2
motorTimer = 3
## Timer channel for pinIN1
channel1 = 1
## Timer channel for pinIN2
channel2 = 2
## Timer channel for pinIN3
channel3 = 3
## Timer channel for pinIN4
channel4 = 4
## Motor 1 Object
Motor1 = MotorDriver(1,pinSleep,pinFault1,pinIN1,channel1,pinIN2,channel2,motorTimer) 
## Motor 2 object
Motor2 = MotorDriver(2,pinSleep,pinFault2,pinIN3,channel3,pinIN4,channel4,motorTimer)

# ENCODER OBJECTS
## Define pin A1 object
pinA1 = Pin(Pin.cpu.B6)
## Define pin B1 object
pinB1 = Pin(Pin.cpu.B7)
## Define the timer to be used for encoder 1
encTimer1 = 4
## Define pin A2 object
pinA2 = Pin(Pin.cpu.C6)
## Define pin B2 object
pinB2 = Pin(Pin.cpu.C7)
## Define the timer to be used for encoder 2
encTimer2 = 8
## Define the pulses per cycle for each encoder
PPC = 4
## Define the cycles per rotation for each encoder
CPR = 1000
## Define the gear ratio for each encoder to motor
gearRatio = 4
## Encoder 1 Object
Encoder1 = EncoderDriver(pinA1,pinB1,encTimer1,PPC,CPR,gearRatio)
## Encoder 2 object
Encoder2 = EncoderDriver(pinA2,pinB2,encTimer2,PPC,CPR,gearRatio)

# TOUCH PANEL OBJECT 
## Positive x-dir touch panel pin
pinxp = Pin(Pin.cpu.A7)
## Negative x-dir touch panel pin
pinxm = Pin(Pin.cpu.A1)
## Positive y-dir touch panel pin
pinyp = Pin(Pin.cpu.A6)
## Negative y-dir touch panel pin
pinym = Pin(Pin.cpu.A0)
# Define platform dimensions
## Platform width
width = 0.108
## Platform length
length = 0.186
## Platform center coordinates
center = [0.105,0.067]   
## Touch panel driver object
TouchObject = TouchDriver(pinxp,pinxm,pinyp,pinym,width,length,center)

###############################################################################

# MOTOR CONTROLLER
# Motor 1
## State-space controller gain assigned to time derivative of ball position for closed-loop feedback
K11 = -7 # units N-s
## State-space controller gain assigned to time derivative of platform angle for closed-loop feedback
K12 = -15 # units N-m-s
## State-space controller gain assigned to ball position for closed-loop feedback
K13 = -.7 # units N
## State-space controller gain assigned to platform angle for closed-loop feedback
K14 = -700 # units N-m

# Motor 2
## State-space controller gain assigned to time derivative of ball position for closed-loop feedback
K21 = -4 # units N-s
## State-space controller gain assigned to time derivative of platform angle for closed-loop feedback
K22 = -20 # units N-m-s
## State-space controller gain assigned to ball position for closed-loop feedback
K23 = -.3 # units N
## State-space controller gain assigned to platform angle for closed-loop feedback
K24 = -1200# units N-m

## Measured internal motor resistance, units Ohms
resistance = 2.21

## Measured motor torque constant, units mN-m/A
Kt = 13.8

## DC voltage supplied to motor, units V
Vdc = 12

## Closed-loop object 1 assigned to motor 1
CLObject1 = CLDriver(K11,K12,K13,K14,resistance,Kt,Vdc)
## Closed-loop object 2 assigned to motor 2
CLObject2 = CLDriver(K21,K22,K23,K24,resistance,Kt,Vdc)


## Closed-loop FSM Task
# Note: if dbg = True, the task will not run within the time constraints of the interval, causing worse performance.
CLTask = CLTask(CLObject1,CLObject2,Motor1,Motor2,Encoder1,Encoder2,TouchObject,dbg=True)

# RUN CONTROLLER
Motor1.enable()
Motor1.enable()

# Implement a try statement that accounts for KeyboardInterrupt and safely disbles the motors and saves data into a .csv
try:
    # Run CLTask indefinitely
    while True:
        CLTask.run()

# If CTRL+C is pressed        
except KeyboardInterrupt:
    Motor1.disable()
    Motor2.disable()
    Motor1.setDuty(0)
    Motor2.setDuty(0)
    
    # Open .csv as write-enabled
    with open ("ClosedLoopResponse.csv","w") as file:
        # Assign column headers
        file.write('Time [us],Motor 1 Duty Cycle [%], Motor 2 Duty Cycle [%]\n')
        # Populate .csv columns with data
        for n in range(len(CLTask.timeArray)):
            file.write('{:},{:},{:}\n'.format(CLTask.timeArray[n],CLTask.dutyArray1[n],CLTask.dutyArray2[n]))
    
    # Notify user that program has concluded
    print('Closed-loop response recorded as "ClosedLoopResponse.csv"')
    print('Balancing concluded')

   
    



