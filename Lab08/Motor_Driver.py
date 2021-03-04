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

 def __init__ (self, motorNum, nSLEEP_pin, nFAULT_pin, IN1_pin, channel1, IN2_pin, channel2, timer):
    ''' Creates a motor driver by initializing GPIO
     pins and turning the motor off for safety.
     @param nSLEEP_pin A pyb.Pin object to use as the enable pin.
     @param nFAULT_pin A pyb.Pin object to detect faults and trigger an external interrupt. It must be configured like this: pyb.Pin(pyb.Pin.cpu.[pinNum])
     @param IN1_pin A pyb.Pin object to use as the input to half bridge 1.
     @param channel1 A number identifier for the timer channel for pinIN1.
     @param IN2_pin A pyb.Pin object to use as the input to half bridge 2.
     @param channel2 A number identifier for the timer channel for pinIN2
     @param timer A pyb.Timer object to use for PWM generation on
     IN1_pin and IN2_pin. 
     '''
    
    ## Identifier for the motor object from constructor
    self.motorNum =     motorNum
    
    ## Defines local object for enable pin from constructor
    self.nSleep_pin =   nSLEEP_pin
    
    ## Defines local object for IN1 pin from constructor
    self.IN1_pin    =   IN1_pin
    
    ## Defines local object for IN2 pin from constructor
    self.IN2_pin    =   IN2_pin
    
    ## Defines local timer that will be used from constructor
    self.timer      =   timer
   
    # Initialize fault pin to function with external interrupt method
    self.nFault_Pin = nFAULT_pin.init(pyb.ExtInt.IRQ_FALLING,pyb.Pin.PULL_UP,faultInterrupt)
    
    ## setting up the channels for PWM on the motors
    self.timch2 = self.timer.channel(channel2,pyb.Timer.PWM,pin = self.IN2_pin)
    self.timch1 = self.timer.channel(channel1,pyb.Timer.PWM,pin = self.IN1_pin)
 

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
         self.timch2.pulse_width_percent(100)
         self.timch1.pulse_width_percent(0)
     elif(duty <= -100):
         self.timch2.pulse_width_percent(0)
         self.timch1.pulse_width_percent(100)
     
     if(duty >= 0):
         self.timch2.pulse_width_percent(duty)
         self.timch1.pulse_width_percent(0)
     elif(duty < 0):
         duty_correct = duty *(-1)
         self.timch2.pulse_width_percent(0)
         self.timch1.pulse_width_percent(duty_correct)
         
         

 ''' This method sets the duty cycle to be sent
 to the motor to the given level. Positive values
 cause effort in one direction, negative values
 in the opposite direction.
 @param duty A signed integer holding the duty
 cycle of the PWM signal sent to the motor '''

def faultInterrupt(self,fault_pin):
    '''
    External interrupt method which is triggered when the motor H-bridge fault pin goes low.
    '''
    
    # Immediately disable the motor
    self.disable()
    
    # Prompt user input before clearing fault
    cmd = input("Fault detected: Press 'f' to clear and resume functioning")
    # Proceed based on user input
    while True:
        if cmd == 'f':
            # Clear cmd variable
            cmd = None
            # Automatically re-enable the motor
            self.enable()
            break
        else:
            cmd = None
            cmd = input("Non-meaningful input detected: Press 'f' to clear fault and resume functioning")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    