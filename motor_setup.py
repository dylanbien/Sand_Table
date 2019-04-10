import time
import odrive
import usb.core

from RPi_ODrive import ODrive_Ease_Lib

#ODrive
radius_SN = 35601883739976
theta_SN = 62161990005815

dev = usb.core.find(find_all=1, idVendor=0x1209, idProduct=0x0d32)
od = []
try:
    while True:
         a = next(dev)
         od.append(odrive.find_any('usb:%s:%s' % (a.bus, a.address)))
    print('added')
except:
    pass
print(len(od))

for odrives in od:
    print(odrives.serial_number)
    if odrives.serial_number == radius_SN:
        print ("connecting radius")
        radius_odrive = odrives 
        blue_motor = ODrive_Ease_Lib.ODrive_Axis(radius_odrive.axis0)
        orange_motor = ODrive_Ease_Lib.ODrive_Axis(radius_odrive.axis1)
    elif odrives.serial_number == theta_SN:
        theta_odrive = odrives
        print("connecting theta")
        theta_motor = ODrive_Ease_Lib.ODrive_Axis(theta_odrive.axis0)
