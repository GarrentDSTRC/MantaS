import serial
import time
import string
import pandas as pd
from datetime import datetime
import threading

result = ""
df = pd.DataFrame(columns=["Time", "Type", "Value1", "Value2", "Value3"])

def load_params():
    global Com485_Sensor
    serial_port = '/dev/ttyUSB0'  # Adjust this based on your setup
    baud_rate = 9600  # Adjust this based on your setup
    Com485_Sensor = serial.Serial(serial_port, baud_rate, timeout=1)

def Get485_Info_Altitude_Sensor(data):
    global result 
    global df
    if data[0] == "$ISADS":  # Altitude sensor: temperature, altitude status
        height = data[1]
        temp = data[3] 
        result = "{}, {}".format(height, temp)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        df.loc[len(df)] = [current_time, "Altitude", height, temp, ""]
        print('height status :  %s' % result)

def Get485_Info__Depth_Temperature_Sensor(data):
    global result 
    if data[0] == "$ISDPT":  # Depth and temperature sensor
        depth = data[1]
        pressure = data[3]
        temp = data[5]
        result = "{}, {}, {}".format(depth, pressure, temp)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        df.loc[len(df)] = [current_time, "Depth", depth, pressure, temp]
        print('temperature and depth status :  %s' % result)

def Get_All_Data_from_485(OriginalData):
    global result 
    try:
        temp = str(OriginalData, encoding = "ISO-8859-1")
        if any(char not in string.printable for char in temp):  # Filter out non-printable characters
            return
        data = temp.split(',')
        if data[0] == "$ISADS":  # Altitude sensor: temperature, altitude status
            Get485_Info_Altitude_Sensor(data)
        if data[0] == "$ISDPT":  # Depth and temperature sensor
            Get485_Info__Depth_Temperature_Sensor(data)
    except Exception as e:  # Handle exceptions, usually caused by electromagnetic interference from multiple devices
        print(e)

def Send_Request_and_Read_Response(request):
    Com485_Sensor.write(request.encode())
    time.sleep(0.001)  # Adjust sleep time based on sensor response time
    Original_Data = Com485_Sensor.readline()
    if len(Original_Data) > 0 and Original_Data[0] == 36:  # 36 is the ASCII code for '$'
        Get_All_Data_from_485(Original_Data)

def Save_Data_To_CSV():
    global df
    while True:
        try:
            df.to_csv("data_log.csv", index=False)
        except Exception as e:
            print("Error while saving data to CSV:", e)
        finally:
            time.sleep(1)  # Save data every minute

def Start():
    load_params()
    start_time = time.time()
    data_count = 0
    # Start a thread to save data periodically
    save_thread = threading.Thread(target=Save_Data_To_CSV)
    save_thread.daemon = True  # Daemonize thread
    save_thread.start()
    
    while True:
        # Request altitude sensor data
        Send_Request_and_Read_Response("$ISADS\n")  
        # Request depth and temperature sensor data
        Send_Request_and_Read_Response("$ISDPT\n")  
        # Count data and print frequency every second
        data_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1:
            print(f"Data transfer frequency: {data_count} messages per second")
            data_count = 0
            start_time = time.time()

if __name__ == '__main__':
    Start()
