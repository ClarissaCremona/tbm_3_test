#!/bin/bash

VAR1=ifconfig wlan0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'

gnome-terminal -x bash -c "roscore && bash"
sleep 1
gnome-terminal -x bash -c "cd ~/catkin_ws && export ROS_IP=192.168.1.63 && roslaunch roah_rsbb roah_rsbb.launch && bash"  
sleep 1 
gnome-terminal -x bash -c "cd ~/catkin_ws && roslaunch iot_bridge iot.launch && bash"



