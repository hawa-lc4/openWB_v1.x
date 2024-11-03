#!/bin/bash
# this is a simplified installation script to install openWB 1.9 an my Raspberry Pi 4B with OS Debian 12 (Bookworm).
# Python 3.11.2, as included in Debian 12 OS, is installed in a virtual environment together with the Python packages
# needed by openWB 1.9. The depending packages are listed in newly created file 'python-requirements.txt'.
# For more detailed information about changes regarding OS Debian 12 see also 'adapt_RPI-4B.txt'.

echo "install required packages..."
sudo apt update
sudo apt -q -y install vim bc apache2 php php-gd php-curl php-xml php-json libapache2-mod-php jq raspberrypi-kernel-headers i2c-tools git mosquitto mosquitto-clients socat sshpass
echo "...done"

# echo "check for timezone"
if  grep -Fxq "Europe/Berlin" /etc/timezone
then
	echo "...ok"
else
	sudo /bin/su -c "echo 'Europe/Berlin' > /etc/timezone"
	sudo dpkg-reconfigure -f noninteractive tzdata
	sudo cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime
	echo "...changed"
fi

echo "check for i2c bus"
echo "enabling and access to i2c bus is done by raspi-config!"
# if grep -Fxq "i2c-bcm2835" /etc/modules
# then
# 	echo "...ok"
# else
# 	# echo "i2c-dev" >> /etc/modules
# 	echo "i2c-bcm2708" >> /etc/modules
# 	echo "i2c-bcm2835" >> /etc/modules
# 	echo "dtparam=i2c1=on" >> /etc/modules
# 	echo "dtparam=i2c_arm=on" >> /etc/modules
# fi

echo "check for initial git clone"
if [ ! -d /var/www/html/openWB/web ]; then
	cd /var/www/html/
	# git clone https://github.com/snaptec/openWB.git --branch master
	sudo git clone https://github.com/hawa-lc4/openWB_v1.x.git --branch adapt_RPI-4B openWB
	sudo chown -R pi:pi openWB 
	echo "... git cloned"
else
	echo "...ok"
fi

if ! grep -Fq "bootmodus=" /var/www/html/openWB/openwb.conf
then
	echo "bootmodus=3" >> /var/www/html/openWB/openwb.conf
fi

echo "check for ramdisk" 
if grep -Fxq "tmpfs /var/www/html/openWB/ramdisk tmpfs nodev,nosuid,size=32M 0 0" /etc/fstab 
then
	echo "...ok"
else
	sudo mkdir -p /var/www/html/openWB/ramdisk
	sudo /bin/su -c "echo 'tmpfs /var/www/html/openWB/ramdisk tmpfs nodev,nosuid,size=32M 0 0' >> /etc/fstab"
	sudo mount -a
	echo "0" > /var/www/html/openWB/ramdisk/ladestatus
	echo "0" > /var/www/html/openWB/ramdisk/llsoll
	echo "0" > /var/www/html/openWB/ramdisk/soc
	echo "...created"
fi

# start mosquitto
sudo service mosquitto start

# check for mosquitto configuration
if [ ! -f /etc/mosquitto/conf.d/openwb.conf ]; then
	echo "updating mosquitto config file"
	sudo cp /var/www/html/openWB/web/files/mosquitto.conf /etc/mosquitto/conf.d/openwb.conf
	sudo service mosquitto reload
fi

echo "disable cronjob logging"
if grep -Fxq "EXTRA_OPTS=\"-L 0\"" /etc/default/cron
then
	echo "...ok"
else
	sudo /bin/su -c "echo 'EXTRA_OPTS=\"-L 0\"' >> /etc/default/cron"
fi

#prepare for Buster or whatever
echo -n "fix upload limit..."
if [ -d "/etc/php/7.0/" ]; then
	echo "OS Stretch (Debian 9)"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/7.0/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/7.0/apache2/conf.d/20-uploadlimit.ini"
elif [ -d "/etc/php/7.3/" ]; then
	echo "OS Buster (Debian 10)"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/7.3/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/7.3/apache2/conf.d/20-uploadlimit.ini"
elif [ -d "/etc/php/7.4/" ]; then
	echo "OS Bullseye (Debian 11)"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/7.4/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/7.4/apache2/conf.d/20-uploadlimit.ini"
elif [ -d "/etc/php/8.1/" ]; then
	echo "OS Bullseye (Debian 11)"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/8.1/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/8.1/apache2/conf.d/20-uploadlimit.ini"
elif [ -d "/etc/php/8.2/" ]; then
	echo "OS Bookworm (Debian 12)"
	sudo /bin/su -c "echo 'upload_max_filesize = 300M' > /etc/php/8.2/apache2/conf.d/20-uploadlimit.ini"
	sudo /bin/su -c "echo 'post_max_size = 300M' >> /etc/php/8.2/apache2/conf.d/20-uploadlimit.ini"
fi
echo "...limit fixed"

echo "installing python packages and create Python virtual environment for openWB 1.9"
sudo apt install python3-venv
if [ `whoami` != "pi" ]; then
	echo "run script as user pi only!"
	exit
else
	python3 -m venv /home/pi/openwb1-venv
	source /home/pi/openwb1-venv/bin/activate
	cd /var/www/html/openWB
	pip3 install -r python-requirements.txt
fi
echo "...done"

sudo /bin/su -c "echo 'www-data ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/010_pi-nopasswd"

chmod 777 /var/www/html/openWB/openwb.conf
chmod +x /var/www/html/openWB/modules/*
chmod +x /var/www/html/openWB/runs/*
chmod +x /var/www/html/openWB/*.sh
sudo touch /var/log/openWB.log
sudo chmod 777 /var/log/openWB.log
sudo -u pi /var/www/html/openWB/runs/atreboot.sh
