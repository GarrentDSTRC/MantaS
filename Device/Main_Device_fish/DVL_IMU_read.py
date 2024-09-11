import serial
import struct
import csv
import time

# 串口配置
port = 'COM3'
baudrate = 460800

# 打开串口
ser = serial.Serial(port, baudrate, timeout=1)

# CSV文件配置
csv_file = 'data.csv'
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
    while True:
        byte = ser.read(1)
        if byte == b'\x55':
            next_byte = ser.read(1)
            if next_byte == b'\xAA':
                # 已找到同步头
                return

# 循环读取数据并保存到CSV文件
try:
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        while True:
            # 寻找同步头
            find_sync()
            # 读取剩余的92个字节
            data = ser.read(92)
            # 加上同步头
            data = b'\x55\xAA' + data
            if len(data) == 94:
                parsed_data = parse_data(data)
                if parsed_data:
                    writer.writerow(parsed_data)
                    print(f"Data saved: {parsed_data}")
            else:
                print(f"Read data length mismatch: {len(data)}")
            time.sleep(0.01)  # 控制读取频率
except KeyboardInterrupt:
    print("Data collection stopped by user.")
