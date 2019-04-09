#///////////////////////////////////////////////////////
#//                   Imports                        //
#//////////////////////////////////////////////////////

import Adafruit_PCA9685
from time import sleep

#///////////////////////////////////////////////////////
#//             Global Variables                      //
#//////////////////////////////////////////////////////

red_pin = 2
blue_pin = 0
green_pin = 1

lights = Adafruit_PCA9685.PCA9684()
lights.set_pwm_frequency(1000)

#///////////////////////////////////////////////////////
#//                   Colors                          //
#//////////////////////////////////////////////////////
white = [1,1,1]
red_rover = [3000,2000,1000]

colors = [red_rover]

current_color = [white[0], white[1], white[2] ]
next_color = [white[0], white[1], white[2]]

lights.set_color(white)
def color_transition(final_color):
    global current_color
    global next_color

    next_color = final_color
    color_difference = []
    for i in range(len(current_color)):  #finding the change in PWM value for all 3 colors
        color_difference.append(abs(next_color[i]-current_color[i]))

    min_difference = min(color_difference) #find the min change
    location = color_difference.index(min_difference) #find the location of the min chagne

    change_per=[]
    for i in range(len(color_difference)): #takes the change per and divides by minimum difference get something like (1,-2, 4) **one value will be +-1
        change_per.append(int((next_color[i]-current_color[i]) / min_difference))

    for i in range (current_color(location), next_color(location)): # going from 400 to 600
        lights.set_pwm(red_pin, change_per(0),0)
        lights.set_pwm(green_pin, change_per(1),0)
        lights.set_pwm(blue_pin, change_per(2),0)

    set_color(next_color)


def set_color(color):
    global current_color
    lights.set_pwm(red_pin,color[0],0)
    lights.set_pwm(green_pin, color[1], 0)
    lights.set_pwm(blue_pin, color[2],0)
    current_color = [color[0], color[1], color[2]]

def set_pin(pin,value):
    lights.set_pwn(pin,value,0)
    current_color[pin] = value



