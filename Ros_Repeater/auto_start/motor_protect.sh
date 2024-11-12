#!/bin/bash

# 启用调试信息输出
set -x

# 设置 ROS Master URI 和 ROS IP
export ROS_MASTER_URI=http://192.168.50.10:11311
export ROS_IP=192.168.50.10

source /opt/ros/noetic/setup.bash
source /home/jetson/Manta/Ros_Fish/devel/setup.bash

# 添加日志输出以查看路径和环境变量
echo "ROS Noetic setup sourced" >> /home/jetson/Dayu_Scripts/motor_control.log
echo "Running rosrun command" >> /home/jetson/Dayu_Scripts/motor_control.log

rosrun motion_control ActuationControl_protect.py >> /home/jetson/Dayu_Scripts/motor_control.log 2>&1

# 添加结束日志
echo "rosrun command finished" >> /home/jetson/Dayu_Scripts/motor_control.log

