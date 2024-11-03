#!/bin/bash
if [[ $evseconlp6 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 6 $chargep6ip
else
	sudo /home/pi/openwb1-venv/bin/python /var/www/html/openWB/modules/mpm3pmlllp6/readmpm3pm.py $mpmlp6ip $mpmlp6id
fi
