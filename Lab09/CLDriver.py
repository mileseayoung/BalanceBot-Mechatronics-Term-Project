# -*- coding: utf-8 -*-
"""
@file       TouchDriver.py
@author     Craig Kimball, Miles Young
@date       02/25/2021
@brief      <b> Resistive Touch Panel Driver </b> \n
@details    This 
"""

class CLDriver:
    '''
    @brief      ...<b> BalanceBot Closed-loop Controller Driver Class</b>
    @details    ...
    '''
    
    def __init__(self,K1,K2,K3,K4):
        '''
        @brief      ...
        @details    ...
        @param K1   ...
        @param K2   ...
        @param K3   ...
        @param K4   ...
        '''
        ## Controller gain 1 from constructor
        self.K1 = K1
        
        ## Controller gain 2 from constructor
        self.K2 = K2
        
        ## Controller gain 3 from constructor
        self.K3 = K3
        
        ## Controller gain 4 from constructor
        self.K4 = K4
    

    
    def TtoD(self,Torque):
        '''
        @brief          Converts Torque to Duty cycle
        @details        Takes a torque value supplied by the controller, for correcting balance, and converts
                        it to a duty cycle that can be sent to the motor through PWM signal
        @param Torque   Output Torque from controller required to balance board. Units assumed to be mN-M
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
