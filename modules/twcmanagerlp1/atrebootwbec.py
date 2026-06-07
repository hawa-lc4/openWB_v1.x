#!/usr/bin/python3
# this script is called from runs/atreboot.sh

#from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusTcpClient
import sys

SERVER_HOST = str(sys.argv[1])
SERVER_PORT = int(sys.argv[2])
unit_id = int(sys.argv[3])

#client = ModbusTcpClient(SERVER_HOST, SERVER_PORT, framer=ModbusRtuFramer)
client = ModbusTcpClient(SERVER_HOST, SERVER_PORT)

# Register 257: ModBus-Master WatchDog Timeout in ms
# Register 258: Standby Function Control (0 = enabled; 4 = disabled)
# Register 262: Standby Function Control im 0,1 A
resp = client.read_input_registers(5, 14, unit=unit_id)
resp = client.read_holding_registers(257, 6, unit=unit_id)
resp = client.write_register(257, 60000, unit=unit_id)
resp = client.write_register(258, 0, unit=unit_id)
resp = client.write_register(262, 110, unit=unit_id)
