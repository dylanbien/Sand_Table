import Adafruit_Ease_Lib

leds = Adafruit_PCA9685.PCA9684()
leds.set_pwm_frequency(1000)
red_port = 0
green_port = 1
blue_port = 2

current_color = [0, 0, 0]
next_color = [0, 0, 0]

def set_color(red_percent, green_percent, blue_percent):
    global current_color
    leds.change_percentage(red_port, red_percent)
    leds.change_percentage(green_port, green_percent)
    leds.change_percentage(blue_port, blue_percent)
    current_color = [red_percent, green_percent, blue_percent]


def transition_color(red_percent, green_percent, blue_percent):
    global next_color
    next_color = [red_percent, green_percent, blue_percent]
    change = []
    for i in range (3):
        if (next_color[i] - current_color[i] > 0):
            change.append(.5)
        elif (next_color[i] - current_color[i] < 0):
            change.append(-.5)
        else:
            change.append(0)

    red_done = False
    green_done = False
    blue_done = False

    while (red_done == False and green_done == False and blue_done == False):

        if (red_done == False):
            current_color[0] += change[0]
            leds.change_percentage(red_port, current_color[0])
            if (current_color[0] == next_color[0] ):
                red_done == True

        if (green_done == False):
            current_color[1] += change[1]
            leds.change_percentage(green_port, current_color[1])
            if (current_color[1] == next_color[1] ):
                green_done == True

        if (blue_done == False):
            current_color[2] += change[2]
            leds.change_percentage(blue_port, current_color[2])
            if (current_color[2] == next_color[2] ):
                blue_done == True

    set_color(red_percent, green_percent, blue_percent)