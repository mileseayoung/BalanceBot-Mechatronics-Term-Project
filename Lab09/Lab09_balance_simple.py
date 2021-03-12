# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 20:28:36 2021

@author: craig
"""

from EncoderDriver import EncoderDriver
from TouchDriver import TouchDriver
from Young_MotorDriver import MotorDriver

import utime
import pyb

pinA1 = pyb.Pin(pyb.Pin.cpu.B6)
## Define pin B1 object
pinB1 = pyb.Pin(pyb.Pin.cpu.B7)
## Define the timer to be used for encoder 1
timer1 = 4
## Define pin A2 object
pinA2 = pyb.Pin(pyb.Pin.cpu.C6)
## Define pin B2 object
pinB2 = pyb.Pin(pyb.Pin.cpu.C7)
## Define the timer to be used for encoder 2
timer2 = 8

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

#defining pin objects for touch panel
xp = pyb.Pin(pyb.Pin.board.PA7)
xm = pyb.Pin(pyb.Pin.board.PA1)
yp = pyb.Pin(pyb.Pin.board.PA6)
ym = pyb.Pin(pyb.Pin.board.PA0)

#defining dimensions of touch panel, and digital center point
w = 108
length = 186
center = [105,67]

touch = TouchDriver(xp,xm,yp,ym,w,length,center)


pinSleep = pyb.Pin(pyb.Pin.cpu.A15)
## Fault pin
pinFault = pyb.Pin(pyb.Pin.cpu.B2)
## Forward driving pin for motor 1
pinIN1 = pyb.Pin(pyb.Pin.cpu.B4)
## Reverse driving pin for motor 1
pinIN2 = pyb.Pin(pyb.Pin.cpu.B5)
## Forward driving pin for motor 2
pinIN3 = pyb.Pin(pyb.Pin.cpu.B0)
## Reverse driving pin for motor 2
pinIN4 = pyb.Pin(pyb.Pin.cpu.B1)
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

Motor1.setDuty(0)
Motor2.setDuty(1)
Motor1.enable()
Motor2.enable()
state = 0

startTime = utime.ticks_us()
        
## Defines the current time for the iteration and is overwritten at the beginning of each iteration
currTime = utime.ticks_us()

## Defines the interval after which another iteration will run as (pulses/PPS)
interval = 1500 # Spitballing here

## Time for which next iteration will run and is overwritten at the end of each iteration
nextTime = utime.ticks_add(startTime,interval)

gains = [-0.2,-0.19]

# Resistance of motor system
Resistance = 2.21 #ohms
#Motor Torque Constant
Kt = 13.8 #mNm/A
#Voltage supplied to the motor
Vdc = 3.3 #volts

try:
    while True:
        currTime = utime.ticks_us()

        # Specifying the next time the task will run
        if utime.ticks_diff(currTime, nextTime) >= 0:

            if state == 0:
                ## Init State
                input('Hold the board level with the ball resting in the cente of the board. Then Press Enter')
                # Update encoder positions to zero them on level position
                zeroX = 0
                Encoder1.setPosition(zeroX)
                
                zeroY = 0
                Encoder2.setPosition(zeroY)
                
                ball_rest = touch.read()
                print(ball_rest)
                
                input('System Calibrated. Press Enter to begin balancing Routine')
                state = 1
            #State for reading position of deviation of ball and platform from centerpoint
            if state == 1:
                #finding theta from 0 on X axis
                Encoder1.update()
                xtick = Encoder1.getPosition()
                X = Encoder1.tick2deg(xtick)
                
                X_dot = Encoder1.getDelta() / (interval*1e6)
                plat_paramX = [X,X_dot]
                
                #finding theta from 0 on Y axis
                Encoder2.update()
                ytick = Encoder2.getPosition()
                Y = Encoder2.tick2deg(ytick)
                Y_dot = Encoder2.getDelta() / interval*(1e6)
                
                plat_paramY = [Y,Y_dot]
                #print([Y,Y_dot])
                # reading Ball positoin
                '''
                #current_ball_pos = touch.read()
                #If the bal is still detected as being on the platform
                if current_ball_pos[0] == True:
                    X_ball = current_ball_pos[1]
                    Y_ball = current_ball_pos[2]
                    
                    x_ball_from_home = X_ball - ball_rest[1]
                    y_ball_from_home = Y_ball - ball_rest[2]
                '''
                state = 2
                
            #Controller state. Where motor values are found and applied
            if state == 2:
                '''
                In this state values are to be fed into a controller. The controller
                will then calculate a Torque output for a motor and that will be converted to a duty
                cycle that is then applied to the motor.
                '''
                
                InputTx = (plat_paramX[0] * (-gains[0])) + ((-gains[1])*plat_paramX[1])
                InputTy = (plat_paramY[0] * (-gains[0])) + ((-gains[1])*plat_paramY[1])
                
                Motorx_feed = ((Resistance / (Kt * Vdc)) * InputTx)*100
                Motory_feed = ((Resistance / (Kt * Vdc)) * InputTy)*100
                print([Motorx_feed,Motory_feed])
                
                Motor1.setDuty(Motorx_feed)
                Motor2.setDuty(Motory_feed)
                state = 1
            nextTime = utime.ticks_add(nextTime,int(interval))
except KeyboardInterrupt:
    Motor1.disable()
    Motor2.disable()
    print('Balancing has concluded ')

def TtoD(self,Torque):
    '''
    @brief Converts Torque to Duty cycle
    @details Takes a torque value supplied by the controller, for correcting balance, and converts
    it to a duty cycle that can be sent to the motor through PWM signal
    @param Torque Output Torque from controller required to balance board. Units assumed to be mN-M
    '''
    # Resistance of motor system
    Resistance = 2.21 #ohms
    #Motor Torque Constant
    Kt = 13.8 #mNm/A
    #Voltage supplied to the motor
    Vdc = 3.3 #volts
    
    Duty_decimal = ((Resistance / (Kt * Vdc)) * Torque)*100
    Duty_percent = Duty_decimal * 100
    return int(Duty_percent)


def Controller(self,gains,plat_param):
    '''
    @brief Closed Loop Controller for getting motor torques
    @details takes a gain matrix input and platform parameters matrix both as an array. Uses
    the form T = -k*x to spit out a motor torque value for the necessary axis.
    @param gains A matrix Of gain values K1 - K4 for the controller. input as a list
    @param plat_param Platform parameters for the controller must be in form [x_dot,Theta_dot,x,theta]
    '''
    T= (plat_param[0] * (-gains[0])) + ((-gains[1])*plat_param[1])
    return(T)
