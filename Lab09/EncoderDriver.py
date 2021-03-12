# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 00:21:08 2020

@file               EncoderDriver.py
@date               10/13/2020
@author             Miles Young
@brief              A class which interprets encoder output to determine angular position or velocity.\n
@details            This driver class constructs an encoder object which is capable 
                    of updating the angular position and velocity of the output 
                    shaft of a motor. Other methods include setting the position, 
                    returning the difference between previous and current positions.\n
                    Sourcecode: https://bitbucket.org/MilesYoung/me305_me405_labs/src/master/Lab%207/MotorEncoder.py
"""

import pyb

class EncoderDriver:
    '''
    @brief          A class for intepreting encoder output
    '''
    
    def __init__(self,pinA,pinB,timer,PPC,CPR,gearRatio):
        '''
       @brief           Constructs Encoder class
       @details         This method constructs the Encoder object by assigning
                        pin and timer input parameters and defining initial
                        states of pins
       @param pinA      The pin location for + encoder terminal. must be 
                        properly defined as a pin object before being input
                        into an encoder class. Use pinA = pyb.Pin.cpu.
                        [pin letter(s) and number]
       @param pinB      The pin location for GND encoder terminal. must follow 
                        same format for pinA
       @param timer     The timer number which applies to both pins, which can
                        be found using Table 17 of the Nucleo datasheet
       @param PPC       The pulses per rotation of the encoder
       @param CPR       The cycles per rotation of the encoder
       @param gearRatio The gear ratio between the motor and the output shaft 
                        on which the encoder is mounted
       '''
        
        ## Translates the encoder pin A input into Encoder object 
        self.pinA = pinA
        
        ## Translates the encoder pin B input into Encoder object
        self.pinB = pinB
        
        ## Defines the timer which applies to pins A and B
        self.tim = pyb.Timer(timer, prescaler = 0, period = 0xFFFF) 
        
        ## Constructs channel for pin A within timer
        self.tim.channel(1,pin=self.pinA, mode=pyb.Timer.ENC_AB)
        
        ## Constructs channel for pin B within timer
        self.tim.channel(2,pin=self.pinB, mode=pyb.Timer.ENC_AB)
        
        ## Creates a variable to hold the current position count of the encoder
        self.curr_count = 0
        
        ## Creates a variable to hold the previous position count of the encoder
        self.prev_count = 0
        
        ## Creates a local variable to hold the total position of the encoder
        self.position = 0

        ## Creates a local variable to hold value representing difference between current and previous position
        self.delta = 0 
        
        ## Define the pulses per cycle for this encoder object via user input into constructor
        self.PPC = PPC
        
        ## Define the cycles per revolution for this encoder object via user input into constructor
        self.CPR = CPR
        
        ## Define the gear ratio (motor:encoder) reduced to an integer via user input into the constructor
        self.gearRatio = gearRatio
        
        ## Defines total number of counter values before overflow
        self.overflow = 65536
        

    def update(self):
        '''
        @brief          Updates the encoder position after a set time interval
        '''
        
        # Update current encoder count
        self.curr_count = self.tim.counter()
        # Update difference between previous and current position
        self.delta = self.curr_count - self.prev_count
        
        # Determine if overflow or underflow has occured
        if(abs(self.delta) < (self.overflow/2)):
            self.position = (self.position + self.delta)
        elif(abs(self.delta) >= self.overflow/2):
            if(self.delta < 0):
                # In the case of overflow
                self.position = (self.position + (self.delta + self.overflow))
            elif(self.delta > 0):
                # In the case of underflow
                self.position = int(self.position + (self.delta - self.overflow))
        
        # Current count becomes previous count for next iteration
        self.prev_count = self.curr_count
        
    def getPosition(self):
        '''
        @brief          Returns the current position of encoder
        '''
       
        return self.position
        
        
    def setPosition(self,newPosition):
        '''
        @brief              Sets the encoder position according to the desired user input parameter 'angle'
        @param newPosition  The angle to which the encoder will be set. must be an integer
        '''
        
        self.position = newPosition
        
        
    def getDelta(self):
        '''
        @brief          Calculates the difference between the current and previous position counts
        '''        
        # Determine if overflow or underflow has occured
        if(abs(self.delta) < (self.overflow/2)):
            return self.delta
        
        elif(abs(self.delta) >= self.overflow/2):
            if(self.delta < 0):
                # In the case of overflow
                return (self.delta + self.overflow)
            
            elif(self.delta > 0):
                # In the case of underflow
                return (self.delta - self.overflow)
    
    
    def tick2deg(self,ticks):
        '''
        @brief          Converts the position of the encoder from ticks to degrees
        '''
    
        ## Position of encoder in degrees
        theta = int(ticks*(1/self.PPC)*(1/self.CPR)*(360/1))
    
        return theta
    
    
    def tick2rpm(self,interval):
       '''
       @brief Determines the angular velocity of the motor according to the encoder PPC (pulses per cycle), CPR (cycles per revolution), and gear ratio which were input into the object constructor, as well as the time interval over which the encoder delta was calculated.
       @param interval  The interval of time over which delta occurs
       '''
       
       ## calculated speed of the encoder
       rpms = (self.getDelta()/interval)*(60000/1)/(self.PPC*self.CPR)
       
       return rpms

