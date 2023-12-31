"""
@file           MotorDriver.py
@author         Craig Kimball, Miles Young
@date           3/10/2021
@brief          <b> DC Motor Driver Class </b>\n
@details        This is an updated version of a DC motor driver class created for 
                ME 305. This driver constructs a motor object which is capable 
                of enabling, disabling, or setting the duty cycle of a motor. 
                Updates include the implementation of an external interrupt method 
                triggered by a fault pin, which is now included in the constructor.
                This external interrupt prevents damage to the motor by disabling 
                and setting the duty cycle to zero if sufficiently high current 
                is detected.\n
                Source -- https://bitbucket.org/MilesYoung/lab-4-term-project/src/master/Lab09/MotorDriver.py
"""

import pyb
import utime

class MotorDriver:
    '''
    @brief          <b> Motor driver class </b>
    '''
    
    def __init__(self,motorNum,pinSleep,pinFault,pinIN1,channel1,pinIN2,channel2,timNum):
        '''
        @brief          <b>Motor driver constructor </b>  
        @details        This constructor creates a motor driver by initializing GPIO pins and turning the motor off for safety.
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
        
        ## Flag used to signal if fault external interrupt has been triggered. It is set to false upon initialization.
        self.faultFlag = False
        
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
        @details        Sets the motor duty cycle according to user input. For forward (CCW) motion when the duty is positive, the duty is assigned 
                        to channel 1. For reverse (CW) motion when duty is negatvive, the duty is assigned to channel 2. Duty is clamped between 
                        100 and -100 percent.
        @param duty     The desired duty cycle, either positive for forward movement or negative for reverse movement
        '''
        
        if (duty >= 100):
            self.timch1.pulse_width_percent(100)
            self.timch2.pulse_width_percent(0)
        elif(duty <= -100):
            self.timch1.pulse_width_percent(0)
            self.timch2.pulse_width_percent(100)
        
        if(duty >= 0):
            self.timch1.pulse_width_percent(duty)
            self.timch2.pulse_width_percent(0)
        elif(duty < 0):
            duty_correct = duty *(-1)
            self.timch1.pulse_width_percent(0)
            self.timch2.pulse_width_percent(duty_correct)
            
    def brake(self):
        '''
        @brief      <b> Brake Motor </b>
        @details    Sets duty cycles to both PWM channels low, causing the motor to brake rapidly
        '''
        
        self.timch1.pulse_width_percent(0)
        self.timch2.pulse_width_percent(0)

    def faultInterrupt(self,faultPin):
        '''
        @brief          <b> Fault Pin External Interrupt</b>
        @details        External interrupt method which is triggered when the motor H-bridge fault pin goes low.
        @param faultPin The pin on the hardware which is used to trigger the external interrupt method.
        '''
        
        # Immediately disable the motor
        self.disable()
        
        # Set motor duty cycle to zero
        self.setDuty(0)
        
        # Reset fault pin to high state
        self.pinFault.high()
        
        # Set fault flag to true
        self.faultFlag = True
        
        # Print fault statement
        print('Fault')
