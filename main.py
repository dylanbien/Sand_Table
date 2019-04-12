import ODrive_Ease_Lib
import motor_setup
import Adafruit_Ease_Lib_Sand_Table


leds = Adafruit_Ease_Lib_Sand_Table.Adafruit_Ease_Lib()
leds = Adafruit_Ease_Lib() 
leds.change_frequency(2000)

motors = motor_setup.motor_setup()

