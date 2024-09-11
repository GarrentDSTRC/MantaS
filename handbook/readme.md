配置master

.bashrc 配置
Master设备 (192.168.1.1):
bash
复制代码
export ROS_MASTER_URI=http://192.168.1.1:11311
export ROS_IP=192.168.1.1

从设备1 (192.168.1.2):
bash
复制代码
export ROS_MASTER_URI=http://192.168.1.1:11311
export ROS_IP=192.168.1.2

从设备2 (192.168.1.3):
bash
复制代码
export ROS_MASTER_URI=http://192.168.1.1:11311
export ROS_IP=192.168.1.3