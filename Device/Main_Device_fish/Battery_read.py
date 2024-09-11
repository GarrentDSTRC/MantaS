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
start_register_relay = 0x00  # 根据实际设备地址调整
start_register_SOC = 0x06   # 根据实际设备地址调整
start_register_work = 0x05   # 根据实际设备地址调整

try:
    while True:
        relay_status = read_register(address, start_register_relay)
        soc_status = read_register(address, start_register_SOC)
        work_status = read_register(address, start_register_work)

        # 打印结果和错误检查
        if relay_status is not None:
            print(f"Relay status: {relay_status}")
        else:
            print("No relay status received or CRC error.")

        if soc_status is not None:
            soc_percentage = get_soc_percentage(soc_status)
            print(f"SOC status: {soc_percentage:.1f}%")
        else:
            print("No SOC status received or CRC error.")

        if work_status is not None:
            current_status = get_current_status(work_status)
            print(f"Work status: {work_status} ({current_status})")
        else:
            print("No work status received or CRC error.")

        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")

finally:
    ser.close()
