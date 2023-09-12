from acutrol3000 import *
import time
import os

directory = "data"
file = "rate_collection_007_1hz_160deg.csv"

if not os.path.exists(directory):
    os.makedirs(directory)  

# define rotation routine
set_limits()
limits()
initialize()
send_oscillation(160,1) # maximum (155,1)
initialize()
send_oscillation(160,1) # maximum (155,1)
n = 0
loop_time_sum = 0
time_initial = time.time()

while True:
    try:
        init_loop_time = time.time()

        # read and save data
        rate = read_rate()
        with open(f"{directory}/{file}", 'a') as text_file:
            text_file.write(f"{rate}\n")

        loop_time = time.time() - init_loop_time    
        loop_time_sum = loop_time_sum + loop_time
        n = n + 1
    except KeyboardInterrupt:
        break

terminate()

text_file.close()
mean_loop_time = loop_time_sum / n
final_time = time.time() - time_initial

print("\nNumber of measurements:", n)
print("Mean loop time: ", mean_loop_time)
print("Total time: ", final_time)