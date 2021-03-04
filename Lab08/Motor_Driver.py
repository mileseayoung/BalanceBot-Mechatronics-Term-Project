''' @file Motor_Driver.py
@brief this driver controls the acuation of the motor
@details This class allows modules to setup a motor on avaliable pins and then send 
input duty cycles to it which will then use PWM to move the motor

 '''
import pyb

class MotorDriver:
 ''' This class implements a motor driver for the
 ME405 board. '''

 def __init__ (self, nSLEEP_pin, IN1_pin, IN2_pin, timer,nfault):
    ''' Creates a motor driver by initializing GPIO
     pins and turning the motor off for safety.
     @param nSLEEP_pin A pyb.Pin object to use as the enable pin.
     @param IN1_pin A pyb.Pin object to use as the input to half bridge 1.
     @param IN2_pin A pyb.Pin object to use as the input to half bridge 2.
     @param timer A pyb.Timer object to use for PWM generation on
     @param nfault A pin object for the motor nfault pin to handle motor faulting
     IN1_pin and IN2_pin. 
     '''
    self.nSleep_pin = nSLEEP_pin
    self.IN1_pin    = IN1_pin
    self.IN2_pin    = IN2_pin
    self.timer      = timer
    # This is a negative logic pin so in this case we want to be tracking falling edge
    # and in its base state will return a 1 when no fault is detected
    self.Fault      = nfault
   
    
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
      ''' This method sets the duty cycle to be sent
      to the motor to the given level. Positive values
      cause effort in one direction, negative values
      in the opposite direction.
      @param duty A signed integer holding the duty
      cycle of the PWM signal sent to the motor '''
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

 def ClearFault(self,user_reset):
    '''
    @brief to be used within external interrupts within the motor class. clears and detects faults
    @details the input is some logic value based on the user interacting with the interrupt on the program end.
    If the user sends a clear logic (1 for this program) and the fault pin read value shows it has been reset
    then the sleep Pin is turned off and the motor is reenabled.
    '''
    #if the user has input some reset condition and there is no fault detection
    if user_reset == 1 and self.Fault.value() == 1:
        #renable the motor
        self.enable()
        return('fault cleared. Good to resume operation')
    #if the user has input a reset condition but the there is still fault detection
    elif user_reset ==1 and self.Fault.value() == 0:
        self.disable()
        return('motor fault pin is still triggering. disabled motor through nSLEEPpin')
        
if __main__ == __name__:
    #setting up motor pin objects
    nSLEEP_pin = pyb.Pin(pyb.Pin.cpu.A15,pyb.Pin.OUT_PP)
    IN1_pin = pyb.Pin(pyb.Pin.cpu.B0)
    IN2_pin  = pyb.Pin(pyb.Pin.cpu.B1)
    timer = pyb.Timer(3,freq = 20000)
    nfault = pyb.Pin(pyb.Pin.board.PB2,pyb.Pin.IN)
    #importing Encoder class for testing purposes
    from encoder_craig import Encoder
    Pin1 = pyb.Pin(pyb.Pin.board.PB6)
    Pin2 = pyb.Pin(pyb.Pin.board.PB7)
    
    
    #creating motor class object
    Motor = MotorDriver(nSLEEP_pin, IN1_pin, IN2_pin, timer,nfault) 
    encoder = Encoder(Pin1,Pin2)
    #Defining interupt
    extint = pyb.ExtInt (pyb.Pin.board.PB2,   # Which pin
             pyb.ExtInt.IRQ_FALLING,       # Interrupt on falling edge
             pyb.Pin.PULL_NONE,             # Activate pullup resistor
             Motor.disable())                   # Interrupt service routine
    
    Test_speed = input('To begin testing please set a motor speed in %:')
    Motor.enable()
    Motor.set_duty(Test_speed)
    try:
        
        while True:
            encoder.update()
    except     
    
    
         
         
         
         
         



 