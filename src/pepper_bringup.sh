#!/bin/bash

gnome-terminal -x bash -c "export ROS_MASTER_URI=http://192.168.1.129:11311 && export ROS_IP=192.168.1.63 && roslaunch pepper_bringup pepper_full_py.launch nao_ip:=192.168.1.121 roscore:=192.168.1.129 && bash"  
sleep 7 
gnome-terminal -x bash -c "cd ~/catkin_ws && rosrun tbm_3_test TBM3.py && bash"



