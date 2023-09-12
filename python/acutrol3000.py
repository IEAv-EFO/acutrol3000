import pyvisa
import time

rm = pyvisa.ResourceManager()
inst = rm.open_resource('GPIB1::1::INSTR')
print(inst.query("*idn?"))

delay_time = 0.2

def status():
    """ Function to read position, rate, and acceleration of the rotary table."""
    # single command is faster then multiple communication handshakes
    # but it is failing when requested multiple times
    data = inst.query(":read:pos? 1;rate? 1;acc? 1")
    data = data.split(";")
    pos = float(data[0])
    rate = float(data[1])
    acc = float(data[2])
    
    return {'pos':pos, 'rate':rate, 'acc':acc}


def read_pos():        
    pos = float(inst.query(":read:pos? 1"))
    return pos

def read_rate():
    inst.write(":read:rate? 1")
    time.sleep(0.001)
    rate = float(inst.read())
    return rate

def read_acc():        
    acc = float(inst.query(":read:acc? 1"))
    return acc



def check_error():
    """Function to check if interlock is throwing error."""
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
    time.sleep(delay_time)
    inst.write(":mode:off 1")
    time.sleep(delay_time)
    inst.write(":int:close 1")
    time.sleep(delay_time)
    stop()



def terminate():
    """Stop movement and open interlock."""
    stop()
    inst.write(":int:open 1")
    time.sleep(delay_time)



def stop():
    """Stops movement by setting rate equal 0."""
    send_oscillation(0,0)
    time.sleep(delay_time)
    inst.write(":mode:rate 1")
    time.sleep(delay_time)
    inst.write(":dem:rate 1,0")
    time.sleep(delay_time)



def limits():
    """Show current limit values."""
    print("Absolute factory limits:")
    print("rate, acc, jerk, pos_lo, pos_hi, vtrip")
    print(inst.query(":limit:absolute? 1")) 
    print("Current limits:")
    # each mode has its limit
    print("acceleration pos mode:", float(inst.query(":limit:acc? pos,1")),"deg/s/s")
    print("acceleration rate mode:", float(inst.query(":limit:acc? rate,1")),"deg/s/s")
    print("acceleration synthesis mode:", float(inst.query(":limit:acc? synt,1")),"deg/s/s")
    print("rate pos mode:", float(inst.query(":limit:rate? pos,1")),"deg/s")
    print("rate rate mode:", float(inst.query(":limit:rate? rate,1")),"deg/s")    
    print("rate synthesis mode:", float(inst.query(":limit:rate? synt,1")),"deg/s")    



def set_limits(lim_acc=8300, lim_rate=1000):
    """
    Set acceleration and rate limits.
    - Necessary to adjust the rate when using the position command.
    """
    inst.write(f":lim:acc pos,1,{lim_acc}")
    inst.write(f":lim:acc rate,1,{lim_acc}")
    inst.write(f":lim:acc synt,1,{lim_acc}")
    inst.write(f":lim:rate pos,1,{lim_rate}")
    inst.write(f":lim:rate rate,1,{lim_rate}")
    inst.write(f":lim:rate synt,1,{lim_rate}")



def send_rate(rate):
    if check_error() == 1:
        initialize()
        time.sleed(delay_time)
    else:
        inst.write(":int:close 1")
        time.sleed(delay_time)

    if inst.query(":mode? 1") == "Rate\n":
        inst.write(f":dem:rate 1,{rate}")
        time.sleed(delay_time)
    else:
        inst.write(":mode 1,rate")
        time.sleed(delay_time)
        inst.write(f":dem:rate 1,{rate}")
        time.sleed(delay_time)
        


def wait_stop(delay=0.5, count_lim=500):
    """Wait until stopped to send next command."""
    count = 1
    while abs(status()["rate"]) > 0.01 and count < count_lim:
        time.sleep(delay)
        print("waiting...")
        count = count + 1
    print("stopped!")


# TODO: can I make a complete turn with position command?
def send_position(pos):
    if check_error() == 1:
        initialize()
    inst.write(":int:close 1")

    if inst.query(":mode? 1") == "Position\n":
        inst.write(f":dem:pos 1,{pos}")
    else:
        inst.write(":mode 1,pos")
        inst.write(f":dem:pos 1,{pos}")
        


def send_delta_position(delta_pos):
    """Limited to 180 deg increment"""
    if check_error() == 1:
        initialize()

    inst.write(":int:close 1")
    time.sleep(delay_time)

    if inst.query(":mode? 1") == "Position\n":
        inst.write(f":dem:delta 1,{delta_pos}")
        time.sleep(delay_time)

    else:
        inst.write(":mode 1,pos")    
        time.sleep(delay_time)
        inst.write(f":dem:delta 1,{delta_pos}")
        time.sleep(delay_time)
        


def set_oscillation(amp_slew=2.0000, freq_slew=0.1000):
    # TODO: Command not working, don't know why
    inst.write(f":con:osc 1,Enable,{amp_slew},{freq_slew},Pos,Lin")
    time.sleep(delay_time)
    print(inst.query(":con:osc? 1"))
    time.sleep(delay_time)



def send_oscillation(amp, freq, phase=0):
    """
    amp = pos/rate/acc... max pos=155 reaches 960 deg/s
    linear frequency slew means Hz/s
    """
    inst.write(":mode:synt 1")
    time.sleep(delay_time)
    inst.write(f":dem:osc 1,{amp},{freq},{phase}")
    time.sleep(delay_time)
