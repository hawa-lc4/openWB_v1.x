#!/bin/bash
#set -x
#trap read debug

if [[ "$1" == "" ]]; then
        get_host="localhost"
else
        get_host="$1"
fi

conf_file="/var/www/html/openWB/smartHome_$get_host.conf"
rm -f $conf_file 2>/dev/null
touch $conf_file

dev_top_base_get="openWB/config/get/SmartHome/Devices"
dev_top_base_set="openWB/config/set/SmartHome/Devices"
declare -a smart_home_device_config_topics=(
        "device_configured"
        "device_canSwitch"
        "device_differentMeasurement"
        "device_shauth"
        "device_measureshauth"
        "device_chan"
        "device_nxdacxxtype"
        "device_measchan"
        "device_ip"
        "device_pbip"
        "device_pbtype"
        "device_measureip"
        "device_name"
        "device_type"
        "device_measureType"
        "device_temperatur_configured"
        "device_einschaltschwelle"
        "device_deactivateper"
        "device_deactivateWhileEvCharging"
        "device_ausschaltschwelle"
        "device_ausschaltverzoegerung"
        "device_einschaltverzoegerung"
        "device_updatesec"
        "device_measureid"
        "device_speichersocbeforestart"
        "device_speichersocbeforestop"
        "device_maxeinschaltdauer"
        "device_mineinschaltdauer"
        "device_mindayeinschaltdauer"
        "device_manual_control"
        "mode"
        "device_einschalturl"
        "device_ausschalturl"
        "device_leistungurl"
        "device_stateurl"
        "device_measureurlc"
        "device_measureurl"
        "device_measurejsonurl"
        "device_measurejsonpower"
        "device_measurejsoncounter"
        "device_username"
        "device_password"
        "device_shusername"
        "device_shpassword"
        "device_manwatt"
        "device_maxueb"
        "device_measureshusername"
        "device_measureshpassword"
        "device_actor"
        "device_measureavmusername"
        "device_measureavmpassword"
        "device_measureavmactor"
        "device_acthortype"
        "device_lambdaueb"
        "device_idmueb"
        "device_acthorpower"
        "device_finishTime"
        "device_onTime"
        "device_offTime"
        "device_onuntilTime"
        "device_startTime"
        "device_endTime"
        "device_homeConsumtion"
        "device_setauto"
        "device_measurePortSdm"
        "device_dacport"
        "device_startupDetection"
        "device_standbyPower"
        "device_nonewatt"
        "device_idmnav"
        "device_nxdacxxueb"
        "device_standbyDuration"
        "device_startupMulDetection"
        "device_measuresmaage"
        "device_measuresmaser"
)

for dev_num in {1..9}; do
  for dev_top in "${smart_home_device_config_topics[@]}"; do
    dev_resp=`mosquitto_sub -h $get_host -C 1 -W 1 -t $dev_top_base_get/$dev_num/$dev_top 2>/dev/null`
    if [[ "$dev_resp" != "" ]]; then
      echo $dev_top_base_get"/"$dev_num"/"$dev_top";"$dev_resp >> $conf_file
      if [[ "$get_host" != "localhost" ]]; then
        mosquitto_pub -h localhost -t $dev_top_base_set/$dev_num/$dev_top -m $dev_resp
      fi
    fi
  done
done
