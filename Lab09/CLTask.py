# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 09:03:11 2021

@author: Miles
"""

import utime
import sys


class CLTask:
    
    S0_init = 0
    
    S1_calibrate = 1
    
    S2_control = 2
    
    
    def __init__(self,taskNum,CLObject,MotorObject1,MotorObject2,EncoderObject1,EncoderObject2,TouchPanelObject,IMUObject,i2c,address):
        '''
        @brief      ...
        @details    ...
        @param taskNum  ...
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



    def run(self):
        '''
        @brief      ...
        @details    ...
        '''
        
        ## Updates to the current time recorded by the controller clock
        self.currTime = utime.ticks_us()
        
        # Specifying the next time the task will run
        if utime.ticks_diff(self.currTime, self.nextTime) >= 0:
            # If the interval has been reached
        
            if self.state == self.S0_init:
                # Check IMU I2C comm. is valid
                if self.i2c.is_ready(self.i2c,self.address):
                    print(' IMU address ' + str(hex(self.address)) + ' verified')
                    self.state = self.S1_calibrate
                else:
                    print('Unable to verify IMU address ' + str(hex(self.address)) + '\n Program will exit')
                    sys.exit()
            
            elif self.state == self.S1_calibrate:
                # Calibrate IMU
                input('Place the platform in a single stable position for a few seconds to allow the gyroscope to calibrate \n Press enter to begin calibration')
                
                while True:
                    # Delay 100 milliseconds
                    utime.sleep_ms(100)
                    # Check calibration status
                    if self.IMU.calibrated(self.IMU):
                        break
                    else:
                        print('Calibrating: ' + str(self.IMU.cal_status(self.IMU)[1]*(100/3)) + '%')
                 
                # Enable motors
                self.Motor1.enable(self.Motor1)
                self.Motor2.enable(self.Motor2)        
                
                # Change IMU mode to gyro only for faster scans
                GYRONLY_MODE = 0x03
                self.IMU.mode(self.IMU,GYRONLY_MODE)
                
                # Calibrate encoders
                # Calibrate x-axis
                while True:
                    self.xCalAngle = self.IMU.gyro(self.IMU)[0]
                    if self.xCalAngle != 0 and self.xCalAngle < 0:
                        self.Motor1.setDuty(self.Motor1,20)
                    elif self.xCalAngle !=0 and self.xCalAngle > 0:
                        self.Motor1.setDuty(self.Motor1,-20)
                    elif self.xCalAngle == 0:
                        self.Encoder1.setPosition(self.Encoder2,0)
                        break
                    else:
                        pass # Error Handling
                # Calibrate y-axis
                while True:
                    self.yCalAngle = self.IMU.gyro(self.IMU)[1]
                    if self.yCalAngle != 0 and self.yCalAngle < 0:
                        self.Motor2.setDuty(self.Motor2,20)
                    elif self.yCalAngle !=0 and self.yCalAngle > 0:
                        self.Motor2.setDuty(self.Motor2,-20)
                    elif self.yCalAngle == 0:
                        self.Encoder2.setPosition(self.Encoder2,0)
                        break
                    else:
                        pass # Error Handling
                    
                print('Encoder calibration complete')
                self.transitionTo(self.S2_control)
                    
            elif self.state == self.S2_control:
                # Update encoder counts
                self.Encoder1.update(self.Encoder1)
                self.Encoder2.update(self.Encoder2)
                ## Measure angle about x-axis
                theta_x = self.IMU.euler(self.IMU)[1]
                ## Measure first time derivative of angle about x-axis
                thetadot_x = self.IMU.gyro(self.IMU)[0]
                
                
                ## Measure angle about y-axis
                theta_y = self.IMU.euler(self.IMU)[2]
                ## Measure first time derivative of angle about y-axis
                thetadot_y = self.IMU.gyro(self.IMU)[1]
            
                ## Measure position
                if self.TouchObject.position(self.TouchObject)[0]:
                    x = self.TouchObject.position(self.TouchObject)[1]
                    y = self.TouchObject.position(self.TouchObject)[2]
                else:
                    input('Loss of contact detected - commencing recalibration')
                    self.transitionTo(self.S1_calibration)
                
                xCL(x,theta_x,thetadot_x)
                yCL(y,theta_y,thetadot_y)
                
    
    
    def transitionTo(self,newState):
        '''
        @brief          Transitions between states
        @param newState The desired state for next iteration
        '''
    
        self.state = newState
        