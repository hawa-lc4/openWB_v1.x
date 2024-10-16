#!/usr/bin/python3
#from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import sys

SERVER_HOST = str(sys.argv[1])
SERVER_PORT = int(sys.argv[2])
unit_id = 1

#client = ModbusTcpClient(SERVER_HOST, SERVER_PORT, framer=ModbusRtuFramer)
client = ModbusTcpClient(SERVER_HOST, SERVER_PORT)

resp = client.read_input_registers(5, 14, unit=unit_id)
#logFile = open('/home/pi/PyRead.txt', 'a')
#print(resp, file=logFile)
#logFile.close()

if isinstance(resp, ModbusIOException):
        sys.exit("ReadLP: Modbus IO Error")

else:
# charge & plug state
        print(resp.registers[0])
# current
        print(resp.registers[1] / 10)
        print(resp.registers[2] / 10)
        print(resp.registers[3] / 10)
# PCB temperature
#       print(resp.registers[4] / 10)
# voltages
        print(resp.registers[5])
        print(resp.registers[6])
        print(resp.registers[7])
# extern lock state
#       print(resp.registers[8])
# power
        print(resp.registers[9])
# energy since power on
#       print(((resp.registers[10] * 65536) + resp.registers[11]) / 1000)
# energy total
        print(((resp.registers[12] * 65536) + resp.registers[13]) / 1000)
