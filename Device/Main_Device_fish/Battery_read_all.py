import serial
import time
import crcmod

# 定义串行通信参数
SERIAL_PORT = '/dev/ttyUSB0'  # 根据实际情况调整串行端口
BAUD_RATE = 9600
BYTESIZE = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE

# 打开串行端口
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, bytesize=BYTESIZE, parity=PARITY, stopbits=STOPBITS, timeout=1)

if ser.isOpen():
    print(f"{SERIAL_PORT} is opened.")

# 定义CRC16校验函数
modbus_crc16 = crcmod.predefined.mkCrcFun('modbus')

# 构建Modbus RTU请求包
def build_request(address, function_code, start_register, quantity):
    data = bytearray([address, function_code, start_register >> 8, start_register & 0xFF, quantity >> 8, quantity & 0xFF])
    crc = modbus_crc16(data)
    request = data + bytes([crc & 0xFF, crc >> 8])
    return request

# 发送请求并接收响应
def send_request(request):
    ser.write(request)
    time.sleep(0.1)  # 等待响应
    response = ser.read(ser.inWaiting())
    return response

# 解析响应数据
def parse_response(response):
    if len(response) < 5:
        print("Response too short")
        return None
    device_address = response[0]
    function_code = response[1]
    byte_count = response[2]
    register_values = response[3:3 + byte_count]
    crc_received = int.from_bytes(response[-2:], byteorder='little')
    return device_address, function_code, register_values, crc_received

# 验证CRC校验码
def verify_crc(data):
    calculated_crc = modbus_crc16(data[:-2])
    crc_from_response = int.from_bytes(data[-2:], byteorder='little')
    return calculated_crc == crc_from_response

# 读取寄存器值
def read_register(address, start_register, function_code=0x03):
    quantity = 1
    request = build_request(address, function_code, start_register, quantity)
    response = send_request(request)
    if not response:
        print("No response received")
        return None
    if not verify_crc(response):
        print("CRC check failed")
        return None
    parsed_response = parse_response(response)
    if not parsed_response:
        print("Failed to parse response")
        return None
    device_address, function_code, register_values, crc_received = parsed_response
    if len(register_values) != 2:
        print(f"Unexpected register value length: {len(register_values)}")
        return None
    register_value = int.from_bytes(register_values, byteorder='big', signed=True)
    return register_value

# 解析继电器状态
def parse_relay_status(relay_status):
    status = {
        "正极继电器": (relay_status & 0x01) != 0,
        "负极继电器": (relay_status & 0x02) != 0,
        "充电继电器": (relay_status & 0x04) != 0,
        "放电继电器": (relay_status & 0x08) != 0,
        "预充继电器": (relay_status & 0x10) != 0,
        "加热继电器": (relay_status & 0x20) != 0
    }
    return status

# 解析电压值
def parse_voltage(voltage_raw):
    return voltage_raw * 0.1  # 分辨率是0.1V/bit

# 解析电流值
def parse_current(current_raw):
    return current_raw * 0.1 - 1500  # 分辨率是0.1A/bit，偏移量是-1500A

# 解析温度值
def parse_temperature(temp_raw):
    return temp_raw - 40  # 分辨率是1℃/bit，偏移量是-40℃

# 解析单体电压值
def parse_single_voltage(single_voltage_raw):
    return single_voltage_raw * 0.001  # 分辨率是1mV/bit

# 解析状态码
def parse_status_code(status_code):
    status_dict = {
        0x00: "无告警",
        0x01: "一级故障",
        0x02: "二级故障",
        0x03: "三级故障"
    }
    return status_dict.get(status_code, "未知状态")

# 根据电流值返回状态
def get_current_status(current):
    if current >= 3000:
        return "放电状态 (0x01)"
    elif current <= -3000:
        return "充电状态 (0x02)"
    elif -3000 < current < 3000:
        return "搁置状态 (0x03)"
    return "未知状态"

# 解析SOC值
def get_soc_percentage(raw_soc):
    return raw_soc * 0.1  # 分辨率是0.1%/bit

# 设备地址和寄存器起始地址
address = 0x01

register_map = {
    "继电器状态": 0x0001,
    "总电压": 0x0002,
    "正半簇电流": 0x0003,
    "负半簇电流": 0x0004,
    "系统工作状态": 0x0005,
    "SOC": 0x0006,
    "SOH": 0x0007,
    "电池组串数": 0x0008,
    "电池组温度采集点数量": 0x0009,
    "最高单体电压": 0x000A,
    "最高单体电压位置": 0x000B,
    "最高单体温度": 0x000C,
    "最高单体温度位置": 0x000D,
    "瞬时最大放电电流": 0x000E,
    "瞬时最大充电电流": 0x000F,
    "持续最大放电电流": 0x0010,
    "持续最大充电电流": 0x0011,
    "最低单体电压": 0x0012,
    "最低单体电压位置": 0x0013,
    "最低单体温度": 0x0014,
    "最低单体温度位置": 0x0015,
}

try:
    while True:
        relay_status = read_register(address, register_map["继电器状态"])
        total_voltage = read_register(address, register_map["总电压"])
        positive_current = read_register(address, register_map["正半簇电流"])
        negative_current = read_register(address, register_map["负半簇电流"])
        work_status = read_register(address, register_map["系统工作状态"])
        soc = read_register(address, register_map["SOC"])
        soh = read_register(address, register_map["SOH"])

        # 打印结果和错误检查
        if relay_status is not None:
            relay_status_parsed = parse_relay_status(relay_status)
            print(f"继电器状态: {relay_status_parsed}")
        else:
            print("No relay status received or CRC error.")

        if total_voltage is not None:
            total_voltage_parsed = parse_voltage(total_voltage)
            print(f"总电压: {total_voltage_parsed:.1f}V")
        else:
            print("No total voltage received or CRC error.")

        if positive_current is not None:
            positive_current_parsed = parse_current(positive_current)
            print(f"正半簇电流: {positive_current_parsed:.1f}A")
        else:
            print("No positive current received or CRC error.")

        if negative_current is not None:
            negative_current_parsed = parse_current(negative_current)
            print(f"负半簇电流: {negative_current_parsed:.1f}A")
        else:
            print("No negative current received or CRC error.")

        if work_status is not None:
            current_status = get_current_status(work_status)
            print(f"系统工作状态: {work_status} ({current_status})")
        else:
            print("No work status received or CRC error.")

        if soc is not None:
            soc_percentage = get_soc_percentage(soc)
            print(f"SOC: {soc_percentage:.1f}%")
        else:
            print("No SOC received or CRC error.")

        if soh is not None:
            soh_percentage = get_soc_percentage(soh)
            print(f"SOH: {soh_percentage:.1f}%")
        else:
            print("No SOH received or CRC error.")

        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")

finally:
    ser.close()
