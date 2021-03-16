# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 00:21:08 2020

@file               EncoderDriver.py
@date               10/13/2020
@author             Miles Young
@brief              <b> Encoder Driver Class</b>\n
@details            This driver class constructs an encoder object which is capable 
                    of updating the angular position and velocity of the output 
                    shaft of a motor. Other methods include setting the position, 
                    returning the difference between previous and current positions.\n
                    Sourcecode: https://bitbucket.org/MilesYoung/me305_me405_labs/src/master/Lab%207/MotorEncoder.py
"""

import pyb
import math

class EncoderDriver:
    '''
    @brief          <b> Encoder Driver Class </b>
    '''
    
    def __init__(self,pinA,pinB,timer,PPC,CPR,gearRatio):
        '''
       @brief           <b> Encoder class constructor </b>
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
        @brief      <b> Update encoder position </b>
        @details    Updates the encoder position after a set time interval
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
        @brief               <b> Return encoder position</b>
        @return position     Returns the current position of encoder in encoder ticks
        '''
        
        return self.position
        
    
    def getAngle(self):
       '''
       @brief        <b> Return encoder angle </b>
       @return angle Returns the current angular position of the encoder in radians
       '''
    
       angle = self.tick2rad(self.position)
       
       return angle
    
    
    def setPosition(self,newPosition):
        '''
        @brief              <b> Set current relative encoder position </b>
        @details            Sets the encoder position according to the desired user input parameter 'angle'
        @param newPosition  The angle to which the encoder will be set. must be an integer
        '''
        
        self.position = newPosition
        
        
    def getDelta(self):
        '''
        @brief      <b> Calculate delta between encoder updates </b>        
        @details    Calculates the difference between the current and previous position counts
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
    
    
    def tick2rad(self,ticks):
        '''
        @brief          <b> Convert encoder ticks to degrees </b>
        @details        Converts the position of the encoder from ticks to degrees
        @param ticks    The position of the encoder in ticks. This is most easily 
                        obtained from the self.position attribute.
        '''
    
        ## Position of encoder in degrees
        rad = (ticks*(1/self.PPC)*(1/self.CPR)*(2*math.pi))
    
        return rad
    
    
    def getSpeed(self,interval):
       '''
       @brief           <b> Convert encoder delta to degrees per second </b>
       @details         Determines the angular velocity of the motor according to the encoder PPC (pulses per cycle), CPR (cycles per revolution), and gear ratio which were input into the object constructor, as well as the time interval over which the encoder delta was calculated.
       @param interval  The interval of time over which delta occurs, which must be in seconds
       @param speed     Returns the speed of the encoder in deg/s   
       '''
       
       ## calculated speed of the encoder
       rps = self.tick2rad(self.getDelta())/interval
       
       return rps

