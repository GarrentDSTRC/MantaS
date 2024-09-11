#!/usr/bin/env python3

import rospy
from sensor_fish.msg import Warmdepth  # 假设这是深度传感器消息类型
from manta.msg import CommandMsg  # 导入CommandMsg消息类型
import time

class PDDepthController:
    def __init__(self, target_depth, kp=1.0, kd=0.1, duration=10.0):
        self.kp = kp
        self.kd = kd
        self.target_depth = target_depth
        self.current_depth = 0.0
        self.previous_error = 0.0
        self.previous_time = rospy.get_time()
        self.start_time = rospy.get_time()
        self.duration = duration
        
        # ROS订阅和发布
        self.depth_sub = rospy.Subscriber('depth_sensor_data', Warmdepth, self.depth_callback)
        self.control_pub = rospy.Publisher('motor_commands', CommandMsg, queue_size=10)

    def depth_callback(self, msg):
        self.current_depth = msg.depth
        self.control_step()

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

        # 计算PD控制输出
        p_term = self.kp * error
        d_term = self.kd * (error - self.previous_error) / delta_time if delta_time > 0 else 0.0
        control_signal = p_term + d_term

        # 将控制信号限制在300到500之间
        control_signal = max(min(control_signal, 500), 300)

        # 为每个推进器创建并发布CommandMsg
        for propeller_id in range(4):  # 推进器ID从0到3
            command_msg = CommandMsg()
            command_msg.ID = propeller_id
            command_msg.command = int(control_signal)

            # 发布控制信号
            self.control_pub.publish(command_msg)

            rospy.loginfo(f"Sent to Propeller {propeller_id} - Current Depth: {self.current_depth}, Target Depth: {self.target_depth}, Control Signal: {control_signal}")

        # 更新前一误差和时间
        self.previous_error = error
        self.previous_time = current_time

    def stop_all_propellers(self):
        # 停止所有推进器
        for propeller_id in range(4):
            command_msg = CommandMsg()
            command_msg.ID = propeller_id
            command_msg.command = 0  # 停止推进器
            self.control_pub.publish(command_msg)
            rospy.loginfo(f"Stopped Propeller {propeller_id}")

if __name__ == '__main__':
    rospy.init_node('pd_depth_control_node', anonymous=True)
    
    # 本地定义目标深度
    target_depth = 1.0  # 目标深度为5米

    # 创建PD控制器实例，执行时间为10秒
    controller = PDDepthController(target_depth=target_depth, kp=1.0, kd=0.1, duration=10.0)

    # 保持节点运行
    rospy.spin()
