#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import serial
import time


def main():
    # 初始化ROS节点
    rospy.init_node('serial_publisher', anonymous=True)

    # 创建一个发布者，发布到 'serial_data' 主题
    pub = rospy.Publisher('serial_data', String, queue_size=10)

    # 配置串口
    ser = serial.Serial(
        port='/dev/ttyUSB0',  # 替换为你的串口设备路径，例如 /dev/ttyUSB0
        baudrate=9600,  # 替换为正确的波特率
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1  # 设置读取超时
    )

    # Hex命令发送（如图所示）
    hex_command = '010300000002c40b'

    # 将hex命令转换为字节
    command_bytes = bytes.fromhex(hex_command)
    print(command_bytes)

    # 循环发布串口数据
    rate = rospy.Rate(1)  # 设置发布频率为1Hz
    while not rospy.is_shutdown():
        # 发送命令
        ser.write(command_bytes)

        # 等待响应
        time.sleep(1)

        # 读取响应
        response = ser.read(ser.inWaiting())

        # 打印并发布响应
        if response:
            response_hex = response.hex()
            rospy.loginfo(f"Received: {response_hex}")
            pub.publish(response_hex)
        else:
            rospy.logwarn("No response received")

        rate.sleep()

    # 关闭串口
    ser.close()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        passß
