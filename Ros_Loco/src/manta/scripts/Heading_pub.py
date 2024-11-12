#!/usr/bin/env python3

import rospy
from manta.msg import DVLData
from manta.msg import CommandMsg  # 导入CommandMsg消息类型
import time
import signal
import sys

class PIDHeadingController:
    def __init__(self, target_heading, kp=1.0, ki=0.01, kd=0.1, duration=10.0,basespeed=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target_depth = target_heading
        self.current_depth = 0.0
        self.previous_error = 0.0
        self.integral_error = 0.0
        self.previous_time = rospy.get_time()
        self.start_time = rospy.get_time()
        self.duration = duration
        self.basespeed=basespeed
        
        # 计数变量
        self.depth_count = 0
        self.control_count = 0
        self.control_countWZY = 0
        self.last_print_time = rospy.get_time()

        # 控制频率限制为10Hz
        self.rate = rospy.Rate(30)

        # ROS订阅和发布
        self.depth_sub = rospy.Subscriber('dvl/data', DVLData, self.depth_callback)
        self.control_pub = rospy.Publisher('propeller_commands', CommandMsg, queue_size=10)

        # 注册信号处理函数
        signal.signal(signal.SIGINT, self.shutdown)

    def depth_callback(self, msg): 
        self.current_heading = msg.heading
        self.depth_count += 1
        #rospy.loginfo(f"Current Depth: {self.current_depth}")
        # print(f"Received Depth Data: {self.current_depth} meters")  # 打印接收到的深度信息
        
        if self.control_countWZY%30==0:
            self.control_step()  # 每次接收到深度数据时进行一次控制
        self.control_countWZY+=1
    def control_step(self):
        
        current_time = rospy.get_time()

        # 检查是否超过了设定的时间
        if current_time - self.start_time > self.duration:
            rospy.loginfo("Depth control duration has ended. Stopping all propellers.")
            self.stop_all_propellers()
            rospy.signal_shutdown("Depth control finished")
            return

        # 计算误差
        error = self.target_depth - self.current_depth
        delta_time = current_time - self.previous_time

        # 计算PID控制输出
        self.integral_error += error * delta_time
        p_term = self.kp * error
        i_term = self.ki * self.integral_error
        d_term = self.kd * (error - self.previous_error) / delta_time if delta_time > 0 else 0.0
        control_signal = p_term + i_term + d_term

        # 将控制信号限制在300到500之间
        control_signal = -1* max(min(int(control_signal), 2200), -2200)  # 确保control_signal为整数类型

        # 发布控制信号
        command_msg = CommandMsg()

        command_msg.ID = 6
        command_msg.command = self.basespeed+control_signal  # 将控制信号作为整数传递
        # 发布控制信号
        self.control_pub.publish(command_msg)
        command_msg.ID = 7
        command_msg.command = self.basespeed-control_signal 
        self.control_pub.publish(command_msg)

        self.control_count += 1

            # rospy.loginfo(f"Sent to Propeller {propeller_id} - Current Depth: {self.current_depth}, Target Depth: {self.target_depth}, Control Signal: {control_signal}")

        # 更新前一误差和时间
        self.previous_error = error
        self.previous_time = current_time

        # 打印频率信息
        if current_time - self.last_print_time >= 1.0:
            rospy.loginfo(f"Current Depth: {self.current_depth}, Target Depth: {self.target_depth}, Control Signal: {control_signal}")
            # rospy.loginfo(f"Depth Read Frequency: {self.depth_count} Hz, Control Publish Frequency: {self.control_count} Hz")
            self.depth_count = 0
            self.control_count = 0
            self.last_print_time = current_time

            self.integral_error=0

        # 控制频率限制为10Hz
        self.rate.sleep()

    def stop_all_propellers(self):
        # 执行两次停止所有推进器的操作
        for _ in range(2):  # 重复两次
            for propeller_id in range(4):
                command_msg = CommandMsg()
                command_msg.ID = propeller_id
                command_msg.command = 0  # 停止推进器
                self.control_pub.publish(command_msg)
                rospy.loginfo(f"Stopped Propeller {propeller_id}")
            # 可以在每次循环后稍作等待，以确保命令已被处理
            rospy.sleep(0.3)  # 减少等待时间

    def shutdown(self, signum, frame):
        rospy.loginfo("Shutdown signal received, stopping all propellers.")
        self.stop_all_propellers()
        sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('pid_heading_control_node', anonymous=True)
    
    # 本地定义目标深度
    target_heading = 1.2# 目标heading为1米
    basespeed=0
    duration=180
    # 创建PID控制器实例，执行时间为10秒
    controller = PIDDepthController(target_heading=target_heading, kp=1, ki=0, kd=0, duration=duration,basespeed=basespeed)

    # 保持节点运行
    rospy.spin()
