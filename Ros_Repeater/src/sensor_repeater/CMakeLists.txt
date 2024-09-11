cmake_minimum_required(VERSION 3.0.2)
project(sensor_repeater)

## 找到catkin的依赖包
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

## 添加消息文件
add_message_files(
  FILES
  CTD.msg
)

## 生成消息
generate_messages(
  DEPENDENCIES
  std_msgs
)

## 包的描述信息
catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs rospy
)

## 包含头文件的路径
include_directories(
  ${catkin_INCLUDE_DIRS}
)

## 安装Python脚本
catkin_install_python(PROGRAMS
  scripts/Do_sensor.py
  scripts/CTD_sensor.py
  scripts/PH_sensor.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
