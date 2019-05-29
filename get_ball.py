import ODrive_Ease_Lib
import motor_setup
import Adafruit_Ease_Lib_Sand_Table
from time import sleep

motors = motor_setup.motor_setup()
sleep(1)
motors.prepare_table()

done = False
while not done:
    r = int(input('where is the ball(-5000, -200000): '))
    motors.set_radius(r)
    response = input('are you done y/n :')
    if response == 'y':
        done = True
    

