#!/usr/bin/env python3

import rospy
from manta.msg import Warmdepth  # 确保消息类型与发布者一致
import time

class DepthDataSubscriber:
    def __init__(self):
        self.data_count = 0
        self.start_time = time.time()

    def depth_data_callback(self, msg):
        # 处理接收到的深度数据
        rospy.loginfo(f"Received depth data:\n Depth: {msg.depth}")
        time.sleep(0.1)
        # 计数接收到的消息数量
        self.data_count += 1

        # 计算并打印读取频率
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 1.0:
            rospy.loginfo(f"Depth Data Read Frequency: {self.data_count} messages per second")
            self.data_count = 0
            self.start_time = time.time()

def main():
    rospy.init_node('depth_sensor_data_subscriber', anonymous=True)
    
    subscriber = DepthDataSubscriber()
    
    # 订阅'depth_sensor_data'话题
    rospy.Subscriber('depth_sensor_data', Warmdepth, subscriber.depth_data_callback)
    
    # 保持节点运行
    rospy.spin()

if __name__ == '__main__':
    main()
