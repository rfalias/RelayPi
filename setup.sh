#!/bin/bash

#####################################
# RelayPi created by rfalias
# Using GNU GPL
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  See <http://www.gnu.org/licenses/>.
#
#
#####################################

function check_package {
        pkg=$1
        PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $pkg |grep "install ok installed")
        echo Checking for php:
        if [ "" == "$PKG_OK" ]; then
        echo "No $pkg. Setting up $pkg."
        #sudo apt-get --force-yes --yes install $pkg
        else
        echo "$pkg installed"
        fi
}
#Check pre-req
check_package php5
check_package php5-curl
check_package python2.7

echo Copying init scripts
cp ./source/daemon/sensord /etc/init.d/sensord
echo Copying scripts
cp ./source/py/sensorwatch.py /usr/local/bin/sensorw/sensorwatch.py
echo Copying Web
webroot=$(cat /etc/apache2/sites-available/default | grep DocumentRoot | sed -e 's/DocumentRoot//g' | sed -e 's/^[ \t]*//' -e 's/[ \t]*$//')
echo "Default WebRoot [$webroot]?"
read defaultWR
if [[ -z "$defaultWR" ]]
then
	webroot=$webroot
else
	webroot=$defaultWR
fi
echo "Copying php scripts to $webroot"
cp ./source/www/toggle.php $webroot
cp ./source/www/getstate.php $webroot
cp ./source/www/tail.php $webroot
echo "Configuring daemeon start options..."
update-rc.d sensord start 20 3 4 5 > /dev/null 2>&1
echo "Starting sensord daemon...."
/etc/init.d/sensord start
echo "Testing relay..."
wget http://127.0.0.1:8080?state=0 --delete-after > /dev/null 2>&1
sleep 1
wget http://127.0.0.1:8080?state=1 --delete-after > /dev/null 2>&1
sleep 1
wget http://127.0.0.1:8080?state=0 --delete-after > /dev/null 2>&1
sleep 1
wget http://127.0.0.1:8080?state=1 --delete-after > /dev/null 2>&1
echo "Setup complete!"

