from acutrol3000 import *


set_limits(4200,1000)
limits()


# Routine implementation
initial_status = status()
initialize()

i_last = 5
rate = 500
dt = 0.4 # longer is this delay, smaller is the position error
pos_initial = initial_status["pos"]
time_initial = time.time()
for i in range(i_last):
    
    send_rate(rate)    
    time.sleep(dt)
    print(status())
    stop()
    actual_status = status()
    time.time()-time_initial
    
    send_rate(-rate)
    time.sleep(dt)
    print(status())
    stop()
    actual_status = status()
    print(f"running...{i+1}/{i_last}")

inst.write(":dem:rate 1,0")


terminate()

pos_final = actual_status["pos"]
pos_error = pos_final - pos_initial
print(f"Final position Error: {pos_error}")