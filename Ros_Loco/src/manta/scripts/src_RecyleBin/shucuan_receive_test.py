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

class ThrusterReceiver:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        if not self.ser.is_open:
            self.ser.open()

    def _parse_data_frame(self, data_frame):
        # 数据帧格式: [帧头(0x03)][数据][校验和][帧尾(0x27)]
        if data_frame[0] != 0x03 or data_frame[-1] != 0x27:
            raise ValueError("Invalid frame format")

        data = data_frame[1:13]
        received_crc = (data_frame[13] << 8) | data_frame[14]
        calculated_crc = crc16(data)

        if received_crc != calculated_crc:
            raise ValueError("CRC check failed")

        control_signals = []
        for i in range(0, 12, 2):
            signal = int.from_bytes(data[i:i+2], byteorder='big', signed=True)
            control_signals.append(signal)
        
        return control_signals

    def receive_control_signals(self):
        data_frame = bytearray(16)  # 数据帧长度为16字节
        while True:
            self.ser.readinto(data_frame)
            try:
                control_signals = self._parse_data_frame(data_frame)
                print("接收到的控制信号:", control_signals)
            except ValueError as e:
                print(f"Error: {e}")

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    port = '/dev/ttyUSB0'  # 根据实际情况调整串口端口
    receiver = ThrusterReceiver(port)
    
    try:
        receiver.receive_control_signals()
    except KeyboardInterrupt:
        print("终止接收")
    finally:
        receiver.close()
