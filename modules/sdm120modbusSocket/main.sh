#!/bin/bash

if [[ $sdm120modbussocketid != "none" ]]; then
	sudo /home/pi/openwb1-venv/bin/python /var/www/html/openWB/modules/sdm120modbusSocket/readsdm.py $sdm120modbussocketsource $sdm120modbussocketid
fi
