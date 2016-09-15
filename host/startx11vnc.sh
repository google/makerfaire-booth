#!/bin/sh
# Enable this by creating a file:
# /etc/lightdm/lightdm.conf.d/50-x11vnc.conf
# containing:
#[SeatDefaults]
#display-setup-script=/home/makerfaire/makerfaire-bayarea-2016/makerfaire-2016/host/startx11vnc.sh
x11vnc -auth /var/run/lightdm/root/:0 -forever > /var/log/x11vnc.log 2>&1 &
