#!/bin/bash

VAR1=ifconfig wlan0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'

gnome-terminal -x bash -c "cd ~/catkin_ws && export ROS_MASTER_URI=http://192.168.1.129:11311 && export ROS_IP=$VAR1 && rostopic list && bash" 
sleep 1

gnome-terminal -x sh -c "roslaunch pepper_bringup pepper_full_py.launch nao_ip:=192.168.1.121 roscore:=192.168.1.63; bash" &
#sleep 1

 
