cmake_minimum_required(VERSION 3.0.2)
project(motion_control)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

# Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)
# 添加消息文件
add_message_files(
  FILES
  MotorCommandMsg.msg
  PropellerCommandMsg.msg
  
)

# 生成消息
generate_messages(
  DEPENDENCIES
  std_msgs
)

# catkin package
catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs rospy
)


# Specify additional locations of header files
include_directories(
  ${catkin_INCLUDE_DIRS}
)

# Install Python scripts
catkin_install_python(PROGRAMS 
  scripts/ActuationControl.py
  scripts/IO_sub.py
  scripts/ActuationControl_protect.py
  scripts/IO_sub_protect.py
  scripts/Control_Final.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

