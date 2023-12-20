from pymodbus.client import ModbusTcpClient
from constant import Register
import time

client = ModbusTcpClient("192.168.15.1")
client.connect()

register = Register()

pathR = [50, 27, 30, 33, 60, 77]
pathL = [12, 17, 0, 47, 55, 63]

frame_time = 3
force_value_delta = 1 / 20

for frame in range(frame_time * len(pathR)):
    idx = frame // frame_time
    for _ in range(int(1 / force_value_delta)):
        r_value = client.read_holding_registers(register.r_rub).registers[0]
        l_value = client.read_holding_registers(register.l_rub).registers[0]
        idx = frame // frame_time
        if l_value != pathL[idx]:
            client.write_registers(register.l_rub, pathL[idx])
        if r_value != pathR[idx]:
            client.write_registers(register.r_rub, pathR[idx])
        time.sleep(force_value_delta)