---
title: "WiFiCheck.sh"
date: 2023-11-13T23:08:41+01:00
draft: false
---
```sh
#!/bin/bash
##################################################################
# A Project of TNET Services, Inc
#
# Title:     WiFi_Check
# Author:    Kevin Reed (Dweeber)
#            dweeber.dweebs@gmail.com
# Project:   Raspberry Pi Stuff
#
# Copyright: Copyright (c) 2012 Kevin Reed <kreed@tnet.com>
#            https://github.com/dweeber/WiFi_Check
#
# Purpose:
#
# Script checks to see if WiFi has a network IP and if not
# restart WiFi
#
# Uses a lock file which prevents the script from running more
# than one at a time.  If lockfile is old, it removes it
#
# Instructions:
#
# o Install where you want to run it from like /usr/local/bin
# o chmod 0755 /usr/local/bin/WiFi_Check
# o Add to crontab
#
# Run Every 5 mins - Seems like ever min is over kill unless
# this is a very common problem.  If once a min change */5 to *
# once every 2 mins */5 to */2 ...
#
# */5 * * * * /usr/local/bin/WiFi_Check
#
# Quelques modifications pour chemin d'accès du pid et localisation du script
##################################################################
# Settings
# Where and what you want to call the Lockfile
lockfile='/home/pi/WiFi/WiFi_Check.pid'
# Which Interface do you want to check/fix
wlan='wlan0'
pingip='192.168.1.1'
##################################################################
echo
echo "Starting WiFi check for $wlan"
date
echo

# Check to see if there is a lock file
if [ -e $lockfile ]; then
    # A lockfile exists... Lets check to see if it is still valid
    pid=`cat $lockfile`
    if kill -0 &>1 > /dev/null $pid; then
        # Still Valid... lets let it be...
        echo "Process still running, Lockfile valid"
        exit 1
    else
        # Old Lockfile, Remove it
        #echo "Old lockfile, Removing Lockfile"
        rm $lockfile
    fi
fi
# If we get here, set a lock file using our current PID#
echo "Setting Lockfile"
echo $$ > $lockfile

# We can perform check
echo "Performing Network check for $wlan"
/bin/ping -c 2 -I $wlan $pingip > /dev/null 2> /dev/null
if [ $? -ge 1 ] ; then
    echo "Network connection down! Attempting reconnection."
    /sbin/ifdown $wlan
    /bin/sleep 5
    /sbin/ifup --force $wlan
else
    echo "Network is Okay"
fi

echo
echo "Current Setting:"
ifconfig $wlan | grep "inet"
echo

# Check is complete, Remove Lock file and exit
#echo "process is complete, removing lockfile"
rm $lockfile
exit 0

##################################################################
# End of Script
##################################################################
```
