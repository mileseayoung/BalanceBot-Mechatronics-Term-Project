# -*- coding: utf-8 -*-
"""
@file       TouchDriver.py
@author     Craig Kimball, Miles Young
@date       02/25/2021
@brief      <b> Resistive Touch Panel Driver </b> \n
@details    This State space program controlls the operation of the Balance board controller.
The Task takes in inputs for the Controller, Motor and Encoder objects and calculates necessary duty cycle to balance the platform.
Source Code: https://bitbucket.org/MilesYoung/lab-4-term-project/src/master/Lab09/CLTask.py
"""

import utime
import sys
from uarray import array

class CLTask:
    
    S0_init = 0
    
    S1_update = 1
    
    S2_control = 2
    
    
    def __init__(self,CLObject1,CLObject2,MotorObject1,MotorObject2,EncoderObject1,EncoderObject2,TouchPanelObject,dbg=False):
        '''
        @brief      <b> Initilization of variables for State space</b>
        @details    Takes in all input parameters necessary to calculate corrected duty cycles for motors on balance board
        @param CLObject ...
        @param MotorObject1     Motor Object for controlling X axis
        @param MotorObject2     Motor Obkect for controlling Y axis
        @param EncoderObject1   Encoder object for tracking X axis motor rotation
        @param EncoderObject2   Encoder object for tracking Y axis motor rotation
        @param TouchPanelObject Touch panel object that uses TouchPanel Driver to read position on board in m
        @param IMUObject    Object for use of IMU sensor (NOT USED)
        @param i2c  i2c address controller (NOT USED)
        @param address  address of IMU sensor (NOT USED)
        '''
        
        self.CL1 = CLObject1
        
        self.CL2 = CLObject2
        
        self.Motor1 = MotorObject1
        
        self.Motor2 = MotorObject2
        
        self.Encoder1 = EncoderObject1
        
        self.Encoder2 = EncoderObject2
        
        self.TouchObject = TouchPanelObject
        
        self.timeArray = array('i')
        
        self.dutyArray1 = array('i')
        
        self.dutyArray2 = array('i')
        
        self.rm = 0.06 # units m
        
        self.lp = .21 # units m
        
        self.angleRatio = -(self.rm/self.lp)
        
        ## Debug flag, set in constructor
        self.dbg = dbg
        
        ## The timestamp for the initial iteration in milliseconds
        self.startTime = utime.ticks_us()
        
        ## Defines the current time for the iteration and is overwritten at the beginning of each iteration
        self.currTime = utime.ticks_us()
        
        ## Defines the interval after which another iteration will run in ms
        self.interval = 10000 # Spitballing here
        
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
        @brief      <b> Controller task finite-state machine </b>
        @details    ...
        '''
        
        ## Updates to the current time recorded by the controller clock
        self.currTime = utime.ticks_us()
        
        # Set initial next time based on current time of first run
        if self.firstFlag == True:
            ## Time for which next iteration will run and is overwritten at the end of each iteration
            ## The timestamp for the initial iteration in milliseconds
            self.startTime = utime.ticks_us()
            self.nextTime = utime.ticks_add(self.currTime,self.interval) 
            self.firstFlag = False
        else:
            pass
        
        if self.Motor1.faultFlag == True or self.Motor2.faultFlag == True:
            print('Fault detected - program will exit' + '\n' + 'Attend to the fault before re-running the program')
            self.Motor1.setDuty(0)
            self.Motor2.setDuty(0)
            sys.exit()
        else:
            pass
        
        # Specifying the next time the task will run
        if utime.ticks_diff(self.currTime, self.nextTime) >= 0:
            # If the interval has been reached
            
            #if self.dbg == True:
            print('')
            print('Run: {:}, State: {:}, time: {:} us'.format(self.runs,self.state,utime.ticks_diff(self.currTime,self.nextTime)))
            
            if self.state == self.S0_init:
                ## Init State
                #input('Hold the board level with the ball resting in the cente of the board. Then Press Enter')
                # Update encoder positions to zero them on level position
                self.Encoder1.setPosition(0)
                self.Encoder2.setPosition(0)
                # Read touch panel to find ball position
                self.ball_rest = self.TouchObject.read()
                if self.dbg == True:
                    print('phi_x: {:.2f}, phi_y: {:.2f}'.format(self.Encoder2.getAngle(),self.Encoder1.getAngle()))
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
                self.phi_y = -self.Encoder1.getAngle()
                self.phi_y_dot = -self.Encoder1.getSpeed(self.interval/1e6)
                self.theta_x = self.phi_y*self.angleRatio
                self.theta_x_dot = self.phi_y_dot*self.angleRatio
                self.plat_paramX = [self.theta_x,self.theta_x_dot]
                #finding theta from 0 on Y axis
                self.Encoder2.update()
                self.phi_x = -self.Encoder2.getAngle()
                self.phi_x_dot = -self.Encoder2.getSpeed(self.interval/1e6)
                self.theta_y = self.phi_x*self.angleRatio
                self.theta_y_dot = self.phi_x_dot*self.angleRatio
                self.plat_paramY = [self.theta_y,self.theta_y_dot]
                if self.dbg == True:
                    print('phi_y: {:.2f}, phi_y_dot: {:.2f}'.format(self.plat_paramX[0],self.plat_paramX[1]))
                    print('phi_x: {:.2f}, phi_x_dot: {:.2f}'.format(self.plat_paramY[0],self.plat_paramY[1]))
                #print([Y,Y_dot])
                # reading Ball position
                
                self.last_ball_pos = self.current_ball_pos
                self.current_ball_pos = self.TouchObject.read()
                #If the bal is still detected as being on the platform
                if self.current_ball_pos[0] == True:
                    self.X_ball = -self.current_ball_pos[1]
                    self.Y_ball = -self.current_ball_pos[2]
                    self.X_ball_dot = -(self.current_ball_pos[1] - self.last_ball_pos[1]) / (self.interval/1e6)
                    self.Y_ball_dot = -(self.current_ball_pos[2] - self.last_ball_pos[2]) / (self.interval/1e6)
                    
                    self.ball_paramX = [self.X_ball,self.X_ball_dot]
                    self.ball_paramY = [self.Y_ball,self.Y_ball_dot]
                    
                    if self.dbg == True:
                        print('x: {:.2f}, x_dot: {:.2f}'.format(self.ball_paramX[0],self.ball_paramX[1]))
                        print('y: {:.2f}, y_dot: {:.2f}'.format(self.ball_paramY[0],self.ball_paramY[1]))
                        
                    '''
                    In this state values are to be fed into a controller. The controller
                    will then calculate a Torque output for a motor and that will be converted to a duty
                    cycle that is then applied to the motor.
                    '''
                    
                    self.InputTx = self.CL1.Controller(self.plat_paramY,self.ball_paramX)
                    self.InputTy = self.CL2.Controller(self.plat_paramX,self.ball_paramY)
                    
                else:
                    print('Ball not detected')
                    self.InputTy = self.CL2.zero(self.plat_paramX)
                    self.InputTx = self.CL1.zero(self.plat_paramX)
                    
                self.Motorx_feed = self.CL2.TtoD(self.InputTy)
                self.Motory_feed = self.CL1.TtoD(self.InputTx)          
                
                #if self.dbg == True:
                print('Motor duty cycles: ' + str([self.Motorx_feed,self.Motory_feed]))
                
            #    self.timeArray.append(int(utime.ticks_diff(self.currTime,self.startTime)/1000))
                self.dutyArray1.append(int(self.Motory_feed))
                self.dutyArray2.append(int(self.Motorx_feed))
                
                self.Motor2.setDuty(self.Motorx_feed)
                self.Motor1.setDuty(self.Motory_feed)
                
            # Define time after which the data collection task will commence
            self.nextTime = utime.ticks_add(self.nextTime,self.interval)
                
            # Increase run count by 1
            self.runs += 1 

    def transitionTo(self,newState):
        '''
        @brief          <b> Transition between FSM states </b>
        @param newState The desired state for next iteration
        '''
    
        self.state = newState
        
        