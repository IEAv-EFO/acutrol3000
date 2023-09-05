import pyvisa
import time

rm = pyvisa.ResourceManager()
inst = rm.open_resource('GPIB1::1::INSTR')

def status():
    """ Function to read position, rate, and acceleration of the rotary table. """
    pos = float(inst.query(":read:pos? 1"))
    # time.sleep(0.25)
    rate = float(inst.query(":read:rate? 1"))
    # time.sleep(0.25)
    acc = float(inst.query(":read:acc? 1"))
    # time.sleep(0.25)
    return {'pos':pos, 'rate':rate, 'acc':acc}
        
def initialize():
    """Initialize in rate mode."""
    inst.write(":Interlock:Reset")
    time.sleep(0.25)
    inst.write(":mode:off 1")
    time.sleep(0.25)
    inst.write(":int:close 1")
    time.sleep(0.25)
    inst.write(":dem:rate 1,0")
    time.sleep(0.25)
    inst.write(":mode:rate 1")
    time.sleep(0.25)

def terminate():
    """Stop movement and open interlock."""
    inst.write(":dem:rate 1,0")
    time.sleep(0.5)
    inst.write(":int:open 1")
    time.sleep(0.5)

def stop():
    inst.write(":dem:rate 1,0")
    time.sleep(0.2)

# absolute factory limits of the rotary table
def limits():
    print("Absolute limits:")
    print(inst.query(":limit:absolute? 1")) # rate, acc, jerk, pos_lo, pos_hi, vtrip

    print("Current limits:")
    # each mode has its limit
    print("acceleration pos mode:", inst.query(":limit:acc? pos,1")) 
    print("acceleration rate mode:", inst.query(":limit:acc? rate,1")) 
    
    print("rate pos mode:", inst.query(":limit:rate? pos,1")) 
    print("rate rate mode:", inst.query(":limit:rate? rate,1"))     


def set_limits(lim_acc, lim_rate=1000):
    inst.write(f":lim:acc pos,1,{lim_acc}")
    inst.write(f":lim:acc rate,1,{lim_acc}")
    inst.write(f":lim:rate pos,1,{lim_rate}")
    inst.write(f":lim:rate rate,1,{lim_rate}")
    
set_limits(4200)
limits()


# Routine implementation
initial_status = status()
initialize()

i_last = 50
rate = 1000
dt = 1 # longer is this delay, smaller is the position error
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