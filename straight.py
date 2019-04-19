import ODrive_Ease_Lib
from time import time
import odrive
print (time())
od = odrive.find_any()
ax0 = ODrive_Ease_Lib.ODrive_Axis(od.axis0)
print('connected')
time.sleep(2)
ax0.calibrate()
print('calirated')
time.sleep(2)
ax0.home_with_vel(-20000)
time.sleep(2)
ax0.set_pos(-100000)
def move_slowly(start, finish, seconds, dt = 0.005):
    
    distance = finish - start
    velocity = distance / seconds
    time.sleep(2)
    piece_length = velocity * dt
    num_pieces = int(distance / (piece_length) )
    
    mark = time.time()
    
    target_pos = start
    ax0.set_pos(target_pos)

    for x in range (0, num_pieces):
        ax0.set_pos_no_loop(target_pos)
        target_pos += piece_length
        
        print = (time.time() - mark)
        
        while time.time() < mark + dt:
            pass
        
        mark = time.time()
    
    
    
    