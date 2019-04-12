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


#///////////////////////////////////////////////////////
#//               Straight Line Function              //
#///////////////////////////////////////////////////////
    def make_shape(self,direction, sides):

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
