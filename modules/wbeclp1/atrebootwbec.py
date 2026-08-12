#!/usr/bin/python3
# this script is called from runs/atreboot.sh

from pymodbus.client.sync import ModbusTcpClient
import sys

SERVER_HOST = str(sys.argv[1])
SERVER_PORT = int(sys.argv[2])
UNIT_ID = int(sys.argv[3])

client = ModbusTcpClient(SERVER_HOST, SERVER_PORT)

# Register 257: ModBus-Master WatchDog Timeout in ms
# Register 258: Standby Function Control (0 = enabled; 4 = disabled); active about 13 minutes after Ev is unplugged
# ACHTUNG: wenn Standby deaktiviert ist wird auch der aktuelle Zählerstand nicht in EEPROM
# geschrieben und geht damit bei Spannungsausfall verloren.
# Andererseits hat ein extrem häufiger Wechsel in den Standby einen hohen Verschleiß des EEPROM zur Folge.
# Standby bleibt disabled bis eine brauchbare Lösung zum automatischen Aufwecken der WBEC vorhanden ist.
# Register 262: Offline Current Control im 0.1 A
resp = client.read_input_registers(5, 14, unit=UNIT_ID)
resp = client.read_holding_registers(257, 6, unit=UNIT_ID)
resp = client.write_register(257, 60000, unit=UNIT_ID)
resp = client.write_register(258, 4, unit=UNIT_ID)
resp = client.write_register(262, 110, unit=UNIT_ID)
