#!/usr/bin/env python

import rospy
from sensor_repeater.msg import CTD
import serial
import csv
import os
import threading
from queue import Queue

# 配置串口
ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=1) 

data_queue = Queue()
shutdown_event = threading.Event()

def parse_data(data):
    try:
        # 按协议格式解析数据
        parts = data.strip().split(',')
        temperature = float(parts[0].split('=')[1])
        pressure = float(parts[1].split('=')[1])
        conductivity = float(parts[2].split('=')[1].strip(';'))
        return temperature, pressure, conductivity
    except Exception as e:
        rospy.logerr(f"解析数据时出错: {e}")
        return None

def save_to_csv(filename='ctd_value.csv'):
    # 初始化CSV文件
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Temperature (℃)', 'Pressure (dbar)', 'Conductivity (mS/cm)'])
    
    while not rospy.is_shutdown() and not shutdown_event.is_set():
        if not data_queue.empty():
            temperature, pressure, conductivity = data_queue.get()
            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([temperature, pressure, conductivity])
                rospy.loginfo(f"已保存: 温度={temperature}℃, 压力={pressure} dbar, 电导率={conductivity} mS/cm")
        rospy.sleep(0.1)

def ros_publisher():
    ctd_pub = rospy.Publisher('ctd_data', CTD, queue_size=10)
    rate = rospy.Rate(1)  # 设置发布频率为1Hz

    while not rospy.is_shutdown() and not shutdown_event.is_set():
        if not data_queue.empty():
            temperature, pressure, conductivity = data_queue.get()
            
            # 创建自定义消息并发布
            ctd_msg = CTD()
            ctd_msg.temperature = temperature
            ctd_msg.pressure = pressure
            ctd_msg.conductivity = conductivity
            ctd_pub.publish(ctd_msg)
        
        rate.sleep()

def serial_reader():
    while not rospy.is_shutdown() and not shutdown_event.is_set():
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8')
            rospy.loginfo(f"接收到数据: {raw_data}")
            parsed_data = parse_data(raw_data)
            if parsed_data:
                data_queue.put(parsed_data)
        rospy.sleep(0.1)

def shutdown_hook():
    rospy.loginfo("关闭中...")
    shutdown_event.set()

if __name__ == "__main__":
    rospy.init_node('ctd_publisher', anonymous=True)
    rospy.on_shutdown(shutdown_hook)

    try:
        # 创建并启动线程
        reader_thread = threading.Thread(target=serial_reader)
        csv_thread = threading.Thread(target=save_to_csv)
        pub_thread = threading.Thread(target=ros_publisher)

        reader_thread.start()
        csv_thread.start()
        pub_thread.start()

        reader_thread.join()
        csv_thread.join()
        pub_thread.join()
    except rospy.ROSInterruptException:
        pass
