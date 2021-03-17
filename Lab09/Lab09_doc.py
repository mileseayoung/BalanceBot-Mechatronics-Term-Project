# -*- coding: utf-8 -*-
"""
@file Lab09_doc.py

@author: Miles Young Craig Kimball
@date 3/11/21
@page Lab09_sec Balance Board Project
@section Intro_sec Background on Balance Board
The final project for ME405 is to utilize all the skills learned in the class, and built
drivers throughout the quarter to implement a closed loop controller on hardware to create
a balancing board that can keep a ball balanced in the center of a platform. Pictured below is the 
hardware used for this project

@image html Lab09_pushrod.png width=500cm

The balance board is controlled by two motors mounted on the lower part of the platofrm, that
have a 2 bar linkage connected from the motor shaft to the edge of the balance platform. By
rotating the motor the balance board can be tilted in the X and Y plane of motion. The balance board
itself is also attached to a universal Ujoint as shown in thepicture above that allows for motion
in either plane and supports the weight of the balance board. 

On top of the balance board a resistive touch sensor is attached, which acts as the balancing 
platform for a rubber ball that will roll freely on the platform. This system was modeled to create
the state space controller for acuating the platform. More reading on this modeling can be found on the documentation
pages for Lab05 and Lab06 if desired.

@image html Lab09_ballPlat.png width=500cm

@section Drivers_sec Drivers 
In this project a number of self built drivers are utilized for the control of the balance board.
A list of Drivers, with their basic functions is given below. For a more detailed descripton of each driver, refer
to its documentation on the website:
    - \b Motor Driver: \b Controls the operation of each motor. Handles setting duty cycle and disabling during faults
    - \b Encoder Driver:\b Read and tracks position values from the quadrature encoders attached to motor shafts. Also allows the ability to zero position
    - \b Touch Panel Driver: \b Checks to see if the ball is making contact with the touch panel and returns \c [x,y] \c as a tuple.
For the Motor Driver and Encoder Driver, two instances of each are used in the project, one of each
motor linkage on each side of the balance board.

@section bno055_sec bno055 sensor

For this project the team attempted to utilize the bno055 sensor for use in calibrating the resting position of the board.
The sensor contains a gyrosope, magnetometer and acelerometer. The baord was soldered onto the top of the balance board and 
was meant to be communicated to over I2c. For use of the sensor the team used the following Driver from GitHub, that setup use of the sensor
with micropython. Source:https://github.com/micropython-IMU/micropython-bno055

@section Controller_sec Controller
This system utilizes a Closed loop Controller to balance the ball on the platform.
a screenchot of a visual representaiton of the controller is given below.

@image html Lab06_model.png

The closed loop system works for a single axis and motor. In the real system, this controller
will be applied in to instances, much like the motor and encoder objects; one to control each axis x and y respectively.
For this controller to work with the real system initial gain values needed to be determined analytically, before tuning to final values.
In order to do this the team simplified the A B matrices into 2x1 matrices as the inputs to the system control Angular position and velocity. for the initial
system a damping ratio of 0.75 was chosen and an wn of 100 was selected. Below is the work to determine these analytical gains.

@image html Lab09_calc1.png width=800cm
@image html Lab09_calc2.png width=800cm

These calculations solved for two gain values for implenting a balancing platform that focused on keeping the platform
level, not dealing with the ball. Next full system analytical calcualtions performed using the method shown by Charlie by creating the charateristic
polynomial

@image html Lab09_calc3.png width=800cm
@image html Lab09_calc4.png width=800cm


Once these values were implented into the system the team could then tune the actual system to account for any assumptions made during the system modeling step in Lab05 and Lab06.
For the actual system a controller method was developed that would take gains as an input and determine the necessary torque for the motor ofr a given axis.
Code from the teams method is shown below.

When implenting the system the team first decided to get the platform to balance itself
without introduction of the ball. This meant that the controller would only need to gains
and the touch panel would not need to be called or operated. Below is a code snippet from the code used to balance
just the platform when working on the initial design
    
    if state == 1:
                #finding theta from 0 on X axis
                Encoder1.update()
                xtick = Encoder1.getPosition()
                X = Encoder1.tick2deg(xtick)
                
                X_dot = Encoder1.getDelta() / (interval*1e6)
                plat_paramX = [X,X_dot]
                
                #finding theta from 0 on Y axis
                Encoder2.update()
                ytick = Encoder2.getPosition()
                Y = Encoder2.tick2deg(ytick)
                Y_dot = Encoder2.getDelta() / interval*(1e6)
                
                plat_paramY = [Y,Y_dot]
                #print([Y,Y_dot])
                # reading Ball positoin


    if state == 2:
                '''
                In this state values are to be fed into a controller. The controller
                will then calculate a Torque output for a motor and that will be converted to a duty
                cycle that is then applied to the motor.
                '''
                
                InputTx = (plat_paramX[0] * (-gains[0])) + ((-gains[1])*plat_paramX[1])
                InputTy = (plat_paramY[0] * (-gains[0])) + ((-gains[1])*plat_paramY[1])
                
                Motorx_feed = int(((Resistance / (Kt * Vdc)) * InputTx)*100)
                Motory_feed = int(((Resistance / (Kt * Vdc)) * InputTy)*100)
                print([Motorx_feed,Motory_feed])
                
                Motor1.setDuty(Motorx_feed)
                Motor2.setDuty(Motory_feed)
                state = 1
                
From the initial run of the program the team got the following result

<a href = "https://drive.google.com/file/d/1pfEcK9UwgfAlWt_J4Or2Do03mU3HuY0M/view?usp=sharing">LAB09 Untuned System Video</a>

The team seemed to have significant issue with the platform over correcting and faulting
even after some tuning was attempted. What the team found was that the values seemed to be off by a factor
of 1000. Upon inspection one of the teammates found that there were inconsistent units being used in the program.
Once that was corrected gains were reimplemented. The new gain matrix showed [-0.7,-0.2,-0.03,-0.2]

<a href = "https://drive.google.com/file/d/1uJaXUN2qS7n4puEiOx6P9G5jeTDpZMB-/view?usp=sharing">Lab09 Tuning Attempt 1</a>

From this video you can see that the system is now responding correctly to the ball rolling around the board but at the wrong magnitude. The team, after some discussion with other teams in office hours found
that loosening the joint connecting the push rod to the motor arm decreased stiction in the system and improved motor response sensitivity. Further tuning
was done with the loosened joint. New tuned values were found [K1,K2,K3,K4]

Here is a video of the final system


"""

