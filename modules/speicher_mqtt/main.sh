#!/bin/bash
#all handled in loadvars.sh & mqttsub.py
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)

openwbModulePublishState "BAT" 0 "Kein Fehler"


# Per MQTT zu schreiben:
# openWB/set/houseBattery/W Speicherleistung in Watt, int, positiv Ladung, negativ Entladung
# openWB/set/houseBattery/WhImported Geladene Energie in Wh, float, nur positiv
# openWB/set/houseBattery/WhExported Entladene Energie in Wh, float, nur positiv
# openWB/set/houseBattery/%Soc Ladestand des Speichers, int, 0-100 
