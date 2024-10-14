#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
import serial
import time
import math
import csv
import threading
from queue import Queue

# 定义串口通信参数
port = '/dev/ttyUSB0'
baudrate = 9600
timeout = 1

# 定义公式中的常数
c1 = -0.029
c2 = 0.000115
T = 25  # 假设的温度值，您需要根据实际情况设置
Pressure = 1  # 假设的压力值，您需要根据实际情况设置

# 初始化CSV文件
csv_file = 'do_values.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'DO Value'])

data_queue = Queue()
shutdown_event = threading.Event()

def serial_communication():
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        rospy.loginfo(f"串口 {port} 已打开。")

        # 定义要发送的固定数据
        fixed_command = bytes.fromhex("01 03 00 00 00 02 c4 0b")

        while not rospy.is_shutdown() and not shutdown_event.is_set():
            ser.write(fixed_command)  # 发送数据

            # 等待一段时间，确保数据发送完成
            time.sleep(0.1)

            # 读取串口数据
            if ser.in_waiting > 0:
                received_data = ser.read(ser.in_waiting).hex().upper()

                # 检查数据长度是否足够
                if len(received_data) >= 14:
                    data_value1_hex = received_data[10:14]
                    o1 = int(data_value1_hex, 16)  # 将十六进制的数据值1转换为十进制
                    O1 = o1 * (5/4096)


                    # 计算DO值
                    DO = (O1 - 0.002) * math.exp((T * c1 + Pressure * c2)) * 100 / (math.exp((T * c1)) * 3.49)
                    rospy.loginfo(f"计算得到的DO值: {DO}")

                    # 将DO值放入队列
                    data_queue.put(DO)

                else:
                    rospy.logwarn("接收到的数据长度不足,无法解析数据值1")

            # 等待下一个发布周期
            # time.sleep(0.5)

    except serial.SerialException as e:
        rospy.logerr(f"串口通信错误: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()  # 关闭串口
            rospy.loginfo("串口已关闭")

def save_to_csv():
    while not rospy.is_shutdown() and not shutdown_event.is_set():
        if not data_queue.empty():
            DO = data_queue.get()
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), DO])
                rospy.loginfo(f"已保存: DO值={DO}")
        # time.sleep(0.1)

def ros_publisher():
    rospy.init_node('repeate_DO_Value', anonymous=True)
    global pub
    pub = rospy.Publisher('DO_Value', Float32, queue_size=10)
    rate = rospy.Rate(2)  # 设置发布频率为2Hz

    while not rospy.is_shutdown() and not shutdown_event.is_set():
        if not data_queue.empty():
            DO = data_queue.get()
            pub.publish(DO)
        rate.sleep()

def shutdown_hook():
    rospy.loginfo("关闭中...")
    shutdown_event.set()

if __name__ == '__main__':
    rospy.init_node('do_publisher', anonymous=True)
    rospy.on_shutdown(shutdown_hook)

    try:

        serial_thread = threading.Thread(target=serial_communication)
        csv_thread = threading.Thread(target=save_to_csv)
        ros_thread = threading.Thread(target=ros_publisher)

        serial_thread.start()
        csv_thread.start()
        ros_thread.start()

        serial_thread.join()
        csv_thread.join()
        ros_thread.join()

    except rospy.ROSInterruptException:
        pass
