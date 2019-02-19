#testing: To Do:
#1) set speeds for both r and theta that you will keep
#2) Find the speed (steps/second) for the theta
#3) find the speed (steps/second) for the radius
#4) find the relationship between velocity and radius's speed (steps per second). **this is more math for bottom of move in straight line function
#5) identify time the motor has to make its increment and solve for velocity



import numpy as np

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def make_shape(sides, outward):
    
    #theta information
    period = 32 #seconds
    steps_per_period = 300000 
    theta_speed = steps_per_period / period
    theta_speed_velocity_relationship = theta_speed / theta_motor.get_vel()
    
   
    #angle informaton
    angle_change = 360 / sides #used in move in straight line call
    increments = 5.0 #angle change between each x,y point
    number_of_increments = angle_change / increments #the number of x,y points used the move in straight line
    
    
    #radius information
    radius_time = (period / 360) * increments
    radius_speed_velocity_relationship = 400 #work on
    if outward:
        r_change = 0
    else:
        r_change = 0

    for count in range (0, sides):
        move_in_straight_line(motor.get_pos(), i * angle_change, r_change)
    
    
def move_in_straight_line (self, starting_r, starting_theta, r_change): 
    global increments 
    
    #gets the starting and ending polar cordinates
    starting_polar = [starting_r, starting_theta]
    ending_polar = [starting_polar[0] + r_change, starting_polar[1] + angle_change ]

    #transfers the above to cartesian
    starting_x, starting_y = pol2cart(starting_polar[0], starting_polar[1])
    ending_x, ending_y = pol2cart(ending_polar[0], ending_polar[1])

    #use these two points to make a line: y = mx + b
    slope = (ending_y - starting_y) / (ending_x - starting_x) #m
    y_intercept = ending_y - (slope * ending_x) #b
    
    
    angles = []
    radii = []
    for ang in range(starting_polar[1], ending_polar[1] + increments , increments):
        
        angles.append(ang)
        radii.append( y_intercept / (sin(ang) - (slope * cos (ang) ) ) ) #note: may need to change angles from theta to radians?
        
    print(angles)
    print(radii)
    
    radius_change = []    
    a = 0
    b = 1
    
    for i in range(number_of_increments):
        radius_change.append(radii[b] - radii[a])
        a += 1
        b += 1
    print (radius_change)


    velocities = []

    for distance in radius_change:
        speed = distance / radius_time #steps per second
        velocities.append(speed * radius_speed_velocity_relationship  ) 
        
