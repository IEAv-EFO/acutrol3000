import pyvisa
import time

rm = pyvisa.ResourceManager()
inst = rm.open_resource('GPIB1::1::INSTR')
print(inst.query("*idn?"))


delay_time = 0

def status():
    """ Function to read position, rate, and acceleration of the rotary table. """
    pos = float(inst.query(":read:pos? 1"))
    # time.sleep(delay_time)
    rate = float(inst.query(":read:rate? 1"))
    # time.sleep(delay_time)
    acc = float(inst.query(":read:acc? 1"))
    # time.sleep(delay_time)
    return {'pos':pos, 'rate':rate, 'acc':acc}
        


def check_error():
    if inst.query(":interlock? 1") == "Fault\n":
        print("Interlock error!")
        return 1
    elif inst.query("*stb?") == "65\n":
        print("Interlock error!")
        return 1
    else:
        return 0



def initialize():
    """Initialize in rate mode."""
    inst.write(":Interlock:Reset")
    # time.sleep(delay_time)
    inst.write(":mode:off 1")
    # time.sleep(delay_time)
    inst.write(":int:close 1")
    # time.sleep(delay_time)
    stop()



def terminate():
    """Stop movement and open interlock."""
    inst.write(":dem:rate 1,0")
    # time.sleep(delay_time)
    inst.write(":int:open 1")
    # time.sleep(delay_time)



def stop():
    inst.write(":mode:rate 1")
    # time.sleep(delay_time)
    inst.write(":dem:rate 1,0")
    # time.sleep(delay_time)



def limits():
    print("Absolute limits:") # absolute factory limits of the rotary table
    print(inst.query(":limit:absolute? 1")) # rate, acc, jerk, pos_lo, pos_hi, vtrip
    print("Current limits:")
    # each mode has its limit
    print("acceleration pos mode:", float(inst.query(":limit:acc? pos,1")),"deg/s/s")
    print("acceleration rate mode:", float(inst.query(":limit:acc? rate,1")),"deg/s/s")
    print("rate pos mode:", float(inst.query(":limit:rate? pos,1")),"deg/s")
    print("rate rate mode:", float(inst.query(":limit:rate? rate,1")),"deg/s")    



def set_limits(lim_acc, lim_rate=1000):
    inst.write(f":lim:acc pos,1,{lim_acc}")
    inst.write(f":lim:acc rate,1,{lim_acc}")
    inst.write(f":lim:rate pos,1,{lim_rate}")
    inst.write(f":lim:rate rate,1,{lim_rate}")



def send_rate(rate):
    if check_error() == 1:
        initialize()
    else:
        inst.write(":int:close 1")

    if inst.query(":mode? 1") == "Rate\n":
        inst.write(f":dem:rate 1,{rate}")
    else:
        inst.write(":mode 1,rate")
        inst.write(f":dem:rate 1,{rate}")
        


def send_position(pos):
    if check_error() == 1:
        initialize()
    else:
        inst.write(":int:close 1")

    if inst.query(":mode? 1") == "Position\n":
        inst.write(f":dem:pos 1,{pos}")
    else:
        inst.write(":mode 1,pos")
        inst.write(f":dem:pos 1,{pos}")
        


def send_delta_position(delta_pos):
    if check_error() == 1:
        initialize()
    else:
        inst.write(":int:close 1")

    if inst.query(":mode? 1") == "Position\n":
        inst.write(f":dem:delta 1,{delta_pos}")
    else:
        inst.write(":mode 1,pos")
        inst.write(f":dem:delta 1,{delta_pos}")
        


set_limits(4200)
limits()


# Routine implementation
initial_status = status()
initialize()

i_last = 10
rate = 1000
dt = 0.1 # longer is this delay, smaller is the position error
pos_initial = initial_status["pos"]
time_initial = time.time()
for i in range(i_last):
    
    inst.write(f":dem:rate 1,{rate}")
    time.sleep(dt)
    print(status())
    stop()
    actual_status = status()
    time.time()-time_initial
    
    inst.write(f":dem:rate 1,-{rate}")
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