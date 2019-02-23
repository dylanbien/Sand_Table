#///////////////////////////////////////////////////////
#//                   Imports                        //
#//////////////////////////////////////////////////////

#ODrive
import odrive
from RPi_ODrive import ODrive_Ease_Lib



#///////////////////////////////////////////////////////
#//             Global Variables                      //
#//////////////////////////////////////////////////////

#ODrive
radius_SN = 2345654345
theta_SN = 42534654756874563452

#Straight Line
increments = 5.0

#///////////////////////////////////////////////////////
#//               Motor Set-up                        //
#//////////////////////////////////////////////////////


#Finds and names all the motors

od1 = odrive.find_any("usb:001:036")
    if od1.serial_number == radius_SN:
        found = "radius"
        blue_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis0)
        orange_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis1)
    else:
        found = "theta"
        theta_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis0)
        
od2 = odrive.find_any("usb:001:036")

    if found == "radius":
        theta_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis0) 
    else:
        blue_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis0)
        orange_motor = ODrive_Ease_Lib.ODrive_Axis(radius.axis1)
        
#Calibrates Motors
        
blue_motor.calibrate()
orange_motor.calibrate()       
theta_motor.calibrate()

#home/calubrate radii motors

blue_motor.home_with_vel(20000)
orange_motor.home_with_vel(20000)

blue_motor.home_with_vel(-20000)
blue_motor.set_pos(-5000)

orange_motor.home_with_vel(-20000)
orange_motor.set_pos(-5000)

#///////////////////////////////////////////////////////
#//            Straight line Calculations             //
#//////////////////////////////////////////////////////

#///////////////////////////////////////////////////////
#//                   Graphing                        //
#//////////////////////////////////////////////////////
