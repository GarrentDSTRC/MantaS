cmake_minimum_required(VERSION 3.0.2)
project(sensor_fish)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

# Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

# Add message files
add_message_files(
  FILES
  Warmdepth.msg
  BatteryStatus.msg
  DVLData.msg
)

# Generate added messages and services
generate_messages(
  DEPENDENCIES
  std_msgs
)

# Declare the catkin package
catkin_package(
  CATKIN_DEPENDS rospy std_msgs message_runtime
)

# Specify additional locations of header files
include_directories(
  ${catkin_INCLUDE_DIRS}
)

# Install Python scripts
catkin_install_python(PROGRAMS 
  scripts/Battery_read.py
  scripts/DVL_IMU_read.py
  scripts/Depth_sensor.py
  scripts/High_sensor.py
  scripts/Loushui_IO.py

  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
