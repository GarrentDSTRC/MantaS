# 设置CMake最低版本要求
cmake_minimum_required(VERSION 3.10)

# 项目名称
project(CANPing)

# 设置C++标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 添加源文件
add_executable(hello_cpp main.cpp)

# 包含头文件路径
include_directories(./controlcan.h) # 修改为您的controlcan.h头文件所在路径

# 链接共享库
target_link_libraries(hello_cpp ./libcontrolcan.so pthread)

# 设置编译选项（可选）
target_compile_options(hello_cpp PRIVATE -Wall -Wextra)
