"""
@file           MotorDriver.py
@author         Craig Kimball, Miles Young
@date           3/11/2021
@brief          <b> A driver for DC motors </b>\n
@details        This code contains a MotorDriver class which allows for the creation of a motor object. It includes 
                methods for enabling and disabling the motor, as well as setting the duty cycle.\n
                Sourcecode: https://bitbucket.org/MilesYoung/me305_me405_labs/src/master/Lab%207/MotorDriver.py
"""

import pyb
import utime

class MotorDriver:
    '''
    @brief          This class implements a motor driver for the ME305/405 board.
    '''
    
    def __init__(self,motorNum,pinSleep,pinFault,pinIN1,channel1,pinIN2,channel2,timNum):
        '''
        @brief          Creates a motor driver by initializing GPIO pins and turning the motor off for safety.
        @param motorNum A number identifier for the motor object.
        @param pinSleep A pyb.Pin object to use as the enable pin.
        @param pinFault A pyb.Pin object to use with an external interrupt to sense current overloads from the motor.
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
        
        ## Defines local fault pin object for fault pin
        self.pinFault = pinFault
        
        ## Create external interrupt object connected to fault pin
        self.extint = pyb.ExtInt(self.pinFault, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, self.faultInterrupt)
        
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
        @brief      <b> Enable Motor </b>      
        @details    Turns the enable pin high, allowing the motor to move
        '''
        
        # Disable fault external interrupt momentarily
        self.extint.disable()
        
        #print('Enabling Motor ' + str(self.motorNum))
        self.pinSleep.high()
        
        # Enable fault external interrupt again

        utime.sleep_us(100)

        self.extint.enable()
        
    def disable(self):
        '''
        @brief      <b> Disable Motor </b>
        @details    Turns the enable pin low, disabling motor movement
        '''
        
        #print('Disabling Motor ' + str(self.motorNum))
        self.pinSleep.low()
        
        
    def setDuty(self,duty):
        '''
        @brief          <b> Set Motor Duty Cycle </b>
        @param duty     The desired duty cycle, either positive for forward movement or negative for reverse movement
        '''
        
        if (duty >= 100):
            self.timch2.pulse_width_percent(100)
            self.timch1.pulse_width_percent(0)
        elif(duty <= -100):
            self.timch2.pulse_width_percent(0)
            self.timch1.pulse_width_percent(100)
        
        if(duty >= 0):
            self.timch2.pulse_width_percent(duty)
            self.timch1.pulse_width_percent(0)
        elif(duty < 0):
            duty_correct = duty *(-1)
            self.timch2.pulse_width_percent(0)
            self.timch1.pulse_width_percent(duty_correct)
            
    def brake(self):
        '''
        @brief      <b> Brake Motor </b>
        @details    Sets duty cycles to both PWM channels low, causing the motor to brake rapidly
        '''
        
        self.timch1.pulse_width_percent(0)
        self.timch2.pulse_width_percent(0)

    def faultInterrupt(self,fault_pin):
        '''
        @brief      <b>Fault Pin External Interrupt</b>
        @Details    External interrupt method which is triggered when the motor H-bridge fault pin goes low.
        '''
        
        # Immediately disable the motor
        self.disable()
        
        self.setDuty(0)
        
        self.faultFlag = True
        
