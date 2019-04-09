import Adafruit_Ease_Lib

leds = Adafruit_Ease_Lib.Adafruit_Ease_Lib() 
leds.change_frequency(2000)
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
    global current_color
    next_color = [red_percent, green_percent, blue_percent]
    change = []
    print(next_color)
    print(current_color)
    for i in range (3):
        if (next_color[i] - current_color[i] > 0):
            change.append(.1)
        elif (next_color[i] - current_color[i] < 0):
            change.append(-.1)
        else:
            change.append(0)
    print(change)
    red_done = False
    green_done = False
    blue_done = False

    while (red_done == False or green_done == False or blue_done == False):

        if (red_done == False):
            current_color[0] += change[0]
            leds.change_percentage(red_port, current_color[0])
            if (int(current_color[0]) == int(next_color[0])):
                red_done =  True
                print('red done')

        if (green_done == False):
            current_color[1] += change[1]
            leds.change_percentage(green_port, current_color[1])
            if (int(current_color[1])== int(next_color[1] )):
                green_done = True
                print('green done')

        if (blue_done == False):
            current_color[2] += change[2]
            leds.change_percentage(blue_port, current_color[2])
            if (int(current_color[2]) == int(next_color[2] )):
                blue_done = True
                print('blue done')
    set_color(red_percent, green_percent, blue_percent)