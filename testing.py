import numpy as np
import matplotlib.pyplot as plt

angle_change = None
increments = 5
number_of_increments = None


# theta information
period = 32  # seconds
degrees_per_sec =  360.0 / period

radius_time = degrees_per_sec * increments

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    #print(rho)
    #print(phi)
    return(int(rho), int(phi))

def pol2cart(rho, phi):
    x = rho * np.cos(np.deg2rad(phi))
    y = rho * np.sin(np.deg2rad(phi))
    #print(x)
    #print(y)
    return(int(x), int(y))

def make_shape(sides, outward):
    global angle_change
    global increments
    global number_of_increments

    
   
    #angle informaton
    angle_change = 360 / sides #used in move in straight line call
    number_of_increments = angle_change / increments #the number of x,y points used the move in straight line
    
    
    #radius information
    radius_time = (period / 360) * increments
    if outward:
        r_change = -5
    else:
        r_change = -15

    start = 200
    for i in range(30):
        for count in range(0, sides):
            start = start + r_change
            if (start < 0):
                print('start below zero')
                return
            move_in_straight_line(start, int(count * angle_change), r_change)
    
    
def move_in_straight_line(starting_r, starting_theta, r_change):
    global increments 
    global angle_change
    global number_of_increments
    global radius_time
    global radius_speed_velocity_relationship
    #gets the starting and ending polar cordinates
    starting_polar = [starting_r, int(starting_theta)]
    ending_polar = [starting_polar[0] + r_change, int(starting_polar[1] + angle_change) ]

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
        radii.append(int( y_intercept / (np.sin(np.deg2rad(ang)) - (slope * np.cos(np.deg2rad(ang)) ) ) )) #note: may need to change angles from theta to radians?
        plt.polar(angles[len(angles)-1]*(np.pi/180), radii[len(angles)-1],'k.')

    print(angles)
    print(radii)


    radius_change = []    
    a = 0
    b = 1
    
    for i in range(int(number_of_increments)):
        radius_change.append(radii[b] - radii[a])
        a += 1
        b += 1
    print(radius_change)


    velocities = []

    for distance in radius_change:
        velocities.append (distance / radius_time)

    print(radii)
    print(velocities)

    for i in range(len(radii) -1 ): #1-25
        #print(radii[i + 1])
        #print(velocities[i])
        continue

ax = plt.subplot(111, projection='polar')
make_shape(5, True)
ax.set_rmax(210)
ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)
ax.set_title("Simulated Pattern", va='bottom')
plt.show()