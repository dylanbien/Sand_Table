from time import sleep
import odrive
import usb.core

import ODrive_Ease_Lib
#import numpy as np

class motor_setup:
    
    #Straight Line
    increments = 5.0
    theta_period = 49.1
    seconds_per_degree = (theta_period / 360)
    straight_line_radius_time = (seconds_per_degree) * increments
    
    outside_position = -200000
    inside_position = -20000
    
    def __init__(self):
        
        #ODrive
        self.radius_SN = 62011668378679
        self.theta_SN = 62161990005815

        dev = usb.core.find(find_all=1, idVendor=0x1209, idProduct=0x0d32)
        od = []

        a = next(dev)
        od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
        print('connected 1')
        a = next(dev)
        od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
        print('connected 2')

        if od[0].serial_number == self.radius_SN:
            self.radius_odrive = od[0]
            self.theta_odrive = od[1]
        else:
            self.radius_odrive = od[1]
            self.theta_odrive = od[0]


        self.blue_motor = ODrive_Ease_Lib.ODrive_Axis(self.radius_odrive.axis0)
        #self.orange_motor = ODrive_Ease_Lib.ODrive_Axis(self.radius_odrive.axis1)

        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_odrive.axis0, 200000)

        print('assigned axises')
    
    def calibrate_theta(self):
        
        self.theta_motor.calibrate()
        print('theta calibrated')
        
    def calibrate_radius(self):
        
        self.blue_motor.calibrate()
        print('radius calibrated') 
#///////////////////////////////////////////////////////
#//               theta movement Function            //
#///////////////////////////////////////////////////////
    def start_theta(self):
        self.theta_motor.set_vel(50000)
        sleep(2)
        self.theta_motor.set_vel(100000)
        sleep(2)
        self.theta_motor.set_vel(150000)
        print("theta moving")

    def stop_theta(self):
        self.theta_motor.set_vel(0)
        
#///////////////////////////////////////////////////////
#//               radius movement Function            //
#///////////////////////////////////////////////////////

    def set_radius(self,location):
        
        print(location)
        if location == "outside":
            self.blue_motor.set_pos(self.outside_position)
            #self.orange_motor.set_pos(self.outside_position)
        if location == "inside":
            self.blue_motor.set_pos(self.inside_position)
            #self.orange_motor.set_pos(self.inside_position)
    


    def cart2pol(self, x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return(rho, phi)

    def pol2cart(self, rho, phi):
        x = rho * np.cos(np.deg2rad(phi))
        y = rho * np.sin(np.deg2rad(phi))
        return(x, y)

    
    def move_in_straight_line(self, starting_r, starting_theta, r_change, angle_change):

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

    def spiral(self, dir):
        if dir == 'out':
            edge = -200000
        else:
            edge = -20000


        while self.blue_motor.get_pos() > edge:
            self.blue_motor.set_vel(-5000)
        self.blue_motor.set_vel(0)
