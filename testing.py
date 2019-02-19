import numpy as nm
period = 100
degrees_per_second = period / 360.0


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def move_in_straight_line (self, sides):

    angle_change = 360 / sides
    incriments = 5.0
    number_of_incriments = angle_change / incriments
    
    global degrees_per_second
    time_per_incriment = degrees_per_second * incriment

    starting_polar = [5, 0]
    ending_polar = [ starting_polar[0], starting_polar[1] + angle_change ]

    starting_x, starting_y = pol2cart(starting_polar[0], starting_polar[1])
    ending_x, ending_y = pol2cart(ending_polar[0], ending_polar[1])

    #use thse two points to make a line: y = mx + b
    
    slope = (ending_y - starting_y) / (ending_x - starting_x) #m
    y_intercept = ending_y - (slope * ending_x) #b
    
    angles = []
    radii = []
    for i in range(starting_polar[1], ending_polar[1] + incriments , incriments):
        
        angles.append(i)
        radii.append( y_intercept / (sin(i) - (slope * cos (i) ) ) )
        
    print(angles)
    print(radii)
    
    radius_change = []    
    a = 0
    b = 1
    
    for l in range(number_of_incriments):
        radius_change.append(radii[b] - radii[a])
        a += 1
        b += 1
        
    print (radius_change)
  
    velocities = []
    
    for j in radius_change:
        velocities.append( j / time_per_incriment )
        
        
    #for l in range (number_of_incriments):
        #motor.set_velocities(velocities[l])
        #motor.go_to_point(radii[l])
        
        
        
        
