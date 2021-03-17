# -*- coding: utf-8 -*-
"""
@file       CLDriver.py
@author     Craig Kimball, Miles Young
@date       03/10/2021
@brief      <b> Closed-loop Feedback Controller Driver </b> \n
@details    This closed-loop feedback controller driver class uses the state-space 
            model with four gains corresponding to the four variables of the simplified 
            dynamic system. It also requires mechanical and electrical characteristics 
            of the motor used to actuate the system. It has two methods: one which 
            uses a feedback equation to determine the torque required from a motor 
            depending on measured parameters, and one which converts torque into duty 
            cycle that can be directly interpreted by a motor driver.
"""

class CLDriver:
    '''
    @brief      <b> BalanceBot Closed-loop Controller Driver Class </b>
    '''
    
    def __init__(self,K1,K2,K3,K4,resistance,Kt,Vdc):
        '''
        @brief      <b> BalanceBot controller driver constructor </b>
        @details    This constructor requires input of four state-space controller 
                    gains, as well as the resistance, torque constant, and DC voltage 
                    of the motor used.
        @param K1   First state-space controller gain
        @param K2   Second state-space controller gain
        @param K3   Third state-space controller gain
        @param K4   Fourth state-space controller gain
        @param resistance The internal resistance of the motor that is to be controlled
        @param Kt   Torque constant of the motor
        @param Vdc  DC voltage used to drive the motor
        '''
        ## Controller gain 1 from constructor
        self.K1 = K1
        
        ## Controller gain 2 from constructor
        self.K2 = K2
        
        ## Controller gain 3 from constructor
        self.K3 = K3
        
        ## Controller gain 4 from constructor
        self.K4 = K4
        
        ## Measured internal motor resistance
        self.resistance = resistance
        
        ## Measured motor torque constant mNm/A
        self.Kt = Kt
        
        ## DC voltage supplied to motor, V
        self.Vdc = Vdc

    
    def TtoD(self,Torque):
        '''
        @brief          <b> Converts Torque to Duty cycle </b>
        @details        Takes a torque value supplied by the controller, for correcting balance, and converts
                        it to a duty cycle that can be sent to the motor through PWM signal
        @param Torque   Output Torque from controller required to balance board. Units assumed to be N-m
        @returns duty   The duty cycle calculated from the torque input as an integer percent
        '''
        
        Duty_decimal = (self.resistance / (self.Kt * self.Vdc)) * Torque

        duty = int(Duty_decimal * 100)
        return duty
        
    
    def Controller(self,plat_param,ball_param):
        '''
        @brief              <b> Closed Loop Controller for getting motor torques </b>
        @details            Requires user-specified gains and platform and ball parameter matrices. Uses
                            the form T = -k*x to calculate a motor torque value for the necessary axis.
        @param plat_param   Platform parameters for the controller must be in form [angle, angular speed]
        @param ball_param   Ball parameters for the controller must be in the form [position, speed]
        @return T           Returns the updated torque output from the control loop in units of N-m
        '''
        T = plat_param[0]*(-self.K4) + plat_param[1]*(-self.K2) + ball_param[0]*(-self.K3) + ball_param[1]*(-self.K1)
        
        return T

    def zero(self,plat_param):
        '''
        @brief              <b> Closed Loop Controller for getting motor torques </b>
        @details            Requires user-specified gains and platform parameter matrix. Uses
                            the form T = -k*x to calculate a motor torque value for the necessary axis.
        @param plat_param   Platform parameters for the controller must be in form [angle, angular speed]
        @return T           Returns the updated torque output from the control loop in units of N-m
        '''
        T = plat_param[0]*(-self.K4) + plat_param[1]*(-self.K2)
        
        return T