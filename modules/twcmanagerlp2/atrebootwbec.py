#!/usr/bin/python3
#from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusTcpClient
import sys

SERVER_HOST = str(sys.argv[1])
SERVER_PORT = int(sys.argv[2])
unit_id = 1

#client = ModbusTcpClient(SERVER_HOST, SERVER_PORT, framer=ModbusRtuFramer)
client = ModbusTcpClient(SERVER_HOST, SERVER_PORT)

resp = client.read_input_registers(5, 14, unit=unit_id)
resp = client.read_holding_registers(257, 6, unit=unit_id)
resp = client.write_register(257, 60000, unit=unit_id)
resp = client.write_register(258, 0, unit=unit_id)
resp = client.write_register(262, 110, unit=unit_id)
