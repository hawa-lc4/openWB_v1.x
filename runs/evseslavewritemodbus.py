#!/usr/bin/python3
import sys
from pymodbus.client import ModbusTcpClient

lla = int(sys.argv[1])

client = ModbusTcpClient('192.168.193.16', port=8899)
rq = client.write_registers(1000, lla, slave=1)
