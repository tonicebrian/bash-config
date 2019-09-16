#!/bin/bash

# Allow nautilus to take care of plugin USB drives and Dropbox icons
/usr/lib/gnome-settings-daemon/gnome-fallback-mount-helper &

xrdb -merge .Xresources

trayer --edge top --align right --SetDockType true --expand true --width 15 --height 18 --transparent true --tint 0x000000 &

if [ -x /usr/bin/nm-applet ] ; then
   nm-applet --sm-disable &
fi
 
if [ -x /usr/bin/gnome-settings-daemon ] ; then
   sleep 1
   gnome-settings-daemon &
fi
 
/usr/bin/gnome-volume-control-applet &
dropbox start &

# Fast terminal anywhere
guake &

exec xmonad
