import ODrive_Ease_Lib
import motor_setup
import Adafruit_Ease_Lib_Sand_Table
from time import sleep

#leds = Adafruit_Ease_Lib_Sand_Table.Adafruit_Ease_Lib()

#leds.change_frequency(2200)
#leds.run_lights()
motors = motor_setup.motor_setup()
sleep(1)
motors.prepare_table()


