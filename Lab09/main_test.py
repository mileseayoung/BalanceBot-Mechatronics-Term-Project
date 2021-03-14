# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 18:46:08 2021

@author: Miles
"""
from pyb import Pin
from Young_MotorDriver import MotorDriver
from EncoderDriver import EncoderDriver

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
Motor1 = MotorDriver(1,pinSleep,pinFault,pinIN1,channel1,pinIN2,channel2,motorTimer) 
## Motor 2 object
Motor2 = MotorDriver(2,pinSleep,pinFault,pinIN3,channel3,pinIN4,channel4,motorTimer)

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


Motor1.enable()
Motor2.enable()


# Prompt user input when ready
input('Set platform in equilibrium and then press Enter to calibrate')

# Zero encoder positions so that all angle readings are absolute
Encoder1.setPosition(0)
Encoder2.setPosition(0)

try:
    while True:
        Encoder1.update()
        Encoder2.update()
        
        EncPos1 = Encoder1.getPosition()
        EncPos2 = Encoder2.getPosition()
        
        print('Encoder 1: {:}, Encoder 2: {:}'.format(EncPos1,EncPos2))
        
        if (EncPos1 < 660) and (EncPos1 > -159):
            Motor1.setDuty(50)
        else:
            Motor1.disable()
            
        if (EncPos2 < 600) and (EncPos2 > -170):
            Motor2.setDuty(50)
        else:
            Motor2.disable()
            
except KeyboardInterrupt:
    Motor1.disable()
    Motor2.disable()
    
    


