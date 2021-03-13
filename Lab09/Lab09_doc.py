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

@image html XXXX.png <---- Balance board hardware 

The balance board is controlled by two motors mounted on the lower part of the platofrm, that
have a 2 bar linkage connected from the motor shaft to the edge of the balance platform. By
rotating the motor the balance board can be tilted in the X and Y plane of motion. The balance board
itself is also attached to a universal Ujoint as shown in thepicture above that allows for motion
in either plane and supports the weight of the balance board. 

On top of the balance board a resistive touch sensor is attached, which acts as the balancing 
platform for a rubber ball that will roll freely on the platform. This system was modeled to create
the state space controller for acuating the platform. More reading on this modeling can be found on the documentation
pages for Lab05 and Lab06 if desired.

@image html XXX.png <------ Touch Panel with Ball on it

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

@image html XXX>png <------- Analytical gain calcs.

Once these values were implented into the system the team could then tune the actual system to account for any assumptions made during the system modeling step in Lab05 and Lab06.
For the actual system a controller method was developed that would take gains as an input and determine the necessary torque for the motor ofr a given axis.
Code from the teams method is shown below.


From the initial run of the program the team got the following result

#insert image, graph video text.

Eventually the system was further tuned to have gain valus of X X X X

Here is a video of the final system

"""
