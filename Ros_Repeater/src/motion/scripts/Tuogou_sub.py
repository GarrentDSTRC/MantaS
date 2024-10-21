#!/usr/bin/env python
import sys
import os
import threading
# 确保当前脚本目录在 sys.path 中
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)
    
from Motor_class import CANMotorController

import rospy
from std_msgs.msg import Bool,Float32
import time
import logging

# 设置日志记录
log_file = os.path.join(script_dir, 'motor_control.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
controller = CANMotorController(motor_id=0x00)
controller.open_device()
controller.init_can_channel()
controller.start_can_channel()
class MotorControlNode2:
    def __init__(self):
        
        # 初始化CANMotorController对象
        self.ID=0x03

        # 订阅话题
        rospy.Subscriber('/absolute_description', Float32, self.control_callback)
        


    def control_callback(self, msg):

        angle = msg.data
        print("angleangleangleangle",angle)
        logging.info(f'Received control command: {"ON" if msg.data else "OFF"}, setting angle to {angle}')
        

        controller.send_angle(self.ID, angle)
        data = controller.receive_data()
        controller.parse_received_data(data)



    def on_shutdown(self):
        # 确保设备关闭
        controller.close_device()
        logging.info('CAN device closed.')

    def run(self):
        rospy.spin()
class MotorControlNode:
    def __init__(self):
        self.ID=0x04   
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
            controller.send_angle(self.ID, angle)
            data = controller.receive_data()
            controller.parse_received_data(data)

            # 等待一段时间
            time.sleep(1)  # 根据需要调整时间间隔
        

    def on_shutdown(self):
        # 确保设备关闭
        controller.close_device()
        logging.info('CAN device closed.')

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    rospy.init_node('Tuogou_control_node', anonymous=True)
    # 创建 MotorControlNode 实例
    motor_control_node = MotorControlNode()
    
    # 创建 MotorControlNode2 实例
    motor_control_node2 = MotorControlNode2()
    
    # 创建线程来运行 MotorControlNode
    thread1 = threading.Thread(target=motor_control_node.run)
    
    # 创建线程来运行 MotorControlNode2
    thread2 = threading.Thread(target=motor_control_node2.run)
    
    # 启动两个线程
    thread1.start()
    thread2.start()
    
    # 等待两个线程完成
    thread1.join()
    thread2.join()
    try:
        pass
        #motor_control_node = MotorControlNode()
        #motor_control_node.run()
    except rospy.ROSInterruptException:
        print("启动失败")
        logging.info("Caught ROS interrupt, shutting down.")
        motor_control_node.on_shutdown()
    except KeyboardInterrupt:
        logging.info("Caught keyboard interrupt, shutting down.")
        motor_control_node.on_shutdown()
    except Exception as e:
        logging.error("An error occurred: {}".format(e))
    finally:
        motor_control_node.on_shutdown()
