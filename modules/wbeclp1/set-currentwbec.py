#!/usr/bin/python3
# this script is called from runs/set-current.sh

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import sys

SERVER_HOST = str(sys.argv[1])
SERVER_PORT = int(sys.argv[2])
SET_CURRENT = int(sys.argv[3]) * 10
UNIT_ID = int(sys.argv[4])

client = ModbusTcpClient(SERVER_HOST, SERVER_PORT)

resp = client.write_register(261, SET_CURRENT, unit=UNIT_ID)
if isinstance(resp, ModbusIOException):
    resp = client.write_register(261, SET_CURRENT, unit=UNIT_ID)
    if isinstance(resp, ModbusIOException):
        if UNIT_ID == 1:
            sys.exit("SetCurrentLP1: Modbus IO Error")
        if UNIT_ID == 2:
            sys.exit("SetCurrentLP2: Modbus IO Error")
