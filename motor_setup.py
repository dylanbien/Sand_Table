from time import sleep
import odrive
import usb.core

import ODrive_Ease_Lib

class motot_setup:
    
    #Straight Line
    increments = 5.0
    theta_period = 49.1
    seconds_per_degree = (theta_period / 360)
    straight_line_radius_time = (seconds_per_degree) * increments
    
    
    def __init__(self):
        
        #ODrive
        radius_SN = 35601883739976
        theta_SN = 62161990005815

        dev = usb.core.find(find_all=1, idVendor=0x1209, idProduct=0x0d32)
        od = []

        a = next(dev)
        od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
        print('connected 1')
        a = next(dev)
        od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
        print('connected 2')

        if od[0].serial_number == radius_SN:
            radius_odrive = od[0]
            theta_odrive = od[1]
        else:
            radius_odrive = od[1]
            theta_odrive = od[0]


        blue_motor = ODrive_Ease_Lib.ODrive_Axis(radius_odrive.axis0)
        orange_motor = ODrive_Ease_Lib.ODrive_Axis(radius_odrive.axis1)

        theta_motor = ODrive_Ease_Lib.ODrive_Axis(theta_odrive.axis0, 200000)

        print('assigned axises')
    
    def calibrate_motors(self):
        
        self.theta_motor.calibrate()
        print('theta calibrated')
        
        self.blue_motor.calibrate()
        


    

    def cart2pol(self, x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return(rho, phi)

    def pol2cart(self, rho, phi):
        x = rho * np.cos(np.deg2rad(phi))
        y = rho * np.sin(np.deg2rad(phi))
        return(x, y)

    def spiral(self, dir):
        if dir == 'out':
            edge = -200000
        else:
            dir = -20000


        while blue_motor.get_pos() > edge:
            blue_motor.set_vel(-5000)
        blue_motor.set_vel(0)

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
