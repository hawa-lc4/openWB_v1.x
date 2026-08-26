#!/usr/bin/python3
# this script is called from local main.sh

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import sys

SERVER_HOST = str(sys.argv[1])
SERVER_PORT = int(sys.argv[2])
UNIT_ID = int(sys.argv[3])

client = ModbusTcpClient(SERVER_HOST, SERVER_PORT)

resp = client.read_input_registers(5, 14, unit=UNIT_ID)

if isinstance(resp, ModbusIOException):
	sys.exit("ReadLP2: Modbus IO Error")
else:
# charge & plug state
	print(resp.registers[0])
# this loadpoint is connected with grid phases changed!
# current
	print(resp.registers[3] / 10)
	print(resp.registers[2] / 10)
	print(resp.registers[1] / 10)
# voltages
	print(resp.registers[7])
	print(resp.registers[6])
	print(resp.registers[5])
# power
	print(resp.registers[9])
# energy total
	print(((resp.registers[12] * 65536) + resp.registers[13]) / 1000)
