#!/usr/bin/env python3
import fileinput
import logging
import re
import subprocess
import sys
import threading
import time
from json import loads as json_loads
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Callable, Any, Union, Iterable, Pattern

import paho.mqtt.client as mqtt

from modules.common.store.ramdisk import files

inaction = 0
openwb_conf_file = "/var/www/html/openWB/openwb.conf"
lock = threading.Lock()
RAMDISK_PATH = Path(__file__).resolve().parents[1] / "ramdisk"

logging.basicConfig(filename=str(RAMDISK_PATH / "mqtt.log"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
log = logging.getLogger("MQTT")


def get_config_value(key):
    with fileinput.input(openwb_conf_file) as file:
        for line in file:
            if line.startswith(str(key+"=")):
                return line.split("=", 1)[1]
        return


def get_serial():
    # Extract serial from cpuinfo file
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line[11:27]
        return "0000000000000002"


mqtt_broker_ip = "localhost"
client = mqtt.Client("openWB-mqttsubB2-" + get_serial())
medianInterval = 7
medianCountB2 = 1
medianPowerB2 = 0
medianSocB2 = 0
evuWatt = 0
battWatt = 0
newPwrB2 = 0
B2_id1 = get_config_value("speicher_hoymiles_id1").strip()
B2_top1s = "homeassistant/sensor/" + B2_id1 + "/quick/state"
B2_top1p = "homeassistant/number/" + B2_id1 + "/power_ctrl/set"


# connect to broker and subscribe to set topics
def on_connect(client: mqtt.Client, userdata, flags: dict, rc: int):
    log.info("B2 Connected")
    client.subscribe(B2_top1s, 2)
    client.subscribe("openWB/evu/W", 2)
    client.subscribe("openWB/housebattery/W1", 2)


# handle each quick/state topic
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    if (len(msg.payload.decode("utf-8")) >= 1):
        lock.acquire()
        global medianCountB2
        global medianPowerB2
        global medianSocB2
        global medianInterval
        global evuWatt
        global battWatt
        global newPwrB2

        try:
            # setTopicCleared = False
            # log all messages before any error forces this process to die
            # but not flooding mqtt.log with messages from HiBattery every second
            if (msg.topic != B2_top1s):
                log.debug("Topic-B2: %s, Message: %s", msg.topic, msg.payload.decode("utf-8"))

            if (msg.topic == "openWB/evu/W"):
                evuWatt = int(msg.payload.decode("utf-8"))

            if (msg.topic == "openWB/housebattery/W1"):
                battWatt = int(msg.payload.decode("utf-8"))

            if (msg.topic == B2_top1s):
                payload = msg.payload.decode("utf-8")
                json_payload = json_loads(str(payload))
                if medianCountB2 < medianInterval:
                    medianPowerB2 = medianPowerB2 + int(json_payload['sys_plug_p'])
                    medianSocB2 = medianSocB2 + int(json_payload['sys_soc'])
                    medianCountB2 += 1
                else:
                    medianPowerB2 = medianPowerB2 + int(json_payload['sys_plug_p'])
                    medianSocB2 = medianSocB2 + int(json_payload['sys_soc'])
                    medianPowerB2 = int(medianPowerB2 / -medianInterval)
                    f = open('/var/www/html/openWB/ramdisk/speicherleistung2', 'w')
                    f.write(str(medianPowerB2))
                    f.close()
                    medianSocB2 = int(medianSocB2 / medianInterval)
                    f = open('/var/www/html/openWB/ramdisk/speichersoc2', 'w')
                    f.write(str(medianSocB2))
                    f.close()
                    medianCountB2 = 1
                    medianPowerB2 = 0
                    medianSocB2 = 0
                    if (battWatt >= 0 and battWatt < 250):
                        if ((evuWatt + newPwrB2) < -250):
                            newPwrB2 = int((evuWatt + newPwrB2) / 2)
                        else:
                            newPwrB2 = 0
                    elif (battWatt >= 250 and evuWatt < 250):
                        newPwrB2=int(battWatt * -0.25)
                    elif (battWatt <= -250):
                        newPwrB2=int(battWatt * -0.145)
                    else:
                        newPwrB2 = 0
                    client.publish(str(B2_top1p), str(newPwrB2), qos=0, retain=True)

            # clear all set topics if not already done
            # if not setTopicCleared:
            #     client.publish(msg.topic, "", qos=2, retain=True)
        except Exception:
            log.exception("Error handling MQTT-Message")
        finally:
            lock.release()


client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
