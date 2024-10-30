#!/usr/bin/python3
#from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import sys

SERVER_HOST = str(sys.argv[1])
SERVER_PORT = int(sys.argv[2])
SET_CURRENT = int(sys.argv[3]) * 10
unit_id = 1

#client = ModbusTcpClient(SERVER_HOST, SERVER_PORT, framer=ModbusRtuFramer)
client = ModbusTcpClient(SERVER_HOST, SERVER_PORT)

resp = client.write_register(261, SET_CURRENT, unit=unit_id)
if isinstance(resp, ModbusIOException):
    resp = client.write_register(261, SET_CURRENT, unit=unit_id)
    if isinstance(resp, ModbusIOException):
        sys.exit("SetCurrent: Modbus IO Error")

#logFile = open('/home/pi/PySetCurr.txt', 'a')
#print(resp, file=logFile)
#logFile.close()
