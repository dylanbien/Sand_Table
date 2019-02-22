import odrive
from RPi_ODrive import ODrive_Ease_Lib

radius = odrive.find_any()

print("found odrive: " + str(radius.serial_number))

motor1 = ODrive_Ease_Lib.ODrive_Axis(radius.axis0)
#o_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis1)

motor1.calibrate()
#o_motor.calibrate()

#o_motor.set_curr_limit(15)
motor1.set_vel_gain(.0001)
motor1.get_vel_gain()

#o_motor.set_vel(20000)


#o_motor.home_with_vel(20000)

