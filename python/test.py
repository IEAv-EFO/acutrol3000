from acutrol3000 import *
import time

n = 10
loop_time_sum = 0
time_initial = time.time()
for i in range(0,n):
    init_loop_time = time.time()

    # logic to test time
    # status()
    # read_pos()
    inst.query(":r:va? 1082")

    
    loop_time = time.time() - init_loop_time    
    loop_time_sum = loop_time_sum + loop_time
    
mean_loop_time = loop_time_sum/n
final_time = time.time() - time_initial


print("Number of requests:",n)
print("Mean loop time: ",mean_loop_time)
print("total time: ",final_time)