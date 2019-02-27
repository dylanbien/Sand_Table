#///////////////////////////////////////////////////////
#//                   Imports                        //
#//////////////////////////////////////////////////////

import time
import odrive
import usb.core
#sys.path.insert(0, "Users\SoftwareDevAdmin\Documents\RPi_ODrive")
from RPi_ODrive import ODrive_Ease_Lib

#straight line
import numpy as np
import matplotlib.pyplot as plt

#///////////////////////////////////////////////////////
#//             Global Variables                      //
#//////////////////////////////////////////////////////

#ODrive
radius_SN = 62161990005815
theta_SN = 35601883739976

#Straight Line
increments = 5.0
theta_period = 20.0
seconds_per_degree = (theta_period / 360)
straight_line_radius_time = (seconds_per_degree) * increments


outside_position = 216000
inside_position = 5000

#///////////////////////////////////////////////////////
#//                    making a design                //
#///////////////////////////////////////////////////////
def make_a_design(design, direction, side):
    
    set_radius(direction)
    #theta.set_vel(1200)???
    
    if design == "swirl":
        swirl(direction)
    if design == "shape":
        make_shape(direction, side)
#///////////////////////////////////////////////////////
#//               radius movement Function            //
#///////////////////////////////////////////////////////

def set_radius(direction):
    global outside_position
    global inside_position
    print(direction)
    if direction == "inward":
        blue_motor.set_pos(outside_position)
        orange_motor.set_pos(outside_position)
    if direction == "outward":
        blue_motor.set_pos(inside_position)
        orange_motor.set_pos(inside_position)
    if direction == "in and out":
        blue_motor.set_pos(outside_position)
        orange_motor.set_pos(inside_position)

#///////////////////////////////////////////////////////
#//               Motor Set-up                       //
#//////////////////////////////////////////////////////

dev = usb.core.find(find_all=1, idVendor=0x1209, idProduct=0x0d32)
od = []
try:
    while True:
         a = next(dev)
         od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
    print('added')
except:
    pass
print(len(od))

for odrives in od:
    print(odrives.serial_number)
    if odrives.serial_number == radius_SN:
        print ("connecting radius")
        blue_motor = ODrive_Ease_Lib.ODrive_Axis(od1.axis0)
        orange_motor = ODrive_Ease_Lib.ODrive_Axis(od1.axis1)
    elif odrives.serial_number == theta_SN:
        print("connecting theta")
        theta_motor = ODrive_Ease_Lib.ODrive_Axis(od1.axis0)


#Calibrates Motors
blue_motor.calibrate()
orange_motor.calibrate()
theta_motor.calibrate()

#home radii motors
blue_motor.home_with_vel(20000)
orange_motor.home_with_vel(20000)

#blue_motor.home_with_vel(-20000)
#blue_motor.set_pos(-5000)

#orange_motor.home_with_vel(-20000)
#orange_motor.set_pos(-5000)

#///////////////////////////////////////////////////////
#//                  Straight line                    //
#//////////////////////////////////////////////////////

def make_shape(direction, sides):
    
    global increments
    global outside_position
    global inside_position
    global straight_line_radius_time

    #angle informaton
    angle_change = 360 / sides #used in move in straight line call

    starting_r_blue = blue.get_pos()
    starting_r_orange = orange.get_pos()

    if direction == "outward":
        r_change = -20
        while (blue.get_pos() < outside_position):
            for count in sides:

                vel = move_in_straight_line(starting_r_blue, int(count * angle_change), r_change, angle_change)

                for velocities in vel:
                    blue_motor.set_vel(velocities)
                    time.sleep(straight_line_radius_time)
            starting_r_blue = blue.get_pos()

    elif direction == "inward":
        r_change = -20
        while (blue.get_pos() > inside_position):
            for count in sides:

                vel = move_in_straight_line(starting_r_blue, int(count * angle_change), r_change, angle_change)

                for velocities in vel:
                    blue_motor.set_vel(velocities)
                    time.sleep(straight_line_radius_time)

            starting_r_blue = blue.get_pos()

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

#///////////////////////////////////////////////////////
#//                   Swirl Function                  //
#///////////////////////////////////////////////////////


def swirl(direction):
    swirl_velocity = 1000
    if direction == "inward":
        blue_motor.set_vel(-1 * swirl_velocity)
        orange_motor.set_vel(-1 * swirl_velocity)
        while blue_motor.get_pos() > inside_position:
            pass
              
    elif direction == "outward":
        blue_motor.set_vel(swirl_velocity)
        orange_motor.set_vel(swirl_velocity)
        while blue_motor.get_pos() < outside_position:
            pass
              
    else: # one starts in one starts out
        blue_motor.set_vel(-1 * swirl_velocity)
        orange_motor.set_vel(swirl_velocity)
        while blue_motor.get_pos() > inside_position:
            pass
              
    blue_motor.set_vel(0)
    orange_motor.set_vel(0)

#///////////////////////////////////////////////////////
#//                   Sinusoidal Function             //
#///////////////////////////////////////////////////////

def sinusoidal(direction,constant_shift=None):
    #these numbers are subject to change after testing
    starting = 180000
    orange_motor.set_pos(starting)
    blue_motor.set_pos(starting)

    if direction == 'in':
        shift = 10000
        while shift >= 1:
            orange_motor.set_pos(starting + shift)
            blue_motor.set_pos(starting - shift)

            orange_motor.set_pos(starting - shift)
            blue_motor.set_pos(starting + shift)

            shift /= 2
    elif direction == 'out':
        shift = 1
        while shift <= 1000:
            orange_motor.set_pos(starting + shift)
            blue_motor.set_pos(starting - shift)

            orange_motor.set_pos(starting - shift)
            blue_motor.set_pos(starting + shift)

            shift *= 2
    elif direction == 'constant':

        constant_shift = 1000
        while True:
            orange_motor.set_pos(starting + constant_shift)
            blue_motor.set_pos(starting - constant_shift)

            orange_motor.set_pos(starting - constant_shift)
            blue_motor.set_pos(starting + constant_shift)

#///////////////////////////////////////////////////////
#//                   Flower Function             //
#///////////////////////////////////////////////////////

def flower(direction, sides):

    angle_change = 360 / sides
    half_a_petal = angle_change / 2
    half_a_petal_period = seconds_per_degree * half_a_petal

    petal_height = 20

    velocity = (blue_motor.get_pos + petal_height) / half_a_petal_period
    while(blue_motor.get_pos() > inside_position):
        for count in sides:
            blue_motor.set_vel(velocity)
            sleep(half_a_petal_period)
            blue_motor.set_vel(-1*velocity)
            sleep(half_a_petal_period)
            blue_motor.set_vel(0)
        blue_motor.set_pos(blue_motor.get_pos()+(petal_height / 2))



#///////////////////////////////////////////////////////
#//                   Graphing                        //
#///////////////////////////////////////////////////////

ax = plt.subplot(111, projection='polar')
make_shape(6, True, 1)
ax.set_rmax(210)
ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)
ax.set_title("Simulated Pattern", va='bottom')
plt.show()
