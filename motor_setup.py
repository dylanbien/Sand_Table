from time import sleep
from time import time 
import odrive
import usb.core

import ODrive_Ease_Lib
import numpy as np

class motor_setup:
    
    #Straight Line
    increments = .1
    theta_period = 49.1
    seconds_per_degree = (theta_period / 360)
    straight_line_radius_time = (seconds_per_degree) * increments       
    
    outside_position = -200000
    inside_position = -20000

    
#///////////////////////////////////////////////////////
#//                    Initialization                 //
#///////////////////////////////////////////////////////    

   
    def __init__(self):
        
        #ODrive
        self.radius_SN =  35799416975435
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


        self.odin = ODrive_Ease_Lib.ODrive_Axis(self.radius_odrive.axis0, 100000)
        self.zeus = ODrive_Ease_Lib.ODrive_Axis(self.radius_odrive.axis1, 100000)

        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_odrive.axis0, 200000)

        print('assigned axises')

    def set_increments(self, inc):
        self.increments = inc
        self.straight_line_radius_time = (self.seconds_per_degree) * self.increments
        print('time: ' + str(self.straight_line_radius_time))
    
    def reboot_blue(self):
        try:
            self.odin.reboot()
        except:
            print('nope')
    
    def reboot_theta(self):
        try:
            self.theta_motor.reboot()
        except:
            print('nope')
    
        
#///////////////////////////////////////////////////////
#//                     Calibration                  //
#///////////////////////////////////////////////////////

        
    def calibrate_theta(self):
        
        self.theta_motor.encoder_calibrate()
        self.theta_motor.set_curr_limit(13)
        print('theta calibrated')
        
    def calibrate_radius(self):
        
        self.odin.encoder_calibrate()
        self.zeus.encoder_calibrate()
        print('radius calibrated')
        
    def set_up_radius(self):
        
        self.odin.home_with_vel(-20000)
        self.odin.set_pos(-200000)
        while self.odin.is_busy() == True:
            pass
        
        self.zeus.home_with_vel(-20000)
        self.zeus.set_pos(-200000)
        while self.zeus.is_busy() == True:
            pass
        
        print('motors ready')

        
#///////////////////////////////////////////////////////
#//                   theta movement                  //
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
        print('theta stopped')

    
    
#///////////////////////////////////////////////////////
#//               radius movement Function            //
#///////////////////////////////////////////////////////

    def set_radius(self,location):
        
        print(location)
        if location == "outside":
            self.odin.set_pos(self.outside_position)
            self.zeus.set_pos(self.outside_position)
            
            while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                pass
            
        if location == "inside":
            self.odin.set_pos(self.inside_position)
            self.zeus.set_pos(self.inside_position)
            
            while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                pass

    def move_slowly_vel(self, end_point, velocity, dt = 0.004):
        
        distance = end_point - self.odin.get_pos()
        seconds = int(distance / velocity)
        piece_length = velocity * dt
        num_pieces = int(distance / (piece_length) )
        
        mark = time()
        
        target_pos = self.odin.get_pos()
        
        self.odin.set_pos(target_pos)
        self.zeus.set_pos(target_pos)

        for x in range (0, num_pieces):
            self.odin.set_pos_no_loop(target_pos)
            self.zeus.set_pos_no_loop(target_pos)
            target_pos += piece_length
            
            while time() < mark + dt:
                pass
            
            mark = time()
            
    
#///////////////////////////////////////////////////////
#//                        Swirl                      //
#///////////////////////////////////////////////////////    
    def spiral(self, dir):
        print('dir: ' + str(dir))
        if dir == 'out':
            self.set_radius('inside')
            print('radius set')
            sleep(2)
            self.move_slowly_vel(self.outside_position, 250)
            print('swirl completed')
        else:
            self.set_radius('outside')
            print('radius set')
            sleep(2)
            self.move_slowly_vel(self.inside_position, 250)
            print('swirl completed')


        
#///////////////////////////////////////////////////////
#//                     Sinusoidal                    //
#///////////////////////////////////////////////////////
        
        
    def sinusoidal(self, starting,direction,constant_shift=None):
        #these numbers are subject to change after testing
        #self.zeus.set_pos(starting)
        self.odin.set_pos(starting)

        if direction == 'in':
            shift = 10000
            while shift >= 1:
                #self.zeus.set_pos(starting + shift)
                self.odin.set_pos(starting - shift)
                sleep(0.1)
                #self.zeus.set_pos(starting - shift)
                self.odin.set_pos(starting + shift)

                shift /= 2
        elif direction == 'out':
            shift = 1
            while shift <= 1000:
                #self.zeus.set_pos(starting + shift)
                self.odin.set_pos(starting - shift)
                sleep(0.1)

                #self.zeus.set_pos(starting - shift)
                self.odin.set_pos(starting + shift)

                shift *= 2
        elif direction == 'constant':

            constant_shift = 20000
            while True:
                #self.zeus.set_pos(starting + constant_shift)
                self.odin.set_pos(starting - constant_shift)
                sleep(1)

                #self.zeus.set_pos(starting - constant_shift)
                self.odin.set_pos(starting + constant_shift)
    
    def flower(self,direction, sides):

        angle_change = 360 / sides
        half_a_petal = angle_change / 2
        half_a_petal_period = self.seconds_per_degree * half_a_petal

        petal_height = 20

        velocity = (self.odin.get_pos() + petal_height) / half_a_petal_period
        while(self.odin.get_pos() < self.inside_position):
            for count in range(sides+1):
                self.odin.set_vel(velocity)
                sleep(half_a_petal_period)
                self.odin.set_vel(-1*velocity)
                sleep(half_a_petal_period)
                self.odin.set_vel(0)
            self.odin.set_pos(self.odin.get_pos()+(petal_height / 2))
            
#///////////////////////////////////////////////////////
#//                     Shapes                        //
#///////////////////////////////////////////////////////

    def make_shape(self, dir, sides):
        
        #angle informaton
        angle_change = 360 / sides #used in move in straight line call
        starting_r_blue = self.odin.get_pos()
        starting_theta = 0
        r_change = 0

        radii = self.straight_line_math(starting_r_blue, starting_theta, r_change, angle_change)

        
        mark = time()
        self.odin.set_pos(radii[0])
        
        for r in radii:
            self.odin.set_pos_no_loop(r)
            
            print( time() - mark)
            
            while time() < mark + self.straight_line_radius_time:
                pass
            mark = time()
            
            
        
    def cart2pol(self, x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return(rho, phi)

    def pol2cart(self, rho, phi):
        x = rho * np.cos(np.deg2rad(phi))
        y = rho * np.sin(np.deg2rad(phi))
        return(x, y)

    
    def straight_line_math(self, starting_r, starting_theta, r_change, angle_change):

        

        number_of_increments = angle_change / self.increments #the number of x,y points used the move in straight line

        #gets the starting and ending polar cordinates
        starting_polar = [starting_r, starting_theta]
        ending_polar = [starting_polar[0] + r_change, starting_polar[1] + angle_change]

        #transfers the above to cartesian
        starting_x, starting_y = self.pol2cart(starting_polar[0], starting_polar[1])
        ending_x, ending_y = self.pol2cart(ending_polar[0], ending_polar[1])

        #use these two points to make a line: y = mx + b
        slope = (ending_y - starting_y) / (ending_x - starting_x)
        y_intercept = ending_y - (slope * ending_x) #b

        #intialize arrays
        angles = []
        radii = []

        for ang in np.arange(int(starting_polar[1]), int(ending_polar[1]+self.increments), self.increments):

            angles.append(ang)
            radii.append(y_intercept / (np.sin(np.deg2rad(ang)) - (slope * np.cos(np.deg2rad(ang)) ) ) ) #note: may need to change angles from theta to radians?
           
        print(radii)
        

    
        radius_change = []    
        a = 0
        b = 1

        for i in range(len(radii) - 1):
            radius_change.append(radii[b] - radii[a])
            a += 1
            b += 1

        #print(radius_change)
        
        

    
        velocities = []
        for distance in radius_change:
            velocities.append (distance / self.straight_line_radius_time)
        
        print(velocities)
        


        return radii

       
