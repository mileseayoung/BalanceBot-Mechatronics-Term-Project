# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:11:55 2021

@file       BalanceBot.py
@author     Miles Young
@date       03/10/2021
@brief      <b> Balancing Platform Main Controller </b> \n
@details    This main script contains the controller programming for the balance bot system.
"""

from pyb import Pin, I2C
import utime
import usys
from TouchDriver import TouchDriver
from MotorDriver import MotorDriver
from EncoderDriver import EncoderDriver
from bno055 import BNO055

# INITIALIZING COMPONENT DRIVER OBJECTS
###############################################################################

# MOTOR OBJECTS
## Enable/disable pin
pinSleep = Pin(Pin.cpu.A15)
pinFault = Pin(Pin.cpu.PB2)
## Forward driving pin for motor 1
pinIN1 = Pin(Pin.cpu.B4)
## Reverse driving pin for motor 1
pinIN2 = Pin(Pin.cpu.B5)
## Forward driving pin for motor 2
pinIN3 = Pin(Pin.cpu.B0)
## Reverse driving pin for motor 2
pinIN4 = Pin(Pin.cpu.B1)
## Timer number for motor 1
timer1 = 3
## Timer number for motor 2
timer2 = 3
## Timer channel for pinIN1
channel1 = 1
## Timer channel for pinIN2
channel2 = 2
## Timer channel for pinIN3
channel3 = 3
## Timer channel for pinIN4
channel4 = 4
## Motor 1 Object
Motor1 = MotorDriver(1,pinSleep,pinFault,pinIN1,channel1,pinIN2,channel2,timer1) 
## Motor 2 object
Motor2 = MotorDriver(2,pinSleep,pinFault,pinIN3,channel3,pinIN4,channel4,timer2)

# ENCODER OBJECTS
## Define pin A1 object
pinA1 = Pin(Pin.cpu.B6)
## Define pin B1 object
pinB1 = Pin(Pin.cpu.B7)
## Define the timer to be used for encoder 1
timer1 = 4
## Define pin A2 object
pinA2 = Pin(Pin.cpu.C6)
## Define pin B2 object
pinB2 = Pin(Pin.cpu.C7)
## Define the timer to be used for encoder 2
timer2 = 8
## Define the pulses per cycle for each encoder
PPC = 4
## Define the cycles per rotation for each encoder
CPR = 1000
## Define the gear ratio for each encoder to motor
gearRatio = 4
## Encoder 1 Object
Encoder1 = EncoderDriver(pinA1,pinB1,timer1,PPC,CPR,gearRatio)
## Encoder 2 object
Encoder2 = EncoderDriver(pinA2,pinB2,timer2,PPC,CPR,gearRatio)

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
width = 108
## Platform length
length = 186
## Platform center coordinates
center = [105,67]   
## Touch panel driver object
TouchObject = TouchDriver(pinxp,pinxm,pinyp,pinym,width,length,center)
    
# IMU OBJECT
## I2C communication protocol
i2c = I2C(1)
## I2C address
address = 0x28
## IMU object
IMU = BNO055(i2c,address,crystal=False)
# Mode integer value from IMU breakout board documentation
NDOF_MODE = 0x0c
IMU.mode(NDOF_MODE)

###############################################################################

# MOTOR CONTROLLER

# Check IMU I2C comm. is valid
if i2c.is_ready(address):
    print(' IMU address ' + str(hex(address)) + ' verified')
else:
    print('Unable to verify IMU address ' + str(hex(address)) + '\n Program will exit')
    # Exit program
    usys.exit()    
    
# Calibrate IMU
input('Place the platform in a single stable position for a few seconds to allow the gyroscope to calibrate \n Press enter to begin calibration')

while True:
    # Delay 100 milliseconds
    utime.sleep_ms(100)
    # Check calibration status
    if IMU.calibrated():
        break
    else:
        print('Calibrating: ' + str(IMU.cal_status()[1]*(100/3)) + '%')
 
# Enable motors
Motor1.enable()
Motor2.enable()        

# Change IMU mode to gyro only for faster scans
GYRONLY_MODE = 0x03
IMU.mode(GYRONLY_MODE = 0x03)

# Calibrate encoders
# Calibrate x-axis
while True:
    if IMU.gyro()[0] != 0 and IMU.gyro()[0] < 0:
        Motor1.setDuty(20)
    elif IMU.gyro()[0] !=0 and IMU.gyro()[0] > 0:
        Motor1.setDuty(-20)
    elif IMU.gyro()[0] == 0:
        Encoder1.setPosition(0)
        break
    else:
        pass # Error Handling
# Calibrate y-axis
while True:
    if IMU.gyro()[1] != 0 and IMU.gyro()[1] < 0:
        Motor2.setDuty(20)
    elif IMU.gyro()[1] !=0 and IMU.gyro()[1] > 0:
        Motor2.setDuty(-20)
    elif IMU.gyro()[1] == 0:
        Encoder2.setPosition(0)
        break
    else:
        pass # Error handling
    
print('Encoder calibration complete')

# CONTROLLER PROGRAM
def angleCalc():
    '''
    @brief      <b> Solve for Angle Via Numerical Integration </b>
    @details    ...
    '''
 

def CLfeedback():
    '''
    @brief      <b> Closed-loop Feedback Control for x-axis </b>
    @details    ...
    '''
    
    ## Measure angle about x-axis
    theta = IMU.euler()[1]
    ## Measure first time derivative of angle about x-axis
    thetadot = IMU.gyro()[0]
    
    
    ## Measure angle about y-axis
    theta = IMU.euler()[2]
    ## Measure first time derivative of angle about y-axis
    thetadot = IMU.gyro()[1]

    ## Measure x-position
    if TouchObject.position[0]:
        x = TouchObject.position()[1]
        y = TouchObject.position()[2]
    else:
        # Recalibrate the platform
    # Feedback Equation
    
       
def yCL():
    '''
    @brief      <b> Closed-loop Feedback Control for y-axis </b>
    @details    ...
    '''
    
    


# Input: x, y, theta_x, theta_y
# Output: Torque (Duty Cycle)
## Start time 
startTime = utime.ticks_us()
## Current time
currTime = utime.ticks_us()

while True:
    currTime = utime.ticks_us()
    yCL()
    xCL()
    



