cmake_minimum_required(VERSION 3.0.2)
project(manta)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

# 添加消息文件
add_message_files(
  FILES
  Warmdepth.msg
  MotorCommandMsg.msg
  PropellerCommandMsg.msg
  CommandMsg.msg
  
)

# 生成消息
generate_messages(
  DEPENDENCIES
  std_msgs
)

# catkin package
catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs
)

# 包含头文件目录
include_directories(
  ${catkin_INCLUDE_DIRS}
)


# Install Python scripts
catkin_install_python(PROGRAMS
  scripts/Depth_high_pub.py
  scripts/High_pub.py
  scripts/Deepth_pub.py
  scripts/Pub_Huxiji.py
  scripts/IO_dayu.py
  scripts/IO_zhongji.py
  scripts/Pub_Motion_2.py
  scripts/Pub_Motion.py
  scripts/Pub_Tuogou.py
  scripts/Sub_Depth.py
  scripts/Sub_Warmdepth.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)