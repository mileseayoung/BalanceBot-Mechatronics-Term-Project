# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 08:57:10 2021

@author: Miles
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
    
        
    
    
    
    
    
    def xCL(x,theta_x,thetadot_x):
        '''
        @brief      <b> x-axis Closed-loop Feedback Control </b>
        @details    ...
        '''
        # Feedback Equation
        
        
        

    def yCL(y,theta_y,thetadot_y):
        '''
        @brief      <b> y-axis Closed-loop Feedback Control </b>
        @details    ... 
        '''        
        
        # Feedback Equation