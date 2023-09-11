from acutrol3000 import *
import time
import os

directory = "data"
file = "rate_collection_1.csv"

if not os.path.exists(directory):
    os.makedirs(directory)


n = 1000
loop_time_sum = 0
time_initial = time.time()
for i in range(0,n):
    init_loop_time = time.time()

    # save data
    rate = read_rate()
    
    with open(f"{directory}/{file}", 'a') as text_file:
        text_file.write(f"{rate}\n")

    loop_time = time.time() - init_loop_time    
    loop_time_sum = loop_time_sum + loop_time
    
text_file.close()
mean_loop_time = loop_time_sum/n
final_time = time.time() - time_initial


print("Number of requests:",n)
print("Mean loop time: ",mean_loop_time)
print("total time: ",final_time)