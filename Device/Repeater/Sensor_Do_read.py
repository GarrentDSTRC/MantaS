import serial
import time
import math
import csv

# 定义串口通信参数
port = 'COM8'
baudrate = 9600
timeout = 1

# 定义公式中的常数
c1 = -0.029
c2 = 0.000115
T = 25  # 假设的温度值，您需要根据实际情况设置
Pressure = 1  # 假设的压力值，您需要根据实际情况设置

# CSV文件名
csv_filename = 'DO_values.csv'

# 尝试打开串口
try:
    ser = serial.Serial(port, baudrate, timeout=timeout)
    print(f"串口 {port} 已打开。")

    # 定义要发送的固定数据
    fixed_command = bytes.fromhex("01 03 00 00 00 02 c4 0b")

    # 打开CSV文件，准备写入
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # 写入标题行（如果需要）
        csvwriter.writerow(['Timestamp', 'DO Value'])

        # 发送数据并解析接收到的数据
        while True:
            ser.write(fixed_command)  # 发送数据
            # print("指令发送完成")

            # 等待一段时间，确保数据发送完成
            time.sleep(0.1)

            # 读取串口数据
            if ser.in_waiting > 0:
                received_data = ser.read(ser.in_waiting).hex().upper()
                # print("接收到的数据（十六进制）:", received_data)

                # 检查数据长度是否足够
                if len(received_data) >= 14:
                    data_value1_hex = received_data[10:14]
                    o1 = int(data_value1_hex, 16)  # 将十六进制的数据值1转换为十进制
                    O1 = o1 * (5/4096)
                    # print("空气中电压值:", O1)
                    # 计算DO值
                    DO = (O1 - 0.002) * math.exp((T * c1 + Pressure * c2)) * 100 / (math.exp((T * c1)) * 3.49)
                    print("计算得到的DO值:", DO)

                    # 将当前时间戳和DO值写入CSV文件
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    csvwriter.writerow([timestamp, DO])

                else:
                    print("接收到的数据长度不足,无法解析数据值1")

            # 等待0.5秒再次发送数据
            time.sleep(0.5)

except serial.SerialException as e:
    print("串口通信错误:", e)

except KeyboardInterrupt:  # 允许使用Ctrl+C中断程序
    print("程序被用户中断")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()  # 关闭串口
        print("串口已关闭")