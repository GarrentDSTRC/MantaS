import serial
import time
import string
import pandas as pd
from datetime import datetime
import threading
import rospy
from sensor_fish.msg import Warmdepth

df_depth = pd.DataFrame(columns=["Time", "Type", "Temp", "Depth", "Pressure"])
data_queue_depth = []  # 用于存储每秒的同步数据
Com485_Depth_Sensor = None
stop_threads_depth = False  # 停止标志

def load_params_depth():
    global Com485_Depth_Sensor
    serial_port = '/dev/ttyUSB1'  # 根据你的设置调整
    baud_rate = 9600  # 根据你的设置调整
    Com485_Depth_Sensor = serial.Serial(serial_port, baud_rate, timeout=1)
    print("串口打开成功")

def Get485_Info__Depth_Temperature_Sensor(data):
    global df_depth
    global data_queue_depth
    if data[0] == "$ISDPT":  # 深度和温度传感器
        depth = float(data[1])
        pressure = float(data[3])
        temp = float(data[5])
        result = "{}, {}, {}".format(depth, pressure, temp)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        df_depth.loc[len(df_depth)] = [current_time, "Depth", temp, depth, pressure]
        data_queue_depth.append({"time": current_time, "depth": depth, "pressure": pressure, "temp": temp})
        print('temperature and depth status :  %s' % result)

def Get_All_Data_from_485_Depth(OriginalData):
    try:
        temp = str(OriginalData, encoding="ISO-8859-1")
        if any(char not in string.printable for char in temp):  # 过滤掉不可打印字符
            return
        data = temp.split(',')
        if data[0] == "$ISDPT":  # 深度和温度传感器
            Get485_Info__Depth_Temperature_Sensor(data)
    except Exception as e:  # 处理异常，通常由多个设备的电磁干扰引起
        print(e)

def Read_Response_From_485_Depth():
    global stop_threads_depth
    while not rospy.is_shutdown() and not stop_threads_depth:
        try:
            Original_Data = Com485_Depth_Sensor.readline()
            if len(Original_Data) > 0 and Original_Data[0] == 36:  # 36是'$'的ASCII码
                Get_All_Data_from_485_Depth(Original_Data)
        except Exception as e:
            print("Error in Read_Response_From_485_Depth:", e)

def Save_Data_To_CSV_Depth():
    global df_depth
    global stop_threads_depth
    while not rospy.is_shutdown() and not stop_threads_depth:
        try:
            df_depth.to_csv("depth_data_log.csv", index=False)
        except Exception as e:
            print("Error while saving depth data to CSV:", e)
        finally:
            time.sleep(0.01)

def Process_And_Send_Data_Depth(pub):
    global data_queue_depth
    global stop_threads_depth
    rate = rospy.Rate(100)
    while not rospy.is_shutdown() and not stop_threads_depth:
        if data_queue_depth:
            for data in data_queue_depth:
                sensor_data_msg = Warmdepth()
                sensor_data_msg.time = data.get("time", "")
                sensor_data_msg.height = 0.0
                sensor_data_msg.temp = data.get("temp", 0.0)
                sensor_data_msg.depth = data.get("depth", 0.0)
                sensor_data_msg.pressure = data.get("pressure", 0.0)
                rospy.loginfo(sensor_data_msg)
                pub.publish(sensor_data_msg)
            data_queue_depth = []  # 清空队列
        rate.sleep()

def main():
    global stop_threads_depth
    load_params_depth()
    rospy.init_node('depth_sensor_data_publisher', anonymous=True)
    pub = rospy.Publisher('depth_sensor_data', Warmdepth, queue_size=10)

    save_thread = threading.Thread(target=Save_Data_To_CSV_Depth)
    save_thread.daemon = True  # 守护线程
    save_thread.start()

    process_thread = threading.Thread(target=Process_And_Send_Data_Depth, args=(pub,))
    process_thread.daemon = True  # 守护线程
    process_thread.start()

    start_time = time.time()
    data_count = 0
    try:
        while not rospy.is_shutdown():
            Read_Response_From_485_Depth()
            data_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                print(f"Depth sensor data transfer frequency: {data_count} messages per second")
                data_count = 0
                start_time = time.time()
    except rospy.ROSInterruptException:
        stop_threads_depth = True

if __name__ == '__main__':
    main()
