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
    

    
    def xCL(self,x,xdot,theta_x,thetadot_x):
        '''
        @brief      <b> x-axis Closed-loop Feedback Control </b>
        @details    ...
        @return xduty   ...
        '''
        # Feedback Equation
        
        ## Solve for torque
        Tx = -(self.K1*xdot + self.K2*thetadot_x + self.K3*x + self.K4*theta_x)
        
        xduty = 1*Tx # Placeholder
        
        return xduty  

    def yCL(self,y,ydot,theta_y,thetadot_y):
        '''
        @brief      <b> y-axis Closed-loop Feedback Control </b>
        @details    ... 
        @return yduty   ...
        '''        
        
        # Feedback Equation
        Ty = -(self.K1*ydot + self.K2*thetadot_y + self.K3*y + self.K4*theta_y)
        
        yduty = 1*Ty # Placeholder
        
        return yduty