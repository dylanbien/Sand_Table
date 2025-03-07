from time import sleep
from time import time 
import odrive
import usb.core

import ODrive_Ease_Lib
import numpy as np

class motor_setup:
    
    #Straight Line
    increments = .1
    theta_period = 36.74
    seconds_per_degree = (theta_period / 360)
    straight_line_radius_time = (seconds_per_degree) * increments       
    
    outside_position = -195000
    inside_position = -5000

    
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
        print('waiting')
        sleep(2)
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
        
        self.radius_odrive.axis0.controller.config.vel_limit_tolerance = 0
        self.radius_odrive.axis1.controller.config.vel_limit_tolerance = 0 

        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_odrive.axis0, 200000)
        
        
        self.odin.set_calibration_current(20)
        self.zeus.set_calibration_current(20)
        
        self.odin.set_curr_limit(20)
        self.zeus.set_curr_limit(20)
        
        


        print('assigned axises')
        
    def prepare_table(self):
      
        self.calibrate_all()
        sleep(1)
        self.start_theta()
        sleep(1)
        self.set_up_radius()
       
    def set_inc(self,inc):
        self.increments = inc
        self.straight_line_radius_time = (self.seconds_per_degree) * self.increments
            
#///////////////////////////////////////////////////////
#//                     Calibration                  //
#///////////////////////////////////////////////////////

        
    def calibrate_theta(self):
        print('calibrating theta')
        self.theta_motor.calibrate_encoder()
        print('theta calibration completed')
        
    def calibrate_radius(self):
        print('calibrating radii')
        self.odin.calibrate_encoder()
        self.zeus.calibrate_encoder()
        print('radii calibration completed')
        
    def calibrate_all(self):
        ODrive_Ease_Lib.calibrate_list( [ self.odin, self. zeus, self.theta_motor] )
        
    def set_up_radius(self):
        
        print('getting motors ready')
        
        self.odin.home_with_vel(-30000)
        self.zeus.home_with_vel(-30000)
        self.set_radius('outside')
        
        print('motors ready')

        
#///////////////////////////////////////////////////////
#//                   theta movement                  //
#///////////////////////////////////////////////////////

        
    def start_theta(self):
        sleep(1)
        self.theta_motor.set_vel(-200000)
        print("theta moving")

    def stop_theta(self):
        self.theta_motor.set_vel(0)
        print('theta stopped')

    
#///////////////////////////////////////////////////////
#//                        Swirl                      //
#///////////////////////////////////////////////////////    
    def spiral(self, dir):
        print('dir: ' + str(dir))
        if dir == 'out':
            self.set_radius('inside')
            print('radius set')
            self.move_slowly_vel(self.outside_position, -175)
            print('swirl completed')
        elif dir == 'in':
            self.set_radius('outside')
            print('radius set')
            self.move_slowly_vel(self.inside_position, 175)
            print('swirl completed')
            
    def move_slowly_vel(self, end_point, velocity, dt = 0.01):
        
        distance = end_point - self.odin.get_pos()
        seconds = int(distance / velocity)
        piece_length = velocity * dt
        num_pieces = abs(int(distance / (piece_length) ))
        
        
        
        target_pos = self.odin.get_pos()
        
        self.odin.set_pos(target_pos)
        self.zeus.set_pos(target_pos)
        
        mark = time()
        
        for x in range (0, num_pieces):
            self.odin.set_pos_no_loop(target_pos)
            self.zeus.set_pos_no_loop(target_pos)
            
            target_pos += piece_length
            
            while time() < mark + dt:
                pass

            mark = time()

        
#///////////////////////////////////////////////////////
#//                     Sinusoidal                    //
#///////////////////////////////////////////////////////
        
        
    def sinusoidal(self, starting, direction, constant_shift=None):
        #these numbers are subject to change after testing
        self.zeus.set_pos(starting)
        self.odin.set_pos(starting)
        while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass

        if direction == 'in':
            shift = 30000
            while shift >= 1:
                self.zeus.set_pos(starting + shift)
                self.odin.set_pos(starting - shift)
                
                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass
                
                self.zeus.set_pos(starting - shift)
                self.odin.set_pos(starting + shift)

                shift /= 1.3
                
                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass
        elif direction == 'out':
            shift = 50
            while shift <= 50000:
                self.zeus.set_pos(starting + shift)
                self.odin.set_pos(starting - shift)
                
                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass

                self.zeus.set_pos(starting - shift)
                self.odin.set_pos(starting + shift)

                shift *= 1.3
                
                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass
        elif direction == 'constant':

            constant_shift = 10000
            t = time()
            while time() <= (t+37) :
                self.zeus.set_pos(starting + constant_shift)
                self.odin.set_pos(starting - constant_shift)
                
                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass

                self.zeus.set_pos(starting - constant_shift)
                self.odin.set_pos(starting + constant_shift)
                
                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass

    def cooler_sinusoidal(self,starting,direction):
        self.sinusoidal(starting,direction)
        self.sinusoidal(starting+20000,direction)
        
#///////////////////////////////////////////////////////
#//                       Flower                      //
#///////////////////////////////////////////////////////        
    
    
    def flower(self, starting, sides):
        self.set_radius(starting)
        while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass
        angle_change = 360 / sides
        half_a_petal = angle_change / 2
        half_a_petal_period = self.seconds_per_degree * half_a_petal

        petal_height = 20

        velocity = (self.odin.get_pos() + petal_height) / half_a_petal_period
        t = time()
        
        while(time() < (t+self.theta_period-1)):
            for count in range(sides+1):
                self.odin.set_vel(velocity)
                sleep(half_a_petal_period)
                self.odin.set_vel(-1*velocity)
                sleep(half_a_petal_period)
                self.odin.set_vel(0)
            self.odin.set_pos(self.odin.get_pos()+(petal_height / 2))
        self.set_radius(starting)
#///////////////////////////////////////////////////////
#//                     Shapes                        //
#///////////////////////////////////////////////////////

    def make_shape(self, dir, sides):
        
        #angle informaton
        angle_change = 360 / sides #used in move in straight line call
        
        starting_theta = 0

        if dir == 'outward':
            self.set_radius(-50000)
            r_change = -1 * (3000.0 / sides)
        elif dir == 'inward':
            self.set_radius('outside')
            r_change = (3000.0 / sides)

        if sides % 2 == 0:
            r_change = r_change / 2.
            
        while True:
            
            i = 0
            while(i<sides):
                
                  #Where should this be???
                
                starting_r = self.zeus.get_pos()

                radii = self.straight_line_math(starting_r, starting_theta, r_change, angle_change)
                print(r_change)
                print(radii[0])
                print(radii[len(radii)-1])
                

                inner_r = radii[ int(len(radii) / 2.0 )]
                if inner_r > -20000.0 or inner_r < self.outside_position:  #may need to cahnge inside position variable to some arbitary amount
                    print(str(r))
                    return

                self.zeus.set_pos(radii[0])
                self.odin.set_pos(radii[0])
                    
                mark = time()
                
                for r in radii:
                     
                    self.zeus.set_pos_no_loop(r)
                    self.odin.set_pos_no_loop(r)
          
                     #print((mark + self.straight_line_radius_time) - time())

                    while time() < mark + self.straight_line_radius_time:
                        pass
         
                    mark = time()
                     
               
                
                i += 1
                
                   
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
            radii.append(y_intercept / (np.sin(np.deg2rad(ang)) - (slope * np.cos(np.deg2rad(ang)) ) ) ) 
           
        #print(radii)
            
        return radii

       
#///////////////////////////////////////////////////////
#//               Setting the Radii             //
#///////////////////////////////////////////////////////

    def set_radius(self, location, motors = 'both'):
        
        print('motors: ' + motors + ', location: ' + str(location))
        self.odin.set_vel_limit(20000)
        self.zeus.set_vel_limit(20000)
        
        if motors == 'both':
            if location == "outside":
                self.odin.set_pos(self.outside_position)
                self.zeus.set_pos(self.outside_position)

                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass

            elif location == "inside":
                self.odin.set_pos(self.inside_position)
                self.zeus.set_pos(self.inside_position)

                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass
                
            elif location == "middle":
                self.odin.set_pos((self.outside_position + self.inside_position)/2.0 )
                self.zeus.set_pos((self.outside_position + self.inside_position)/2.0 )

                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass
                
            elif location == "opposite":
                self.odin.set_pos(self.outside_position)
                self.zeus.set_pos(self.inside_position)

                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    
                    pass
            else:
                
                self.odin.set_pos(location)
                self.zeus.set_pos(location)

                while (self.zeus.is_busy() == True and self.odin.is_busy() == True):
                    pass

    
        else:
            
            if location == "outside":
                
                if motors == "odin":
                    self.odin.set_pos(self.outside_position)
                    while (self.odin.is_busy() == True):
                           pass
                elif motors == "zeus":
                    self.zeus.set_pos(self.outside_position)
                    while (self.zeus.is_busy() == True):
                           pass
                
            elif location == "inside":
                if motors == "odin":
                    self.odin.set_pos(self.inside_position)
                    while (self.odin.is_busy() == True):
                           pass
                elif motors == "zeus":
                    self.zeus.set_pos(self.inside_position)
                    while (self.zeus.is_busy() == True):
                           pass

            elif location == "middle":
                if motors == "odin":
                    self.odin.set_pos((self.outside_position + self.inside_position)/2.0 )
                    while (self.odin.is_busy() == True):
                        pass
                elif motors == "zeus":          
                    self.zeus.set_pos((self.outside_position + self.inside_position)/2.0 )
                    while (self.zeus.is_busy() == True):
                           pass

            else:
                if motors == "odin":
                    self.odin.set_pos(location)
                    while (self.odin.is_busy() == True):
                        pass
                elif motors == "zeus":
                    self.zeus.set_pos(location)
                    while (self.zeus.is_busy() == True):
                           pass
        self.odin.set_vel_limit(100000)
        self.zeus.set_vel_limit(100000)