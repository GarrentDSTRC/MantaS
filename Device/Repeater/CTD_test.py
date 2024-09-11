import serial
import csv
import os

# 配置串口
ser = serial.Serial('com20', 9600, timeout=1)  # 修改为您使用的串口名称

def parse_data(data):
    try:
        # 按协议格式解析数据
        parts = data.strip().split(',')
        temperature = float(parts[0].split('=')[1])
        pressure = float(parts[1].split('=')[1])
        conductivity = float(parts[2].split('=')[1].strip(';'))
        return temperature, pressure, conductivity
    except Exception as e:
        print(f"解析数据时出错: {e}")
        return None

def save_to_csv(temperature, pressure, conductivity, filename='data.csv'):
    # 如果文件不存在，先创建文件并写入标题
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Temperature (℃)', 'Pressure (dbar)', 'Conductivity (mS/cm)'])
    
    # 写入数据
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([temperature, pressure, conductivity])
        print(f"已保存: 温度={temperature}℃, 压力={pressure} dbar, 电导率={conductivity} mS/cm")

def main():
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8')
            print(f"接收到数据: {raw_data}")
            parsed_data = parse_data(raw_data)
            if parsed_data:
                save_to_csv(*parsed_data)

if __name__ == "__main__":
    main()
