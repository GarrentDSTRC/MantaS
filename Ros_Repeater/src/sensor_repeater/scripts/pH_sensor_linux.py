import serial
import csv
import time

# 配置串口
ser = serial.Serial(
    port='/dev/ttyUSB0',         # 根据实际情况修改
    baudrate=9600,       # 波特率
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1            # 读取超时
)

def read_ph_voltage():
    # 发送读取命令
    ser.write(b'\x01\x03\x00\x00\x00\x02\xc4\x0b')
    time.sleep(0.5)
    response = ser.read(9)
    if len(response) == 9:
        # 解析响应
        ad_value = int.from_bytes(response[3:5], byteorder='big')
        voltage = ad_value / 4095 * 5  # 转换为电压
        return voltage
    else:
        return None

def calculate_a1(T, a1_20, k):
    # 计算 a1(T)
    return a1_20 + (T - 20) * k

def calculate_ph(voltage, a1_T, a0):
    # 使用公式计算pH值
    return a1_T * voltage + a0

def main():
    # 根据实际情况设置校准参数
    a1_20 = 0.017  # 示例值，从校准报告中获得
    a0 = 7.0       # 示例值，从校准报告中获得
    k = 0.001      # 示例值，温度补偿系数，需要从校准报告或实验确定
    temperature = 25  # 实际测量温度，假设为25℃

    with open('ph_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Voltage (V)', 'pH'])

        while True:
            voltage = read_ph_voltage()
            if voltage is not None:
                a1_T = calculate_a1(temperature, a1_20, k)
                ph = calculate_ph(voltage, a1_T, a0)
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([timestamp, voltage, ph])
                print(f'Time: {timestamp}, Voltage: {voltage:.3f} V, pH: {ph:.2f}')
            else:
                print('Failed to read from sensor')
            
            time.sleep(1)  # 每秒读取一次

if __name__ == '__main__':
    main()
