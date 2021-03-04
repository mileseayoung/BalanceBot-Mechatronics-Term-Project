''' @file Motor_Driver.py
@brief this driver controls the acuation of the motor
@details This class allows modules to setup a motor on avaliable pins and then send 
input duty cycles to it which will then use PWM to move the motor
Source Code: https://bitbucket.org/CraigKimball/me305_labs/src/master/Lab06/Motor_Driver.py
 '''
import pyb

class MotorDriver:
 ''' This class implements a motor driver for the
 ME405 board. '''

 def __init__ (self, nSLEEP_pin, nFAULT_pin, IN1_pin, IN2_pin, timer):
    ''' Creates a motor driver by initializing GPIO
     pins and turning the motor off for safety.
     @param nSLEEP_pin A pyb.Pin object to use as the enable pin.
     @param nFAULT_pin A pyb.Pin object to detect faults and trigger an external interrupt. It must be configured like this: pyb.Pin(pyb.Pin.cpu.[pinNum], mode = IN, pull = pyb.Pin.PULL_UP)
     @param IN1_pin A pyb.Pin object to use as the input to half bridge 1.
     @param IN2_pin A pyb.Pin object to use as the input to half bridge 2.
     @param timer A pyb.Timer object to use for PWM generation on
     IN1_pin and IN2_pin. 
     '''
    self.nSleep_pin = nSLEEP_pin
    self.IN1_pin    = IN1_pin
    self.IN2_pin    = IN2_pin
    self.timer      = timer
   
    
    ## setting up the channel 4 for PWM on the motors
    self.t3ch2 = self.timer.channel(4,pyb.Timer.PWM,pin = self.IN2_pin)
    ## Setting up the channel 5 for PWM on the motors
    self.t3ch1 = self.timer.channel(3,pyb.Timer.PWM,pin = self.IN1_pin)
 

## Sets the sleep pin of the motor to high
 def enable (self):
     #print ('Enabling Motor')
     self.nSleep_pin.high()
     self.t3ch2.pulse_width_percent(0)
     self.t3ch1.pulse_width_percent(0)
## sets the sleep pin of the motor to low
 def disable (self):
     print ('Disabling Motor')
     self.nSleep_pin.low()
     
## sets the duty cycle of the motor.
# This is also referred to the acuation value controlled by PWM represented as a %
 def set_duty (self, duty):
     
     # Saturation prevention on motor. Will not let PWM go above 100%
     if (duty >= 100):
         self.t3ch2.pulse_width_percent(100)
         self.t3ch1.pulse_width_percent(0)
     elif(duty <= -100):
         self.t3ch2.pulse_width_percent(0)
         self.t3ch1.pulse_width_percent(100)
     
     if(duty >= 0):
         self.t3ch2.pulse_width_percent(duty)
         self.t3ch1.pulse_width_percent(0)
     elif(duty < 0):
         duty_correct = duty *(-1)
         self.t3ch2.pulse_width_percent(0)
         self.t3ch1.pulse_width_percent(duty_correct)
         
         

 ''' This method sets the duty cycle to be sent
 to the motor to the given level. Positive values
 cause effort in one direction, negative values
 in the opposite direction.
 @param duty A signed integer holding the duty
 cycle of the PWM signal sent to the motor '''

def faultInterrupt(self,fault_pin):
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    