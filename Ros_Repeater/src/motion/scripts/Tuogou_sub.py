#!/usr/bin/env python
import sys
import os

# 确保当前脚本目录在 sys.path 中
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)
    
from Motor_class import CANMotorController

import rospy
from std_msgs.msg import Bool
import time
import logging

# 设置日志记录
log_file = os.path.join(script_dir, 'motor_control.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MotorControlNode:
    def __init__(self):
        rospy.init_node('Tuogou_control_node', anonymous=True)
        
        # 初始化CANMotorController对象
        self.controller = CANMotorController(motor_id=0x03)
        
        # 开启设备
        self.controller.open_device()
        self.controller.init_can_channel()
        self.controller.start_can_channel()

        # 订阅话题
        rospy.Subscriber('Tuogou_control', Bool, self.control_callback)
        
        # 在节点关闭时调用的回调函数
        rospy.on_shutdown(self.on_shutdown)

    def control_callback(self, msg):
        if msg.data:
            angle = 10
        else:
            angle = 115
        logging.info(f'Received control command: {"ON" if msg.data else "OFF"}, setting angle to {angle}')
        
        for _ in range(2):
            # 第一次发送角度指令
            self.controller.send_angle_newM(self.controller.motor_id, angle)
            data = self.controller.receive_data()
            self.controller.parse_received_data(data)

            # 等待一段时间
            time.sleep(1)  # 根据需要调整时间间隔
        
        # 关闭节点
        rospy.signal_shutdown('Task completed and shutting down.')

    def on_shutdown(self):
        # 确保设备关闭
        self.controller.close_device()
        logging.info('CAN device closed.')

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        motor_control_node = MotorControlNode()
        motor_control_node.run()
    except rospy.ROSInterruptException:
        logging.info("Caught ROS interrupt, shutting down.")
        motor_control_node.on_shutdown()
    except KeyboardInterrupt:
        logging.info("Caught keyboard interrupt, shutting down.")
        motor_control_node.on_shutdown()
    except Exception as e:
        logging.error("An error occurred: {}".format(e))
    finally:
        motor_control_node.on_shutdown()
