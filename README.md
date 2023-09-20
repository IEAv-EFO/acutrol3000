# Acutrol3000

Acutronics rotary table BD125 driver development.

The routine can be executed by a local `macro` or on real time by `GPIB` (40 ms minimum) or `ethernet` cable (2 ms minimum).

The main interface is being developed in LabVIEW.

![image](/labview/main_vi.png)

mode: if activated and with loaded demand value, it will move.
- rate 
- position

demand:
- set value for mode to go




One can check https://github.com/robotics/acutrol as reference.