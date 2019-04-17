#Straight Line
increments = 5.0
theta_period = 49.1
seconds_per_degree = (theta_period / 360)
straight_line_radius_time = (seconds_per_degree) * increments
#import numpy as np
#import matplotlib.pyplot as plt
import odrive
from RPi_ODrive import ODrive_Ease_Lib
from time import sleep
print ("connecting radius")
radius_odrive = odrive.find_any() 
blue_motor = ODrive_Ease_Lib.ODrive_Axis(radius_odrive.axis0)
orange_motor = ODrive_Ease_Lib.ODrive_Axis(radius_odrive.axis1)

blue_motor.calibrate()
blue_motor.home_with_vel(-10000)
sleep(2)
blue_motor.set_pos(-100000)

def make_shape():
    
    global increments
    global outside_position
    global inside_position
    global straight_line_radius_time

    #angle informaton
    angle_change = 360 / sides #used in move in straight line call

    starting_r_blue = -1 * blue_motor.get_pos()
    
    vel = move_in_straight_line(starting_r_blue, 0, 0, 120)

    for velocities in vel:
        blue_motor.set_vel(-1 * velocities)
        sleep(straight_line_radius_time)
                    

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(np.deg2rad(phi))
    y = rho * np.sin(np.deg2rad(phi))
    return(x, y)


def move_in_straight_line(starting_r, starting_theta, r_change, angle_change):
   
    global increments
    global straight_line_radius_time

    number_of_increments = angle_change / increments #the number of x,y points used the move in straight line

    #gets the starting and ending polar cordinates
    starting_polar = [starting_r, starting_theta]
    ending_polar = [starting_polar[0] + r_change, starting_polar[1] + angle_change]

    #transfers the above to cartesian
    starting_x, starting_y = pol2cart(starting_polar[0], starting_polar[1])
    ending_x, ending_y = pol2cart(ending_polar[0], ending_polar[1])

    #use these two points to make a line: y = mx + b
    slope = (ending_y - starting_y) / (ending_x - starting_x)
    y_intercept = ending_y - (slope * ending_x) #b
    
    #intialize arrays
    angles = []
    radii = []

    for ang in range(int(starting_polar[1]), int(ending_polar[1]+increments)  , increments):
        
        angles.append(ang)
        radii.append(y_intercept / (np.sin(np.deg2rad(ang)) - (slope * np.cos(np.deg2rad(ang)) ) ) ) #note: may need to change angles from theta to radians?
        plt.polar(angles[len(angles)-1]*(np.pi/180), radii[len(angles)-1],'k.')

    print(angles)
    print(radii)

    
    radius_change = []    
    a = 0
    b = 1
    
    for i in range(int(number_of_increments )):
        radius_change.append(radii[b] - radii[a])
        a += 1
        b += 1
        
    print(radius_change)

    velocities = []

    for distance in radius_change:
        velocities.append (distance / straight_line_radius_time)

    print(radii)
    print(velocities)
    
    return velocities
