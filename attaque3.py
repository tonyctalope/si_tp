from pymodbus.client import ModbusTcpClient
from constant import Register
import time

register = Register()

client = ModbusTcpClient("192.168.15.1")
client.connect()

while True:
    speed_val = client.read_holding_registers(register.energy_speed).registers[0]
    if speed_val != 100:
        client.write_registers(register.energy_speed, 100)
    time.sleep(0.5)