# -*- coding: utf-8 -*-
"""
@file       CLTask.py
@author     Craig Kimball, Miles Young
<<<<<<< HEAD
@date       03/10/2021
@brief      <b> Closed-loop Feedback Controller Task </b> \n
@details    This script contains a task class used to implement closed-loop feedback 
            control for the BalanceBot. It handles the behavior of objects from 
            each driver class in one cohesive task. It runs on an interval of 10,000 
            us, meaning it updates 100 times per second. It has two states: the first 
            is an initialization state, in which encoder angle readings are set to 
            zero and the initial ball position is recorded, and the second is an 
            update/control state, in which measurements are updated, secondary values 
            are calculated from updated measurements, and the control loop is implemented.
=======
@date       02/25/2021
@brief      <b> Resistive Touch Panel Driver </b> \n
@details    This State space program controlls the operation of the Balance board controller.
The Task takes in inputs for the Controller, Motor and Encoder objects and calculates necessary duty cycle to balance the platform.
Source Code: https://bitbucket.org/MilesYoung/lab-4-term-project/src/master/Lab09/CLTask.py
>>>>>>> b8ff90c5248ae510b6ae31aa658582f3e0630553
"""

import utime
import sys
from uarray import array

class CLTask:
    '''
    @brief  <b> Closed-loop Feedback Control Task </b>
    '''
    
    ## Init state for zeroing angles and recording initial ball position
    S0_init = 0
    
    ## Control state in which measurements and calculations are updated and control loop is implemented
    S1_update = 1
    
    
    def __init__(self,CLObject1,CLObject2,MotorObject1,MotorObject2,EncoderObject1,EncoderObject2,TouchPanelObject,dbg=False):
        '''
<<<<<<< HEAD
        @brief      <b> Control Task Constructor </b>
        @details    The constructor requires two closed-loop driver objects, two 
                    motor driver objects, two encoder objects, and a touch panel object. 
                    It converts these to class-specific objects, and defines some 
                    essential variables. During initialization, an input message 
                    prompts the user to set the platform at equilibrium.
        
        @param CLObject1            First object of the CLDriver class
        @param CLObject2            Second object of the CLDriver class
        @param MotorObject1         First object of the MotorDriver class
        @param MotorObject2         Second object of the MotorDriver class
        @param EncoderObject1       First object of the EncoderDriver class
        @param EncoderObject2       Second object of the EncoderDriver class
        @param TouchPanelObject     Object of TouchDriver class
        @param dbg                  Optional constructor parameter which enables 
                                    debugging print traces. Defaults to False.
=======
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
>>>>>>> b8ff90c5248ae510b6ae31aa658582f3e0630553
        '''
        
        
        ## Class-specific CLDriver object 1. Corresponds to control loop for Motor 1.
        self.CL1 = CLObject1
        
        ## Class-specific CLDriver object 2. Corresponds to control loop for Motor 2.
        self.CL2 = CLObject2
        
        ## Class-specific MotorDriver object 1. Motor 1 rotates about the universal y-axis according to the coordinate frame used in the system dynamic analysis.
        self.Motor1 = MotorObject1
        
        ## Class-specific MotorDriver object 2. Motor 2 rotates about the universal x-axis according to the coordinate frame used in the system dynamic analysis.
        self.Motor2 = MotorObject2
        
        ## Class-specific EncoderDriver object 1. Encoder 1 should be attached to Motor 1.
        self.Encoder1 = EncoderObject1
        
        ## Class-specific EncoderDriver object 2. Encoder 1 should be attached to Motor 2.
        self.Encoder2 = EncoderObject2
        
        ## Class-specific Touch Panel object.
        self.TouchObject = TouchPanelObject
        
        ## Array that holds sampled time data
        self.timeArray = array('i')
        
        ## Array that holds sampled duty cycle data to motor 2
        self.dutyArrayX = array('i')
        
        ## Array that holds sampled duty cycle data to motor 1
        self.dutyArrayY = array('i')
        
        ## Length of motor actuation arm. Used in angleRatio conversion attribute.
        self.rm = 0.06 # units m
        
        ## Length of platform. Used in angleRatio coversion attribute.
        self.lp = .21 # units m
        
        ## Class-specific attribute used to convert motor/encoder angles to corresponding platform angles.
        self.angleRatio = -(self.rm/self.lp)
        
        ## Debug flag, set in constructor.
        self.dbg = dbg
        
        ## The timestamp for the initial iteration in microseconds.
        self.startTime = utime.ticks_us()
        
        ## Defines the current time for the iteration and is overwritten at the beginning of each iteration.
        self.currTime = utime.ticks_us()
        
        ## Defines the interval after which another iteration will run in microseconds.
        self.interval = 10000 # Spitballing here
        
        ## Time for which next iteration will run and is overwritten at the end of each iteration
        self.nextTime = utime.ticks_add(self.startTime,self.interval)
        
        ## Defines the starting state for the run() method.
        self.state = self.S0_init
        
        ## Flag variable to signal if the first run() of the fsm is occurring. This is used to set an accurate initial nextTime.
        self.firstFlag = True
        
        ## Creates a variable to hold the index of the current iteration of the task.
        self.runs = 0
        
        # Before FSM runs, encoder zero positions must be determined
        input('Hold the board level with the ball resting in the center of the board, then press Enter')
        
        # Debug initialization confirmation
        if dbg == True:
            print('Initialization successful')
        
    def run(self):
        '''
        @brief      <b> Controller task finite-state machine </b>
        @details    This method fully implements all aspects of the control loop. 
                    After initialization, in which encoder values are zeroed and 
                    the initial ball position is recorded, driver objects are 
                    used to directly measure encoder angles and ball positions. 
                    Then, platform angles and speeds and ball speeds are calculated 
                    for the defined time interval between runs. Finally, the control 
                    loop is implemented and new duty cycles are sent to the motors.
        '''
        
        # Updates to the current time recorded by the controller clock at the beginning of the task run
        self.currTime = utime.ticks_us()
        
        # Set initial next time based on current time of first run
        # This allows for accurate time data collection
        if self.firstFlag == True:
            # Define start time
            self.startTime = utime.ticks_us()
            # Define next time based on start time
            self.nextTime = utime.ticks_add(self.startTime,self.interval) 
            # Set flag to true to prevent this conditional statement from running again 
            self.firstFlag = False
        
        # Before main loop, check for fault flag from either motor object
        # If a fault is detected, the program exits immediately using the sys.exit() method
        # Duty cycles are set to zero to avoid motor damage when they are reenabled
        if self.Motor1.faultFlag == True or self.Motor2.faultFlag == True:
            print('Fault detected - program will exit' + '\n' + 'Attend to the fault before re-running the program')
            self.Motor1.setDuty(0)
            self.Motor2.setDuty(0)
            sys.exit()
        
        # Specifying the next time the task will run
        # If the difference between the current time and the next time, which is defined as the previous next time plus the interval is reached, is greater than 0.
        if utime.ticks_diff(self.currTime, self.nextTime) >= 0:  
            
            # Print trace if dbg is enabled
            if self.dbg == True:
                print('')
                print('Run: {:}, State: {:}, time: {:} us'.format(self.runs,self.state,utime.ticks_diff(self.currTime,self.nextTime)))
            
            # Initial state in which encoder position is zeroed at equilibrium and initial ball position is recorded
            if self.state == self.S0_init:
                # Update encoder positions to zero them on level position
                self.Encoder1.setPosition(0)
                self.Encoder2.setPosition(0)
                # Read touch panel to find ball position
                ## The initial position of the ball at equilibrium
                self.ball_rest = self.TouchObject.read()
                # Print trace if dbg is enabled
                if self.dbg == True:
                    print('phi_x: {:.2f}, phi_y: {:.2f}'.format(self.Encoder2.getAngle(),self.Encoder1.getAngle()))
                    print(str(self.ball_rest))
                # Define current ball position as initial measurement
                ## The current position of the ball used to measure x- and y-position and detect if the ball is on the platform.
                self.current_ball_pos = self.ball_rest
                # Transition to update state
                self.transitionTo(self.S1_update)
                
            # State for reading positions, calculating speeds, and implementing control loop
            # In this state, measurements for ball and platform position or orientation are updated and secondary values are calculated
            elif self.state == self.S1_update:
                
                #finding theta_x from 0 on X axis
                # Update the encoder reading
                self.Encoder1.update()
                # Measure motor 1 angle using encoder method to convert ticks to radians
                # To keep axis directions consistent with our dynamic model, angle signs are inverted
                ## The current angular position of motor 1 in radians
                self.phi_y = -self.Encoder1.getAngle()
                # Calculate motor 1 speed using encoder method and interval scaled into seconds
                ## The current angular speed of motor 1 in rad/s
                self.phi_y_dot = -self.Encoder1.getSpeed(self.interval/1e6)
                # Covert motor 1 angle and speed about y-axis to platform angle about x-axis using angleRatio attribute
                ## The current angular position of the platform about the x-axis in rad
                self.theta_x = self.phi_y*self.angleRatio
                ## The currrent angular speed of the platform about the x-axis in rad/s
                self.theta_x_dot = self.phi_y_dot*self.angleRatio
                ## A list containing the angle and speed of platform about the x-axis in rad and rad/s
                self.plat_paramX = [self.theta_x,self.theta_x_dot]
                
                #finding theta_y from 0 on Y axis
                # Repeat the process above for the encoder 2/motor 2 combo
                self.Encoder2.update()
                ## The current angular position of motor 2 in radians
                self.phi_x = -self.Encoder2.getAngle()
                ## The current angular speed of motor 1 in rad/s
                self.phi_x_dot = -self.Encoder2.getSpeed(self.interval/1e6)
                ## The current angular position of the platform about the y-axis in rad
                self.theta_y = self.phi_x*self.angleRatio
                ## The currrent angular speed of the platform about the x-axis in rad/s
                self.theta_y_dot = self.phi_x_dot*self.angleRatio
                ## A list containing the angle and speed of platform about the x-axis in rad and rad/s
                self.plat_paramY = [self.theta_y,self.theta_y_dot]
                # Print trace if dbg is enabled
                if self.dbg == True:
                    print('phi_y: {:.2f}, phi_y_dot: {:.2f}'.format(self.plat_paramX[0],self.plat_paramX[1]))
                    print('phi_x: {:.2f}, phi_x_dot: {:.2f}'.format(self.plat_paramY[0],self.plat_paramY[1]))

                # reading Ball position
                # Update the previous ball position
                ## The ball position from the previous run, used to calculate the speed of the ball
                self.last_ball_pos = self.current_ball_pos
                # update the current ball position by reading the touch panel
                self.current_ball_pos = self.TouchObject.read()
                #If the ball is still detected as being on the platform
                if self.current_ball_pos[0] == True:
                    # To keep axis directions consistent with the dynamic model, position and speed signs are inverted
                    ## The position of the ball on the touch panel in the x-direction in m
                    self.X_ball = -self.current_ball_pos[1]
                    ## The position of the ball on the touch panel in the y-direction in m
                    self.Y_ball = -self.current_ball_pos[2]
                    # Calculate the linear speed of the ball in the x- and y-directions in m/s, scaling the interval to seconds
                    ## The speed of the ball in the x-direction in m/s
                    self.X_ball_dot = -(self.current_ball_pos[1] - self.last_ball_pos[1]) / (self.interval/1e6)
                    ## The speed of the ball in the y-direction in m/s
                    self.Y_ball_dot = -(self.current_ball_pos[2] - self.last_ball_pos[2]) / (self.interval/1e6)
                    ## A list holding the position and speed of the ball in the x-direction in m and m/s
                    self.ball_paramX = [self.X_ball,self.X_ball_dot]
                    ## A list holding the position and speed of the ball in the y-direction in m and m/s
                    self.ball_paramY = [self.Y_ball,self.Y_ball_dot]
                    # Print trace if dbg is enabled
                    if self.dbg == True:
                        print('x: {:.2f}, x_dot: {:.2f}'.format(self.ball_paramX[0],self.ball_paramX[1]))
                        print('y: {:.2f}, y_dot: {:.2f}'.format(self.ball_paramY[0],self.ball_paramY[1]))
                        
                    # Implementation of the control loop  
                    # Calculate torque using platform and ball parameters
                    ## Required torque for motor 1
                    self.InputTx = self.CL1.Controller(self.plat_paramY,self.ball_paramX)
                    ## Required torque for motor 2
                    self.InputTy = self.CL2.Controller(self.plat_paramX,self.ball_paramY)
                
                # If the ball is not detected, meaning positional measurements are meaningless, then a simpler control loop using only the platform angles is implemented
                else:
                    print('Ball not detected')
                    # Calculate torque using only platform parameters
                    self.InputTy = self.CL2.zero(self.plat_paramX)
                    self.InputTx = self.CL1.zero(self.plat_paramX)
                
                # Convert torque to a duty cycle that is then applied to the motor
                self.Motorx_feed = self.CL2.TtoD(self.InputTy)
                self.Motory_feed = self.CL1.TtoD(self.InputTx)          
                # Print trace if dbg is enabled
                if self.dbg == True:
                    print('Motor duty cycles: ' + str([self.Motorx_feed,self.Motory_feed]))
                
<<<<<<< HEAD
                if self.runs/100 == int:
                    # Store time data in an array in seconds
                    self.timeArray.append(int(utime.ticks_diff(self.currTime,self.startTime)/1e6))
                    # Store motor 1 duty cycle data in an array in percent
                    self.dutyArray1.append(int(self.Motory_feed))
                    # Store motor 2 duty cycle data in an array in percent
                    self.dutyArray2.append(int(self.Motorx_feed))
=======
                #if self.dbg == True:
                print('Motor duty cycles: ' + str([self.Motorx_feed,self.Motory_feed]))
                
            #    self.timeArray.append(int(utime.ticks_diff(self.currTime,self.startTime)/1000))
                self.dutyArray1.append(int(self.Motory_feed))
                self.dutyArray2.append(int(self.Motorx_feed))
>>>>>>> b8ff90c5248ae510b6ae31aa658582f3e0630553
                
                # Set the motor duty cycles according to updated controller values
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
        
        