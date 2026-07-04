# Das Original

finden Sie hier: https://github.com/snaptec/openWB
Weitere Infos unter https://openwb.de
Aktuelle openWB gibt es unter 

	https://openwb.de/shop/



# openWB  Anpassungen zur Version 1.9


Die Software steht frei für jeden zur Verfügung, siehe GPLv3 Bedingungen.


# Haftungsausschluss
Es wird mit Kleinspannung aber auch 230V beim Anschluss der EVSE gearbeitet. 
Dies darf nur geschultes Personal.
Die Anleitung ist ohne Gewähr und jegliches Handeln geschieht auf eigene Gefahr.
Eine Fehlkonfiguration der Software kann möglicherweise auch einen massiven Schaden am Fahrzeug bedeuten!
(Hier ist speziell die Umschaltung der Phasenanzahl 1P3P gemeint)
Falsch zusammengebaute Hardware kann lebensgefährlich sein.
Im Zweifel diesen Part von einem Elektriker durchführen lassen!!
Keine Gewährleistung für die Software - use at your own RISK!


# Wofür?
Steuerung einer EVSE DIN oder anderer Ladepunkte für sofortiges laden, Überwachung der Ladung, PV Überschussladung und Lastmanagement mehrerer WB.
Unterstützt wird jedes EV das den AC Ladestandard unterstützt.

Besonderheit dieser Installation ist die Einbindung der Wallbox Heidelberg Energy Control als eigenes Modul.
Die Kommunikation erfolgt über Modbus-TCP mittels einer ESP32 basierten Modbus-TCP-Bridge (siehe Tasmota) für zwei Wallboxen dieses Typs.



# Installation


Software:

Installiertes Raspbian (Debian) auf einem Raspberry Pi 4B.

Installationsanleitung für Windows: http://openwb.de/main/wp-content/uploads/2019/07/install_openWB_v2.pdf

Raspbian installieren aktuell werden in der Version 1.9 nur Stretch (bevorzugt) und Buster unterstützt.
Diese Variante nutzt Debian 12 (bookworm).
Die entscheidende Anpassung ist das Python3 in der Version 3.11.2 für den Benutzer pi in einem virtuellen environment installiert ist.
In diesem virt. env. werden dann auch alle von openWB benötigten Python Pakete in älteren Versionen installiert.
Die Basis Pakete installiert die "openwb-install.sh"; falls man eigene Pakete zur Verwendung in openWB installieren möchte müssen diese ebenfalls in dieses virtuelle env. installiert werden.
Dieses Vorgehen erfordert dann noch geringe Anpassungen in allen shell-Skripten die python Kommandos aufrufen.
OpenWB 1.9.304 läuft dann grundsätzlich aber ohne weitere Anpassungen in den Python Skripten.

Raspian:

	http://downloads.raspberrypi.org/raspbian_full/images/

Vorausgesetzt wird das ein Benutzer 'pi' mit der Gruppe 'pi' eingerichtet ist.

Als dieser Benutzer anmelden und in der Shell folgendes eingeben:

	cd ~ && curl -s https://raw.githubusercontent.com/hawa-lc4/openWB_v1.x/adapt_RPI-4B/openwb-install.sh > openwb-install.sh
	chmod +x openwb-install.sh && ./openwb-install.sh


Crontab anpassen:

	crontab -e

hier einfügen:

	* * * * * /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 10 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 20 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 30 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 40 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 50 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 


 
Der Raspberry funktioniert zuverlässig mit gutem WLAN. Kabel-Lan ist zu bevorzugen.

Taster am Raspberry zur Einstellung des Lademodi:
(diese Komponente wurde hier nicht angepasst; erfordert also Eigeninitiative wenn sie verwendet werden soll)
Der Lademodi kann nicht nur über die Weboberfläche sondern auch an der openWB direkt eingestellt werden.
Hierzu müssen schließende Taster von GND (Pin 34) nach Gpio X  angeschlossen werden.

	SofortLaden GPIO 12, PIN 32

	Min+PV GPIO 16, PIN 36

	NurPV GPIO 6, Pin 31

	Aus Gpio 13, Pin 33
	

Ebenso ist es möglich die Ladezutände der Wallbox(en) nicht nur durch ein Display oder Web-UI anzuzeigen
sondern auch über LEDs. Dazu die Skripte runs/leds.py bzw. runs/ledss1.py anpassen entsprechend konfigurieren.
(Diese Komponente ist nuch eine Baustelle!)


# Module erstellen

Ist ein Modul für den gewünscht Einsatzzweck noch nicht verfügbar kann man dies selbst erstellen.
Wenn es läuft bitte melden und es (einstellbar) dem Projekt hinzugefügt.

Ein Modul ist immer ein Ordner mit dem Modulnamen im Ordner openWB/modules. Es besteht aus einem Shell script mit dem Namen main.sh. Sollten weitere Dateien benötigt werden liegen diese mit im Ordner. 

Exemplarisch der Aufbau erklärt am bezug_http Modul:


	#!/bin/bash
	# Die eigentliche (in dem Fall http) Abfrage. Die Variable sollte den Modulnamen und im Anschluss den Wert enthalten um sie eindeutig zu identifizieren
	watt_bezug=$(curl --connect-timeout 10 -s $bezug_http_w_url)
	# Prüfung auf Richtigkeit der Variable. Sie darf bei Bezugsmodulen ein - enthalten sowie die Zahlen 0-9
	re='^-?[0-9]+$'
	# Entspricht der abgefragte Wert nicht der Anforderung wird sie auf 0 gesetzt um ein Fehlverhalten der Regelung zu verhindern
	if ! [[ $watt_bezug =~ $re ]] ; then
		watt_bezug="0"
	fi
	# Der Hauptwert (Watt) wird als echo an die Regellogik zurückgegeben
	echo $watt_bezug
	# Zusätzlich wird der Wert in die Ramdisk geschrieben, dies ist für das Webinterface sowie das Logging und ggf. externe Abfragen
	echo $watt_bezug > /var/www/html/openWB/ramdisk/watt_bezug
	# Wird Logging von Zählern genutzt, wird der absolute Zählerstand in Wh benötigt. Ist dieser nicht vorhanden sollte die Variable auf "none" gesetzt werden
	if [[ $bezug_http_ikwh_url != "none" ]]; then
		import_kwh=$(curl --connect-timeout 5 -s $bezug_http_ikwh_url)
		echo $import_kwh > /var/www/html/openWB/ramdisk/bezugkwh
	fi
	# Analog zum bezug dasselbe Verfahren für die Einspeisung
	if [[ $bezug_http_ekwh_url != "none" ]]; then
		export_kwh=$(curl --connect-timeout 5 -s $bezug_http_ekwh_url)
		echo $export_kwh > /var/www/html/openWB/ramdisk/einspeisungkwh
	fi


Bei PV Modulen muss geschrieben werden:

	# Rückgabewert in Watt
	echo $pv_watt
	echo $pv_watt > /var/www/html/openWB/ramdisk/pvwatt
	# ggf wenn verfügbar für logging den Zählerstand in Wh
	echo $pv_wh > /var/www/html/openWB/ramdisk/pvkwh

Beispielhaft das wr_fronius Modul für deren Wechselrichter mit Webinterface:
Fronius bietet eine Json API an. Diese wird hier auf die Werte die gebraucht werden reduziert.


	#!/bin/bash
	# Auslesen eine Fronius Symo WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung
	# Abfrage der kompletten Json Rückgabe
	pv_watt_tmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
	# Das Tool jq verarbeitet die Rückgabe und reduziert sie auf die gewünschte Zeile. sed & tr entfernen ungewollte Klammern, Punkte und \n newline Zeichen um die reine Zahl zu erhalten
	pv_watt=$(echo $pv_watt_tmp | jq '.Body.Data.PAC.Values' | sed 's/.*://' | tr -d '\n' | sed 's/^.\{2\}//' | sed 's/.$//' )
	#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
	#Fronius Wechselrichter gehen nachts in den Standby und antworten dann nicht. Um einen Fehler abzufangen bei leerer Rückgabe wird eine 0 gesetzt
	re='^[0-9]+$'
	if ! [[ $pv_watt =~ $re ]] ; then
	   pv_watt="0"
	fi
	#Rückgabe des Watt Wertes an die Regellogik
	echo $pv_watt
	#zur weiteren Verwendung im Webinterface, zum Logging & zur externen Abfrage
	echo $pv_watt > /var/www/html/openWB/ramdisk/pvwatt
	#Aus dem selben String erhält man ebenso den totalen Zählerstand für das Logging
	#Hier sieht man das statt .Body.Data.PAC der Wert .Body.Data:TOTAL_Energy "ausgeschnitten" wird
	pv_kwh=$(echo $pv_watt_tmp | jq '.Body.Data.TOTAL_ENERGY.Values' | sed '2!d' |sed 's/.*: //' )
	#Dieser Wert wird nun in die ramdisk gespeichert
	echo $pv_kwh > /var/www/html/openWB/ramdisk/pvkwh




P.S. openWB 2.x ist für mich leider KEINE Option mehr; siehe Nutzungsbedingungen. :(

