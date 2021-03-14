# -*- coding: utf-8 -*-
"""
@file       TouchDriver.py
@author     Craig Kimball, Miles Young
@date       02/25/2021
@brief      <b> Resistive Touch Panel Driver </b> \n
@details    This
"""

import utime
import sys

class CLTask:
    
    S0_init = 0
    
    S1_update = 1
    
    S2_control = 2
    
    
    def __init__(self,CLObject,MotorObject1,MotorObject2,EncoderObject1,EncoderObject2,TouchPanelObject,dbg=False):
        '''
        @brief      ...
        @details    ...
        @param CLObject ...
        @param MotorObject1     ...
        @param MotorObject2     ...
        @param EncoderObject1     ...
        @param EncoderObject2     ...
        @param TouchPanelObject   ...
        @param IMUObject    ...
        @param i2c  ...
        @param address  ...
        '''
        
        self.CL = CLObject
        
        self.Motor1 = MotorObject1
        
        self.Motor2 = MotorObject2
        
        self.Encoder1 = EncoderObject1
        
        self.Encoder2 = EncoderObject2
        
        self.TouchObject = TouchPanelObject
        
        #self.IMU = IMUObject
        
        ## Debug flag, set in constructor
        self.dbg = dbg
        
        ## The timestamp for the initial iteration in milliseconds
        self.startTime = utime.ticks_us()
        
        ## Defines the current time for the iteration and is overwritten at the beginning of each iteration
        self.currTime = utime.ticks_us()
        
        ## Defines the interval after which another iteration will run in ms
        self.interval = 20000 # Spitballing here
        
        ## Defines the starting state for the run() method
        self.state = self.S0_init
        
        ## Flag variable to signal if the first run() of the fsm is occurring. This is used to set an accurate initial nextTime
        self.firstFlag = True
        
        ## Creates a variable to hold the index of the current iteration of the task
        self.runs = 0
        
        # Before FSM runs, encoder zero positions must be determined
        input('Hold the board level with the ball resting in the center of the board, then press Enter')
        
        # Debug initialization confirmation
        if dbg == True:
            print('Initialization successful')
        
        ## Time for which next iteration will run and is overwritten at the end of each iteration
        self.nextTime = utime.ticks_add(self.startTime,self.interval)
        
        
    def run(self):
        '''
        @brief      ...
        @details    ...
        '''
        
        ## Updates to the current time recorded by the controller clock
        self.currTime = utime.ticks_us()
        
        # Set initial next time based on current time of first run
        if self.firstFlag == True:
            ## Time for which next iteration will run and is overwritten at the end of each iteration
            self.nextTime = utime.ticks_add(self.currTime,self.interval) 
            self.firstFlag = False
        else:
            pass
        
        # Specifying the next time the task will run
        if utime.ticks_diff(self.currTime, self.nextTime) >= 0:
            # If the interval has been reached
            
            if self.dbg == True:
                print('Run: {:}, State: {:}, time: {:} us'.format(self.runs,self.state,utime.ticks_diff(self.currTime,self.startTime)))
            
            if self.state == self.S0_init:
                ## Init State
                #input('Hold the board level with the ball resting in the cente of the board. Then Press Enter')
                # Update encoder positions to zero them on level position
                self.zeroX = 0
                self.Encoder1.setPosition(self.zeroX)
                self.zeroY = 0
                self.Encoder2.setPosition(self.zeroY)
                # Read touch panel to find ball position
                self.ball_rest = self.TouchObject.read()
                print(str(self.ball_rest))
                self.current_ball_pos = self.ball_rest
                self.transitionTo(self.S1_update)
                
            #State for reading position of deviation of ball and platform from centerpoint
            elif self.state == self.S1_update:
                '''
                In this state, measurements for ball and platform position or orientation are updated and secondary values are calculated
                '''
                #finding theta from 0 on X axis
                self.Encoder1.update()
                self.xtick = self.Encoder1.getPosition()
                self.X = self.Encoder1.tick2deg(self.xtick)
                self.X_dot = self.Encoder1.getDelta() / (self.interval*1e6)
                self.plat_paramX = [self.X,self.X_dot]
                
                #finding theta from 0 on Y axis
                self.Encoder2.update()
                self.ytick = self.Encoder2.getPosition()
                self.Y = self.Encoder2.tick2deg(self.ytick)
                self.Y_dot = self.Encoder2.getDelta() / self.interval*(1e6)
                self.plat_paramY = [self.Y,self.Y_dot]
                #print([Y,Y_dot])
                # reading Ball position
                
                self.last_ball_pos = self.current_ball_pos
                self.current_ball_pos = self.TouchObject.read()
                #If the bal is still detected as being on the platform
                if self.current_ball_pos[0] == True:
                    self.X_ball = self.current_ball_pos[1]
                    self.Y_ball = self.current_ball_pos[2]
                    self.X_ball_dot = (self.current_ball_pos[1] - self.last_ball_pos[1]) / (self.interval*(1e6))
                    self.Y_ball_dot = (self.current_ball_pos[2] - self.last_ball_pos[2]) / (self.interval*(1e6))
                   
                    self.ball_paramX = [self.X_ball,self.X_ball_dot]
                    self.ball_paramY = [self.Y_ball,self.Y_ball_dot]
                    self.transitionTo(self.S2_control)
                else:
                    print('Ball no longer detected - program will exit')
                    sys.exit()
                
            #Controller state. Where motor values are found and applied
            elif self.state == self.S2_control:
                '''
                In this state values are to be fed into a controller. The controller
                will then calculate a Torque output for a motor and that will be converted to a duty
                cycle that is then applied to the motor.
                '''
                self.InputTx = self.CL.Controller(self.plat_paramX,self.ball_paramX)
                self.InputTy = self.CL.Controller(self.plat_paramY,self.ball_paramY)
                
                self.Motorx_feed = self.CL.TtoD(self.InputTx)
                self.Motory_feed = self.CL.TtoD(self.InputTy)
                print([self.Motorx_feed,self.Motory_feed])
                
                self.Motor1.setDuty(self.Motory_feed)
                self.Motor2.setDuty(self.Motorx_feed)
                self.transitionTo(self.S1_update)
                
            # Define time after which the data collection task will commence
            self.nextTime = utime.ticks_add(self.nextTime,self.interval)
                
            # Increase run count by 1
            self.runs += 1 

    def transitionTo(self,newState):
        '''
        @brief          Transitions between states
        @param newState The desired state for next iteration
        '''
    
        self.state = newState
        
        
    def linVelocity(self,delta):
        '''
        @brief      ...
        @details    ...
        '''
        
        velocity = delta/(self.interval*1e6)
        
        return velocity
        
        