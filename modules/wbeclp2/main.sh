#!/bin/bash

source /home/pi/openwb1-venv/bin/activate

rekwh='^[-+]?[0-9]+\.?[0-9]*$'
stb=`cat /var/www/html/openWB/ramdisk/llstandbys1`

if (( $stb >= 4 )); then
  exit 4
fi

output=$(python3 /var/www/html/openWB/modules/wbeclp2/readwbec.py $wbeclp2ip $wbeclp2port $wbeclp2mbid)

if [ -z "${output}" ]; then
  stb=$((stb + 1))
  echo "$stb" > /var/www/html/openWB/ramdisk/llstandbys1
  exit 2
fi
echo 0 > /var/www/html/openWB/ramdisk/llstandbys1

n=0
while read -r line; do
  if (( $n == 0 )); then
    case "$line" in
      4 | 5)
        echo 1 > /var/www/html/openWB/ramdisk/plugstats1
        echo 0 > /var/www/html/openWB/ramdisk/chargestats1
        python /var/www/html/openWB/runs/ledss1.py an1
        ;;
      6)
        echo 1 > /var/www/html/openWB/ramdisk/plugstats1
        echo 1 > /var/www/html/openWB/ramdisk/chargestats1
        python /var/www/html/openWB/runs/ledss1.py an1
        ;;
      7)
        echo 1 > /var/www/html/openWB/ramdisk/plugstats1
        echo 1 > /var/www/html/openWB/ramdisk/chargestats1
        python /var/www/html/openWB/runs/ledss1.py an12
        ;;
      *)
        echo 0 > /var/www/html/openWB/ramdisk/plugstats1
        echo 0 > /var/www/html/openWB/ramdisk/chargestats1
        python /var/www/html/openWB/runs/ledss1.py aus
        ;;
    esac
  fi
  if (( $n == 1 )); then
    echo "$line" > /var/www/html/openWB/ramdisk/llas11
  fi
  if (( $n == 2 )); then
    echo "$line" > /var/www/html/openWB/ramdisk/llas12
  fi
  if (( $n == 3 )); then
    echo "$line" > /var/www/html/openWB/ramdisk/llas13
  fi
  if (( $n == 4 )); then
    echo "$line" > /var/www/html/openWB/ramdisk/llvs11
  fi
  if (( $n == 5 )); then
    echo "$line" > /var/www/html/openWB/ramdisk/llvs12
  fi
  if (( $n == 6 )); then
    echo "$line" > /var/www/html/openWB/ramdisk/llvs13
  fi
  if (( $n == 7 )); then
    echo "$line" > /var/www/html/openWB/ramdisk/llaktuells1
  fi
  if (( $n == 8 )); then
    llkwhs1=$(echo "$line")
    if [[ $llkwhs1 =~ $rekwh ]]; then
      echo $llkwhs1 > /var/www/html/openWB/ramdisk/llkwhs1
    fi
  fi

  n=$((n + 1))
done <<< "$output"
