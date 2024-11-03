#!/bin/bash
if [[ $evseconlp8 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 8 $chargep8ip
else
	sudo /home/pi/openwb1-venv/bin/python /var/www/html/openWB/modules/mpm3pmlllp8/readmpm3pm.py $mpmlp8ip $mpmlp8id
fi
