# -*- coding: utf-8 -*-
"""
@file       TouchDriver.py
@author     Miles Young
@date       02/25/2021
@brief      <b> Resistive Touch Panel Driver </b> \n
@details    This driver class can be used to scan for a point of contact on a 
            resistive touch panel. Its constructor requires 4 pin objects - one 
            for each of the nodes of the resistive elements within the panel - 
            as well as a measurement for the width and length of the panel in 
            units of cm. The center coordinate of the panel can also be defined, 
            although it is set as an origin by default. This class has 4 methods; 
            xscan() and yscan() determine the x- and y-position, respectively, 
            of the point of contact on the panel from the center coordinates; 
            zscan() determines whether an object is in contact with the panel; and 
            read() scans all three consecutively and returns a tuple containing 
            their readings. Source Code: https://bitbucket.org/MilesYoung/lab-4-term-project/src/master/Lab09/TouchDriver.py
"""

from pyb import Pin, ADC
import utime

class TouchDriver:
    '''
    @brief      <b> Resistive touch panel driver class </b> \n
    '''
    
    def __init__(self,pinxp,pinxm,pinyp,pinym,width,length,center = [0,0]):
        '''
        @brief          <b> Constructor </b> \n
        @details        This constructor requires that the user create and input 
                        four pins to correspond to the x and y positive and 
                        negative nodes of the touch panel. It also requires that 
                        the user input the length (x-direction) and width (y-direction) 
                        of the panel, as well as the coordinates for the center 
                        of the panel. Any units can be used as long as they are 
                        consistent throughout.
        @param pinxp    Pin object corresponding to the positive x node of the touch panel
        @param pinxm    Pin object corresponding to the negative x node of the touch panel
        @param pinyp    Pin object corresponding to the positive y node of the touch panel
        @param pinym    Pin object corresponding to the negative y node of the touch panel
        @param width    The width of the resistive touch panel
        @param length   The length of the resistive touch panel
        @param center   Coordinates representing the center of the resistive touch panel. Must be input as a 1x2 list of the form [x,y]. Default center coordinates are [0,0].
        '''
    
        ## Define xp pin within class based on user input in constructor
        self.pinxp = pinxp
        
        ## Define xm pin based on user input in constructor
        self.pinxm = pinxm
        
        ## Define yp pin based on user input in constructor
        self.pinyp = pinyp
        
        ## Define ym pin based on user input in constructor
        self.pinym = pinym
        
        ## Define touch plate width based on user input in constructor
        self.width = width
        
        ## Define touch plate length based on user input in constructor
        self.length = length
        
        ## Define touch plate center coordinates based on user input in constructor
        self.center = center
    
    
    def xScan(self):
        '''
        @brief          <b> X position scan </b> \n
        @details        This method reconfigures the touch panel pins so that 
                        the xp pin is a high output, the xm pin is a low output, 
                        the yp pin is an inactive input, and the ym pin is an ADC 
                        input. It then waits a duration of 3.6 us to account for 
                        the settling time after pin reassignment and proceeds to 
                        measure and scale the ADC input.
        @return xpos    x position measured from the center of the touch panel
        '''
        
        # Reconfigure pins
        self.pinxp.init(Pin.OUT_PP)
        self.pinxp.high()
        self.pinxm.init(Pin.OUT_PP)
        self.pinxm.low()
        self.pinyp.init(Pin.IN)
        ## Define ADC object to read from ym pin
        #self.pinym.init(mode = Pin.ANALOG)
        xADC = ADC(self.pinym)
        
        # Sample ADC readings
        # Delay 3.6 microseconds to account for resistor settling time
        utime.sleep_us(4)
        # Read adc channel to find unscaled x position
        xpos = xADC.read()
        # Scale x position
        xpos = xpos*(self.length/(3800-200)) - self.center[0]
        
        return xpos
        
    def yScan(self):
        '''
        @brief          <b> Y position scan </b> \n
        @details        This method reconfigures the touch panel pins so that 
                        the xp pin is an inactive input, the xm pin is an ADC, 
                        the yp pin is a high output, and the ym pin is a low output. 
                        It then waits a duration of 3.6 us to account for the 
                        settling time after pin reassignment and proceeds to 
                        measure and scale the ADC input.
        @return ypos    y position measured from the center of the touch panel
        '''
        
        # Reconfigure pins
        self.pinxp.init(Pin.IN)
        #self.pinxm.init(Pin.ANALOG)
        ## Define ADC object to read from xm pin
        yADC = ADC(self.pinxm)
        self.pinyp.init(Pin.OUT_PP)
        self.pinyp.high()
        self.pinym.init(Pin.OUT_PP)
        self.pinym.low()
        
        # Sample ADC readings
        # Delay 3.6 microseconds to account for resistor settling time
        utime.sleep_us(4)
        # Read adc channel to find unscaled y position
        ypos = yADC.read()
        # Scale x position
        ypos = ypos*(self.width/(3600-400)) - self.center[1]
        
        return ypos
        
    def zScan(self):
        '''
        @brief          <b> Contact scan </b> \n
        @details        This method reconfigures the touch panel pins so that 
                        the xp pin is an inactive input, the xm pin is a low output, 
                        the yp pin is a high output, and the ym pin is an ADC. 
                        It then waits a duration of 3.6 us to account for the 
                        settling time after pin reassignment and proceeds to 
                        measure the ADC input. Last, it determines whether the 
                        there is contact with the touch panel
        @return zflag   A boolean representing the state of contact
        '''
        
        
        # Reconfigure pins
        self.pinxp.init(Pin.IN)
        self.pinxm.init(Pin.OUT_PP)
        self.pinxm.low()
        self.pinyp.init(Pin.OUT_PP)
        self.pinyp.high()
        #self.pinym.init(Pin.ANALOG)
        ## Define ADC object to read from ym pin
        zADC = ADC(self.pinym)
        
        # Sample ADC readings
        # Delay 3.6 microseconds to account for resistor settling time
        utime.sleep_us(4)
        # Read adc channel to find unscaled y position
        ## Variable to hold bit ADC reading
        zReading = zADC.read()
        # Determine boolean state to return  
        if zReading < 4000:
           zFlag = True
        else:
            zFlag = False
        
        # Filter ADC Readings
        return zFlag
        #return zflag
        
    def read(self):
        '''
        @brief              <b> Total position scan </b> \n
        @details            This method utilizes the xscan(),yscan(), and zscan() 
                            methods to create and returna tuple containing all 
                            three positional measurements.
        @return position    A tuple containing the outputs of xscan(), yscan(), 
                            and zscan() in the following order: [xpos, ypos, zflag ]
        '''
        
        # Scan x, y, and z into a position tuple
        position = [self.zScan(),self.xScan(),self.yScan()]
        
        return position
                            
        
        
if __name__ == "__main__":
        
    # Create pin objects
    pinxp = Pin(Pin.cpu.A7)
    pinxm = Pin(Pin.cpu.A1)
    pinyp = Pin(Pin.cpu.A6)
    pinym = Pin(Pin.cpu.A0)
    
    # Define platform dimensions
    width = 0.108
    length = 0.186
    center = [0.105,0.067]
    
    # Create touch panel driver object
    touchObject = TouchDriver(pinxp,pinxm,pinyp,pinym,width,length,center)
    
    # Test scanning methods and observe timing
    # Test zScan()
    startTime = utime.ticks_us()
    zTest = touchObject.zScan()
    endTime = utime.ticks_us()
    print('Time: {:}, z-state: {:}'.format(utime.ticks_diff(endTime,startTime),zTest))  

    # Test xScan()
    startTime = utime.ticks_us()
    xTest = touchObject.xScan()
    endTime = utime.ticks_us()
    print('Time: {:}, x-value: {:}'.format(utime.ticks_diff(endTime,startTime),xTest))

    # Test yScan()
    startTime = utime.ticks_us()
    yTest = touchObject.yScan()
    endTime = utime.ticks_us()
    print('Time: {:}, y-value: {:}'.format(utime.ticks_diff(endTime,startTime),yTest))
       
    # Test read() to find average runtime of all 3 scans
    timeSum = 0
    for n in range(100):
        startTime = utime.ticks_us()
        readTest = touchObject.read()
        endTime = utime.ticks_us()
        testTime = utime.ticks_diff(endTime,startTime)
        timeSum += testTime
    timeAvg = timeSum/100    
    print('Average Time: {:}'.format(timeAvg))
    
       
        
        
        
    