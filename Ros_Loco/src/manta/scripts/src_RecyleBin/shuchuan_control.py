import serial
import time

def crc16(data: bytearray) -> int:
    """
    Calculate CRC-16-CCITT checksum for given data.
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
        crc &= 0xFFFF
    return crc

class ThrusterController:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        if not self.ser.is_open:
            self.ser.open()

    def _create_data_frame(self, control_signals):
        # 数据帧格式: [帧头(0x03)][数据][校验和][帧尾(0x27)]
        data_frame = bytearray(1 + 12 + 2 + 1)  # 帧头(1字节) + 数据(12字节) + 校验和(2字节) + 帧尾(1字节)
        data_frame[0] = 0x03  # 帧头
        
        # 填充数据部分
        for i, signal in enumerate(control_signals):
            data_frame[1 + 2 * i: 3 + 2 * i] = signal.to_bytes(2, byteorder='big', signed=True)
        
        # 计算并填充校验和
        crc = crc16(data_frame[1:13])  # 计算数据部分的CRC
        data_frame[13] = (crc >> 8) & 0xFF  # CRC高字节
        data_frame[14] = crc & 0xFF  # CRC低字节

        data_frame[15] = 0x27  # 帧尾

        return data_frame

    def send_control_signals(self, control_signals):
        if len(control_signals) != 6:
            raise ValueError("控制信号的数量必须为6个")
        
        data_frame = self._create_data_frame(control_signals)
        self.ser.write(data_frame)
        return data_frame  # 返回数据帧用于模拟输出

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    # 使用示例
    port = '/dev/ttyUSB1'  # 根据实际情况调整串口端口
    controller = ThrusterController(port)
    
    try:
        while True:
            # 生成6个推进器的控制信号，这里假设为指定值
            # control_signals = [500, 500, 500, 500, 500, 500]
            control_signals = [0, 0, 0, 0, 0, 0]
            data_frame = controller.send_control_signals(control_signals)
            
            # 模拟输出数据帧内容
            print("发送的数据帧内容:", data_frame.hex())
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("终止控制")
    finally:
        controller.close()
