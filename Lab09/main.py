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
from TouchDriver import TouchDriver
from Young_MotorDriver import MotorDriver
from EncoderDriver import EncoderDriver
from CLDRiver import CLDriver
from CLTask import CLTask
from bno055 import BNO055
import sys

# INITIALIZING COMPONENT DRIVER OBJECTS
###############################################################################

# MOTOR OBJECTS
## Enable/disable pin
pinSleep = Pin(Pin.cpu.A15)
## Fault pin
pinFault = Pin(Pin.cpu.B2)
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
## I2C SDA pin on NUCLEO
pinSDA = Pin(Pin.cpu.B8, Pin.IN, Pin.PULL_UP)
## I2C scl pin on NUCLEO
pinSCL = Pin(Pin.cpu.B9, Pin.IN, Pin.PULL_UP)
## I2C object
i2c = I2C(1)
## I2C address
address = 0x28
# Initialize I2C object
i2c.init(I2C.MASTER)
# Check validity of address
# Check IMU I2C comm. is valid
if i2c.is_ready(address):
    print(' IMU address ' + str(hex(address)) + ' verified')
else:
    print('Unable to verify IMU address ' + str(hex(address)) + '\n' + 'Program will exit')
    sys.exit()

## IMU object
IMU = BNO055(i2c,address,crystal=False)
# Mode integer value from IMU breakout board documentation
NDOF_MODE = 0x0c
IMU.mode(NDOF_MODE)

###############################################################################

# MOTOR CONTROLLER

## First controller gain for closed-loop feedback
K1 = 1
## Second controller gain for closed-loop feedback
K2 = 1
## Third controller gain for closed-loop feedback
K3 = 1
## Fourth controller gain for closed-loop feedback
K4 = 1

## Closed-loop object  
CLObject = CLDriver(K1,K2,K3,K4)

## Closed-loop FSM Task
ControlTask = CLTask(CLObject,Motor1,Motor2,Encoder1,Encoder2,TouchObject,IMU)

# RUN CONTROLLER FSM INDEFINITELY
while True:
    ControlTask.run()

   
    


