#!/usr/bin/env python3
import sys
from pymodbus.client import ModbusSerialClient

seradd = str(sys.argv[1])
modbusid = int(sys.argv[2])
readreg = int(sys.argv[3])
reganzahl = int(sys.argv[4])

client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)
request = client.read_holding_registers(readreg, reganzahl, slave=modbusid)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
    print(result[0])
