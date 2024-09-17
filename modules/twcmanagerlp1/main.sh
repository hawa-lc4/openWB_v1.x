#!/bin/bash

wbeclp2ip=$twcmanagerlp2ip
wbeclp2port=$twcmanagerlp2port
# wbeclp2ip='192.168.183.114'
# wbeclp2port=502
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

n=0
output=$(sudo python3 /var/www/html/openWB/modules/twcmanagerlp2/readwbec.py $wbeclp2ip $wbeclp2port)

while read -r line; do
        if (( $n == 0 )); then
                case "$line" in
                        4 | 5)
                                echo 1 > /var/www/html/openWB/ramdisk/plugstat
                                echo 0 > /var/www/html/openWB/ramdisk/chargestat
                                ;;
                        6 | 7)
                                echo 1 > /var/www/html/openWB/ramdisk/plugstat
                                echo 1 > /var/www/html/openWB/ramdisk/chargestat
                                ;;
                        *)
                                echo 0 > /var/www/html/openWB/ramdisk/plugstat
                                echo 0 > /var/www/html/openWB/ramdisk/chargestat
                                ;;
                esac
        if (( $n == 1 )); then
                echo "$line" > /var/www/html/openWB/ramdisk/lla1
        fi
        if (( $n == 2 )); then
                echo "$line" > /var/www/html/openWB/ramdisk/lla2
        fi
        if (( $n == 3 )); then
                echo "$line" > /var/www/html/openWB/ramdisk/lla3
        fi
        if (( $n == 4 )); then
                echo "$line" > /var/www/html/openWB/ramdisk/llv1
        fi
        if (( $n == 5 )); then
                echo "$line" > /var/www/html/openWB/ramdisk/llv2
        fi
        if (( $n == 6 )); then
                echo "$line" > /var/www/html/openWB/ramdisk/llv3
        fi
        if (( $n == 7 )); then
                echo "$line" > /var/www/html/openWB/ramdisk/llaktuell
        fi
        if (( $n == 8 )); then
                llkwhs1=$(echo "$line")
                if [[ $llkwhs1 =~ $rekwh ]]; then
                        echo $llkwhs1 > /var/www/html/openWB/ramdisk/llkwh
                fi
        fi

        n=$((n + 1))
done <<< "$output"
