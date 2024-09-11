import serial
import time
import string
import pandas as pd
from datetime import datetime
import threading
import rospy
from sensor_fish.msg import Warmdepth  # 导入自定义消息类型

result = ""
df = pd.DataFrame(columns=["Time", "Type", "Height", "Temp", "Depth", "Pressure"])
data_queue = []  # 用于存储每秒的同步数据
Com485_Sensor = None
stop_threads = False  # 停止标志

def load_params():
    global Com485_Sensor
    serial_port = '/dev/ttyUSB1'  # 根据你的设置调整
    baud_rate = 9600  # 根据你的设置调整
    Com485_Sensor = serial.Serial(serial_port, baud_rate, timeout=1)

def Get485_Info_Altitude_Sensor(data):
    global result 
    global df
    global data_queue
    if data[0] == "$ISADS":  # 高度传感器: 温度、高度状态
        height = float(data[1])
        temp = float(data[3])
        result = "{}, {}".format(height, temp)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        df.loc[len(df)] = [current_time, "Altitude", height, temp, None, None]
        data_queue.append({"time": current_time, "height": height, "temp": temp})
        print('height status :  %s' % result)

def Get485_Info__Depth_Temperature_Sensor(data):
    global result 
    global df
    global data_queue
    if data[0] == "$ISDPT":  # 深度和温度传感器
        depth = float(data[1])
        pressure = float(data[3])
        temp = float(data[5])
        result = "{}, {}, {}".format(depth, pressure, temp)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        df.loc[len(df)] = [current_time, "Depth", None, temp, depth, pressure]
        data_queue.append({"time": current_time, "depth": depth, "pressure": pressure})
        print('temperature and depth status :  %s' % result)

def Get_All_Data_from_485(OriginalData):
    global result 
    try:
        temp = str(OriginalData, encoding="ISO-8859-1")
        if any(char not in string.printable for char in temp):  # 过滤掉不可打印字符
            return
        data = temp.split(',')
        if data[0] == "$ISADS":  # 高度传感器: 温度、高度状态
            Get485_Info_Altitude_Sensor(data)
        if data[0] == "$ISDPT":  # 深度和温度传感器
            Get485_Info__Depth_Temperature_Sensor(data)
    except Exception as e:  # 处理异常，通常由多个设备的电磁干扰引起
        print(e)

def Send_Request_and_Read_Response(request):
    global stop_threads
    while not rospy.is_shutdown() and not stop_threads:
        Com485_Sensor.write(request.encode())
        time.sleep(0.001)  # 根据传感器响应时间调整睡眠时间
        Original_Data = Com485_Sensor.readline()
        if len(Original_Data) > 0 and Original_Data[0] == 36:  # 36是'$'的ASCII码
            Get_All_Data_from_485(Original_Data)

def Save_Data_To_CSV():
    global df
    global stop_threads
    while not rospy.is_shutdown() and not stop_threads:
        try:
            df.to_csv("data_log.csv", index=False)
        except Exception as e:
            print("Error while saving data to CSV:", e)
        finally:
            time.sleep(1)  

def Process_And_Send_Data(pub):
    global data_queue
    global stop_threads
    rate = rospy.Rate(5) 
    while not rospy.is_shutdown() and not stop_threads:
        if data_queue:
            synchronized_data = {}
            for data in data_queue:
                if "height" in data and "depth" in data:
                    synchronized_data = data
                    break
                elif "height" in data:
                    synchronized_data.update({"height": data["height"], "temp": data["temp"]})
                elif "depth" in data:
                    synchronized_data.update({"depth": data["depth"], "pressure": data["pressure"]})
            
            if synchronized_data:
                sensor_data_msg = Warmdepth()
                sensor_data_msg.time = synchronized_data.get("time", "")
                sensor_data_msg.height = synchronized_data.get("height", 0.0)
                sensor_data_msg.temp = synchronized_data.get("temp", 0.0)
                sensor_data_msg.depth = synchronized_data.get("depth", 0.0)
                sensor_data_msg.pressure = synchronized_data.get("pressure", 0.0)
                rospy.loginfo(sensor_data_msg)
                pub.publish(sensor_data_msg)
                data_queue = []  # 清空队列
            
        rate.sleep()

def main():
    global stop_threads
    load_params()
    rospy.init_node('sensor_data_publisher', anonymous=True)
    pub = rospy.Publisher('sensor_data', Warmdepth, queue_size=10)
    
    save_thread = threading.Thread(target=Save_Data_To_CSV)
    save_thread.daemon = True  # 守护线程
    save_thread.start()

    process_thread = threading.Thread(target=Process_And_Send_Data, args=(pub,))
    process_thread.daemon = True  # 守护线程
    process_thread.start()
    
    start_time = time.time()
    data_count = 0
    try:
        while not rospy.is_shutdown():
            # 请求高度传感器数据
            Send_Request_and_Read_Response("$ISADS\n")  
            # 请求深度和温度传感器数据
            Send_Request_and_Read_Response("$ISDPT\n")  
            # 每秒计算并打印数据传输频率
            data_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                print(f"Data transfer frequency: {data_count} messages per second")
                data_count = 0
                start_time = time.time()
    except rospy.ROSInterruptException:
        stop_threads = True

if __name__ == '__main__':
    main()
