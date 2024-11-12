#!/bin/bash

# 启用调试信息输出
set -x

# 设置日志文件路径
LOG_FILE=/home/jetson/Dayu_Scripts/log/loushui.log

# 添加日志函数，包含时间戳
log_with_timestamp() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

# 设置 ROS Master URI 和 ROS IP
export ROS_MASTER_URI=http://192.168.50.10:11311
export ROS_IP=192.168.50.13

# 加载ROS环境
source /opt/ros/noetic/setup.bash
source /home/jetson/Manta/Ros_Repeater/devel/setup.bash

# 添加日志输出以查看路径和环境变量
log_with_timestamp "ROS Noetic setup sourced"
log_with_timestamp "Running rosrun command"

# 运行ROS节点并将输出重定向到日志文件，包含时间戳
{
    rosrun motion loushui.py
} >> $LOG_FILE 2>&1

# 添加结束日志
log_with_timestamp "rosrun command finished"

