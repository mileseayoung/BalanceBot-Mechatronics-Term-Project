# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:09:13 2021

@file       mcp9808_young.py
@author     Miles Young
@date       02/4/2021
@brief      <b> ... </b> \n
@details    ...
"""


class MCP9808:
    '''
    @brief      <b> MCP9808 temperature sensor class </b> \n
    @details    ...
    '''
    
    def __init__(self,i2cObject,address):
        '''
        @brief              <b> MCP9808 semperature sensor class constructor </b> \n
        @details            ...
        @param i2cObject    The I2C communication protocol object which is to be used for communication between the NUCLEO MCU and MCP9808 temperature sensor
        @param address      The I2C bus address of the MCP9808 temperature sensor 
        '''
    
        self.i2c = i2cObject
        
        self.mcp = address
    
    
    
    
    def check(self):
        '''
        @brief      <b> Verify sensor address </b> \n
        @details    ...
        '''
        
        self.i2c.is_ready()
        
        
        
    def celsius(self):
        '''
        @brief      <b> Return measured temperature in degrees Celcius </b> \n
        @details    ...
        '''
        
    def fahrenheit(self):
        '''
        @brief      <b> Return measured temperature in degrees Fahrenheit </b> \n
        @details    ...
        '''
        
 
if __name__ == '__main__':
    # Test code
    one = 1