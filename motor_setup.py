import odrive
from RPi_ODrive import ODrive_Ease_Lib

radius = odrive.find_any()

print("found odrive: " + str(radius.serial_number))

motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis0)
#o_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis1)

motor.calibrate()

motor.home_with_vel(20000)

