import Adafruit_Ease_Lib

leds = Adafruit_PCA9685.PCA9684()

red_port = 0
green_port = 1
blue_port = 2

def set_color(red_percent, green_percent, blue_percent):
    leds.change_percentage(red_port, red_percent)
    leds.change_percentage(green_port, green_percent)
    leds.change_percentage(blue_port, blue_percent)