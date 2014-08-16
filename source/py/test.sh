#!/bin/bash

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

check_package php5
