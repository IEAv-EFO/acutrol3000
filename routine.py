from acutrol3000 import *

limits()
initialize()

rate = 1000
acc = 4200
set_limits(acc, rate)
send_position(0)
time.sleep(.5)

pos_initial = status()["pos"]
time_initial = time.time()

angle = 179
i_last = 5
for i in range(i_last):
    wait_stop()
    send_delta_position(angle)   
    print(status())
    time.time()-time_initial

    wait_stop()
    send_delta_position(-angle)   
    print(status())
    print(f"running...{i+1}/{i_last}")

wait_stop()
terminate()

pos_final =  status()["pos"]
pos_error = pos_final - pos_initial
print(f"Final position Error: {pos_error}")