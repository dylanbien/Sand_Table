import ODrive_Ease_Lib
import motor_setup
import Adafruit_Ease_Lib_Sand_Table
from time import sleep
from threading import Thread

leds = Adafruit_Ease_Lib_Sand_Table.Adafruit_Ease_Lib()
leds.change_frequency(2000)

t = Thread(target = leds.run_lights)
t.start()



motors = motor_setup.motor_setup()
sleep(1)
motors.prepare_table()

def set_one():
    print('1')
    motors.spiral('in')
    motors.flower(-80000,9)
    motors.flower(-80000,3)
    motors.flower(-80000,11)
    motors.sinusoidal(-70000,'constant')
    sleep(motors.theta_period+1)
    
def set_two():
    print('2')
    motors.make_shape('inward',3)
    motors.flower(-80000,9)
    motors.flower(-80000,3)
    motors.flower(-80000,11)
    motors.sinusoidal(-70000,'constant')
    sleep(motors.theta_period+1)

def set_three():
    print('3')
    motors.make_shape('inward',6)
    motors.flower(-80000,9)
    motors.flower(-80000,3)
    motors.flower(-80000,11)
    motors.sinusoidal(-70000,'constant')
    sleep(motors.theta_period+1)

def set_four():
    print('4')
    motors.make_shape('inward',8)
    motors.flower(-80000,9)
    motors.flower(-80000,3)
    motors.flower(-80000,11)
    motors.sinusoidal(-70000,'constant')
    sleep(motors.theta_period+1)
    
def set_five():
    print('5')
    motors.make_shape('inward',5)
    motors.sinusoidal(-80000,'constant')
    motors.flower(-80000,3)
    sleep(motors.theta_period+1)
    motors.flower(-80000,11)
    motors.sinusoidal(-70000,'constant')
    sleep(motors.theta_period+1)
    
while True:
    print('start')
    set_one()
    set_two()
    set_three()
    set_four()
    set_five()
    print('done')
    motors.spiral('in')



