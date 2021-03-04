# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 09:03:22 2020

@file           MotorDriver.py
@author         Miles Young
@date           11/10/2020
@brief          A driver for DC motors.\n
@details        This code contains a MotorDriver class which allows for the creation of a motor object. It includes 
                methods for enabling and disabling the motor, as well as setting the duty cycle.\n
                Sourcecode: https://bitbucket.org/MilesYoung/me305_me405_labs/src/master/Lab%207/MotorDriver.py
"""

import pyb

class MotorDriver:
    '''
    @brief          This class implements a motor driver for the ME305/405 board.
    '''
    
    def __init__(self,motorNum,pinSleep,pinIN1,channel1,pinIN2,channel2,timNum):
        '''
        @brief          Creates a motor dirver by initializing GPIO pins and turning the motor off for safety.
        @param motorNum A number identifier for the motor object.
        @param pinSleep A pyb.Pin object to use as the enable pin.
        @param pinIN1   A pyb.Pin object to use as the input to half bridge 1.
        @param channel1 A number identifier for the timer channel for pinIN1.
        @param pinIN2   A pyb.Pin object to use as the input to half bridge 2.
        @param channel2 A number identifier for the timer channel for pinIN2
        @param timNum   A number identifier for the timer used in PWM generation on pinIN1 and pinIN2.
        '''
        
        print('Motor Driver ' + str(motorNum) + ' created')
        
        ## Identifier for the motor object.
        self.motorNum = motorNum
        
        ## Defines local object for enable pin
        self.pinSleep = pinSleep
        
        ## Defines local object for IN1 pin
        self.pinIN1 = pinIN1
        
        ## Defines local object for IN2 pin
        self.pinIN2 = pinIN2
        
        ## Defines local variable for the timer
        self.timer = pyb.Timer(timNum,freq=20000)
        
        ## Defines timer channel for pinIN1 PWM function
        self.timch1 = self.timer.channel(channel1,pyb.Timer.PWM, pin=self.pinIN1)
        
        ## Defines the timer channel for pinIN2 PWM function
        self.timch2 = self.timer.channel(channel2,pyb.Timer.PWM, pin=self.pinIN2)
        
        
    def enable(self):
        '''
        @brief          Turns the enable pin high, allowing the motor to move
        '''
        
        #print('Enabling Motor ' + str(self.motorNum))
        self.pinSleep.high()
        
        
    def disable(self):
        '''
        @brief          Turns the enable pin low, disabling motor movement
        '''
        
        #print('Disabling Motor ' + str(self.motorNum))
        self.pinSleep.low()
        
        
    def setDuty(self,duty):
        '''
        @brief          Sets the duty cycle of the motor
        @param duty     The desired duty cycle, either positive for forward movement or negative for reverse movement
        '''
        
        if duty > 0 and duty <= 100:
            self.timch1.pulse_width_percent(duty)
            self.timch2.pulse_width_percent(0)
        elif duty < 0 and duty >= -100:
            self.timch1.pulse_width_percent(0)
            self.timch2.pulse_width_percent(abs(duty))
        elif duty == 0:
            self.timch1.pulse_width_percent(duty)
            self.timch2.pulse_width_percent(duty)
        else:
            print('Duty cycle ' + str(duty) +  ' is out of bounds')
            
    def brake(self):
        '''
        @brief          Brakes the motor
        '''
        
        self.timch1.pulse_width_percent(0)
        self.timch2.pulse_width_percent(0)