#!/bin/bash


# The URL variuabile where we will store the final address to open
URL=''


# Disable all energy save features, and leave the monitor always on
xset s off         # don't activate screensaver
xset -dpms         # disable DPMS (Energy Star) features.
xset s noblank     # don't blank the video device

# Hide mouse cursor
#unclutter -display :0.0 -noevents -grab -root -reset &


# Autostart Chromium in Fullscreen mode
exec python /home/makerfaire/makerfaire-booth/2018/burger/camera_markers/camera.py
