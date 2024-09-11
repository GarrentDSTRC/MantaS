cmake_minimum_required(VERSION 3.0.2)
project(motion)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

# # 添加消息文件
# add_message_files(
#   FILES
# )

# 生成消息
generate_messages(
  DEPENDENCIES
  std_msgs
)

# # catkin package
# catkin_package(
#   CATKIN_DEPENDS message_runtime std_msgs
# )

# 包含头文件目录
include_directories(
  ${catkin_INCLUDE_DIRS}
)


# Install Python scripts
catkin_install_python(PROGRAMS 
# scripts/data_subscriber.py
scripts/Tuogou_sub.py
scripts/IO_zhongji.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
