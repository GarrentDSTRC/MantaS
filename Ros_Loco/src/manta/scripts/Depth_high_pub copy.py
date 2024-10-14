#!/usr/bin/env python3

import rospy
from manta.msg import Warmdepth as HeightMsg  # 高度传感器消息类型
from manta.msg import Warmdepth as DepthMsg        # 深度传感器消息类型
from manta.msg import CommandMsg                   # 控制命令消息类型
import time
import signal
import sys

class HeightController:
    def __init__(self, target_height=10.0):
        self.target_height = target_height
        self.current_height = 0.0
        self.triggered = False  # 触发定深控制的标志
        self.control_countWZY = 0
        # 订阅高度传感器数据
        self.height_sub = rospy.Subscriber('altitude_sensor_data', HeightMsg, self.height_callback)
        
        # 注册信号处理函数
        signal.signal(signal.SIGINT, self.shutdown)
    
    def height_callback(self, msg):
        self.current_height = msg.height
        rospy.loginfo(f"Received Height Data: {self.current_height} meters")
        
        # 如果当前高度达到了目标高度，并且还没有触发定深控制
        if self.current_height >= self.target_height and not self.triggered:
            rospy.loginfo("Target height reached, triggering depth control.")
            self.trigger_depth_control()
            self.triggered = True
    
    def trigger_depth_control(self):
        # 初始化并启动深度控制器
        depth_controller = DepthController(target_depth=self.target_height, kp=1.0, ki=0.01, kd=0.1, duration=10.0)
        depth_controller.start()

    def shutdown(self, signum, frame):
        rospy.loginfo("Shutdown signal received.")
        sys.exit(0)

class DepthController:
    def __init__(self, target_depth=2.0, kp=1.0, ki=0.01, kd=0.1, duration=10.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target_depth = target_depth
        self.current_depth = 0.0
        self.previous_error = 0.0
        self.integral_error = 0.0
        self.previous_time = rospy.get_time()
        self.start_time = rospy.get_time()
        self.duration = duration
        self.control_countWZY = 0
        # 计数变量
        self.depth_count = 0
        self.control_count = 0
        self.last_print_time = rospy.get_time()

        # 订阅深度传感器数据
        self.depth_sub = rospy.Subscriber('altitude_sensor_data', HeightMsg,  self.depth_callback)
        # 发布控制信号
        self.control_pub = rospy.Publisher('propeller_commands', CommandMsg, queue_size=10)

    def depth_callback(self, msg):
        self.current_depth = msg.depth
        self.depth_count += 1
        #rospy.loginfo(f"Received Depth Data: {self.current_depth} meters")
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
        control_signal = max(min(int(control_signal), 1800), -1800)  # 确保control_signal为整数类型

        # 发布控制信号
        for propeller_id in range(4):
            command_msg = CommandMsg()
            command_msg.ID = propeller_id
            command_msg.command = control_signal
            self.control_pub.publish(command_msg)
            self.control_count += 1

        # 更新前一误差和时间
        self.previous_error = error
        self.previous_time = current_time

        # 打印频率信息
        if current_time - self.last_print_time >= 1.0:
            rospy.loginfo(f"Current Depth: {self.current_depth}, Target Depth: {self.target_depth}, Control Signal: {control_signal}")
            self.depth_count = 0
            self.control_count = 0
            self.last_print_time = current_time

    def stop_all_propellers(self):
        # 停止所有推进器
        for _ in range(2):
            for propeller_id in range(4):
                command_msg = CommandMsg()
                command_msg.ID = propeller_id
                command_msg.command = 0
                self.control_pub.publish(command_msg)
                rospy.loginfo(f"Stopped Propeller {propeller_id}")
            rospy.sleep(0.3)

    def start(self):
        rospy.spin()

def main():
    rospy.init_node('height_and_depth_control_node', anonymous=True)
    
    # 启动高度控制器
    height_controller = HeightController(target_height=1.0)

    # 保持节点运行
    rospy.spin()

if __name__ == '__main__':
    main()
