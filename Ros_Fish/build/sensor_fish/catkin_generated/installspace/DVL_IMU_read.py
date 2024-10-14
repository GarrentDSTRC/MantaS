#!/usr/bin/env python3

import rospy
import serial
import struct
import csv
import time
import threading
from sensor_fish.msg import DVLData
from queue import Queue

# 串口配置
port = '/dev/ttyUSB0'
baudrate = 460800

# 打开串口
ser = serial.Serial(port, baudrate, timeout=1)

# CSV文件配置
csv_file = 'DVL_data.csv'
csv_columns = [
    'Frame Count', 'Week', 'Week Seconds', 'Heading', 'Pitch', 'Roll',
    'East Velocity', 'North Velocity', 'Up Velocity', 'Latitude', 'Longitude',
    'Altitude', 'X Angular Velocity', 'Y Angular Velocity', 'Z Angular Velocity',
    'X Acceleration', 'Y Acceleration', 'Z Acceleration', 'Primary Satellite Count',
    'Secondary Satellite Count', 'Navigation Status', 'GNSS Status', 'Fault Status',
    'DVL Height', 'DVL Velocity'
]

# 写入CSV文件头
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

shutdown_event = threading.Event()
data_queue = Queue()

def parse_data(data):
    if len(data) < 94:
        print(f"Data length is too short: {len(data)}")
        return None
    
    parsed_data = {}
    parsed_data['Frame Count'], = struct.unpack('<H', data[6:8])
    parsed_data['Week'], = struct.unpack('<H', data[8:10])
    parsed_data['Week Seconds'], = struct.unpack('<d', data[10:18])
    parsed_data['Heading'], = struct.unpack('<i', data[18:22])
    parsed_data['Pitch'], = struct.unpack('<i', data[22:26])
    parsed_data['Roll'], = struct.unpack('<i', data[26:30])
    parsed_data['East Velocity'], = struct.unpack('<i', data[30:34])
    parsed_data['North Velocity'], = struct.unpack('<i', data[34:38])
    parsed_data['Up Velocity'], = struct.unpack('<i', data[38:42])
    parsed_data['Latitude'], = struct.unpack('<i', data[42:46])
    parsed_data['Longitude'], = struct.unpack('<i', data[46:50])
    parsed_data['Altitude'], = struct.unpack('<i', data[50:54])
    parsed_data['X Angular Velocity'], = struct.unpack('<i', data[54:58])
    parsed_data['Y Angular Velocity'], = struct.unpack('<i', data[58:62])
    parsed_data['Z Angular Velocity'], = struct.unpack('<i', data[62:66])
    parsed_data['X Acceleration'], = struct.unpack('<i', data[66:70])
    parsed_data['Y Acceleration'], = struct.unpack('<i', data[70:74])
    parsed_data['Z Acceleration'], = struct.unpack('<i', data[74:78])
    parsed_data['Primary Satellite Count'], = struct.unpack('<B', data[78:79])
    parsed_data['Secondary Satellite Count'], = struct.unpack('<B', data[79:80])
    parsed_data['Navigation Status'], = struct.unpack('<B', data[80:81])
    parsed_data['GNSS Status'], = struct.unpack('<H', data[81:83])
    parsed_data['Fault Status'], = struct.unpack('<H', data[83:85])
    parsed_data['DVL Height'], = struct.unpack('<f', data[85:89])
    parsed_data['DVL Velocity'], = struct.unpack('<f', data[89:93])

    # 转换数据格式
    parsed_data['Heading'] *= 0.0001
    parsed_data['Pitch'] *= 0.0001
    parsed_data['Roll'] *= 0.0001
    parsed_data['East Velocity'] *= 0.0001
    parsed_data['North Velocity'] *= 0.0001
    parsed_data['Up Velocity'] *= 0.0001
    parsed_data['Latitude'] *= 0.0000001
    parsed_data['Longitude'] *= 0.0000001
    parsed_data['Altitude'] *= 0.0001
    parsed_data['X Angular Velocity'] *= 0.000001
    parsed_data['Y Angular Velocity'] *= 0.000001
    parsed_data['Z Angular Velocity'] *= 0.000001
    parsed_data['X Acceleration'] *= 0.000001
    parsed_data['Y Acceleration'] *= 0.000001
    parsed_data['Z Acceleration'] *= 0.000001

    return parsed_data

# 找到同步头
def find_sync():
    while not rospy.is_shutdown() and not shutdown_event.is_set():
        byte = ser.read(1)
        if byte == b'\x55':
            next_byte = ser.read(1)
            if next_byte == b'\xAA':
                # 已找到同步头
                return

def publish_data(parsed_data):
    dvl_data = DVLData()
    dvl_data.heading = parsed_data['Heading']
    dvl_data.pitch = parsed_data['Pitch']
    dvl_data.roll = parsed_data['Roll']
    dvl_data.dvl_height = parsed_data['DVL Height']
    dvl_data.dvl_velocity = parsed_data['DVL Velocity']
    dvl_data.stat_byte = parsed_data['Navigation Status']
    dvl_data.latitude = parsed_data['Latitude']
    dvl_data.longitude = parsed_data['Longitude']
    dvl_data.altitude = parsed_data['Altitude']
    dvl_pub.publish(dvl_data)

def csv_writer_thread(queue):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        while not rospy.is_shutdown() and not shutdown_event.is_set():
            if not queue.empty():
                data = queue.get()
                writer.writerow(data)
        rospy.sleep(0.1)

def serial_reader():
    while not rospy.is_shutdown() and not shutdown_event.is_set():
        find_sync()
        data = ser.read(92)
        data = b'\x55\xAA' + data
        if len(data) == 94:
            parsed_data = parse_data(data)
            if parsed_data:
                data_queue.put(parsed_data)
                publish_data(parsed_data)
                rospy.loginfo(f"Data published: {parsed_data}")
            else:
                rospy.logwarn("Parsed data is None.")
        else:
            rospy.logwarn(f"Read data length mismatch: {len(data)}")
        rospy.sleep(0.01)

def shutdown_hook():
    rospy.loginfo("关闭中...")
    shutdown_event.set()

def main():
    rospy.init_node('dvl_publisher')
    global dvl_pub
    dvl_pub = rospy.Publisher('dvl/data', DVLData, queue_size=10)
    rospy.on_shutdown(shutdown_hook)

    csv_thread = threading.Thread(target=csv_writer_thread, args=(data_queue,))
    serial_thread = threading.Thread(target=serial_reader)

    csv_thread.start()
    serial_thread.start()

    csv_thread.join()
    serial_thread.join()

if __name__ == '__main__':
    main()
