import serial
import time
import string
import pandas as pd
from datetime import datetime
import threading
import rospy
from sensor_fish.msg import Warmdepth

# Initialize global variables
df_altitude = pd.DataFrame(columns=["Time", "Type", "Height", "Temp"])
df_body_status = pd.DataFrame(columns=["Time", "Type", "Heading", "Pitch", "Roll"])
data_queue_altitude = []  # Queue for synchronized altitude sensor data
data_queue_body_status = []  # Queue for synchronized body status data
Com485_Altitude_Sensor = None
stop_threads_altitude = False  # Stop flag

def load_params_altitude():
    global Com485_Altitude_Sensor
    serial_port = '/dev/ttyUSB1'  # Adjust according to your settings
    baud_rate = 9600  # Adjust according to your settings
    Com485_Altitude_Sensor = serial.Serial(serial_port, baud_rate, timeout=1)
    print("Serial port opened successfully")

def Get485_Info_Altitude_Sensor(data):
    global df_altitude
    global df_body_status
    global data_queue_altitude
    global data_queue_body_status

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    if data[0] == "$ISADS":  # Altitude sensor: temperature, height status
        height = float(data[1])
        temp = float(data[3])
        result = "{}, {}".format(height, temp)
        df_altitude.loc[len(df_altitude)] = [current_time, "Altitude", height, temp]
        data_queue_altitude.append({"time": current_time, "height": height, "temp": temp})
        print('Height status :  %s' % result)

    elif data[0] == "$ISHPR":  # Body status: heading, pitch, roll
        heading = data[1]
        pitch = data[2]
        roll_f = data[3].split('*')
        roll = roll_f[0] 
        result = "{}, {}, {}, {}".format("ISHPR", heading, pitch, roll)
        df_body_status.loc[len(df_body_status)] = [current_time, "ISHPR", heading, pitch, roll]
        data_queue_body_status.append({"time": current_time, "heading": heading, "pitch": pitch, "roll": roll})
        print('Machine status :  %s' % result)

def Get_All_Data_from_485_Altitude(OriginalData):
    try:
        temp = str(OriginalData, encoding="ISO-8859-1")
        if any(char not in string.printable for char in temp):  # Filter out non-printable characters
            return
        data = temp.split(',')
        Get485_Info_Altitude_Sensor(data)
    except Exception as e:  # Handle exceptions, often caused by electromagnetic interference from multiple devices
        print(e)

def Read_Response_From_485_Altitude():
    global stop_threads_altitude
    while not rospy.is_shutdown() and not stop_threads_altitude:
        try:
            Original_Data = Com485_Altitude_Sensor.readline()
            if len(Original_Data) > 0 and Original_Data[0] == 36:  # 36 is ASCII code for '$'
                Get_All_Data_from_485_Altitude(Original_Data)
        except Exception as e:
            print("Error in Read_Response_From_485_Altitude:", e)

def Save_Data_To_CSV_Altitude():
    global df_altitude
    global df_body_status
    global stop_threads_altitude
    while not rospy.is_shutdown() and not stop_threads_altitude:
        try:
            df_altitude.to_csv("altitude_data_log.csv", index=False)
            df_body_status.to_csv("body_status_data_log.csv", index=False)
        except Exception as e:
            print("Error while saving data to CSV:", e)
        finally:
            time.sleep(0.01)
            
def Process_And_Send_Data_Altitude(pub_altitude, pub_body_status):
    global data_queue_altitude
    global data_queue_body_status
    global stop_threads_altitude
    rate = rospy.Rate(100)
    while not rospy.is_shutdown() and not stop_threads_altitude:
        if data_queue_altitude:
            for data in data_queue_altitude:
                sensor_data_msg = Warmdepth()
                sensor_data_msg.time = data.get("time", "")
                sensor_data_msg.height = data.get("height", 0.0)
                sensor_data_msg.temp = data.get("temp", 0.0)
                sensor_data_msg.depth = 0.0
                sensor_data_msg.pressure = 0.0
                sensor_data_msg.roll = 0.0
                sensor_data_msg.pitch = 0.0
                sensor_data_msg.yaw = 0.0
                rospy.loginfo(sensor_data_msg)
                pub_altitude.publish(sensor_data_msg)
            data_queue_altitude = []  # Clear the queue

        if data_queue_body_status:
            for data in data_queue_body_status:
                body_status_msg = Warmdepth()
                body_status_msg.time = data.get("time", "")
                body_status_msg.height = 0.0  # Not applicable for body status
                body_status_msg.temp = 0.0  # Not applicable for body status
                body_status_msg.depth = 0.0  # Not applicable for body status
                body_status_msg.pressure = 0.0  # Not applicable for body status
                body_status_msg.roll = float(data.get("roll", 0.0))
                body_status_msg.pitch = float(data.get("pitch", 0.0))
                body_status_msg.yaw = float(data.get("heading", 0.0))  # Assuming heading is yaw
                rospy.loginfo(body_status_msg)
                pub_body_status.publish(body_status_msg)
            data_queue_body_status = []  # Clear the queue

        rate.sleep()

def main():
    global stop_threads_altitude
    load_params_altitude()
    rospy.init_node('sensor_data_publisher', anonymous=True)
    
    pub_altitude = rospy.Publisher('altitude_sensor_data', Warmdepth, queue_size=10)
    pub_body_status = rospy.Publisher('body_status_data', Warmdepth, queue_size=10)

    save_thread = threading.Thread(target=Save_Data_To_CSV_Altitude)
    save_thread.daemon = True  # Daemon thread
    save_thread.start()

    process_thread = threading.Thread(target=Process_And_Send_Data_Altitude, args=(pub_altitude, pub_body_status,))
    process_thread.daemon = True  # Daemon thread
    process_thread.start()

    start_time = time.time()
    data_count = 0
    try:
        while not rospy.is_shutdown():
            Read_Response_From_485_Altitude()
            data_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                print(f"Sensor data transfer frequency: {data_count} messages per second")
                data_count = 0
                start_time = time.time()
    except rospy.ROSInterruptException:
        stop_threads_altitude = True

if __name__ == '__main__':
    main()
