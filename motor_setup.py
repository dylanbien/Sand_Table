import odrive
from RPi_ODrive import ODrive_Ease_Lib
from time import sleep

radius = odrive.find_any()

print("found odrive: " + str(radius.serial_number))

motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis0)
#o_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis1)
if motor.is_calibrated() == False:
    motor.calibrate()
radius.axis0.controller.config.vel_limit_tolerance = 0
motor.set_vel_limit(30000)
motor.home_with_vel(20000)
motor.home_with_vel(-20000)
i = -20000
motor.set_vel(i)
while motor.get_pos() < 200000:
    
    print(motor.get_vel())
   
    
motor.set_vel(0)