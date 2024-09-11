from ctypes import *
import time

####################Can盒配置####################

class CANMotorController:
    VCI_USBCAN2 = 4
    STATUS_OK = 1

    class VCI_INIT_CONFIG(Structure):
        _fields_ = [("AccCode", c_uint),
                    ("AccMask", c_uint),
                    ("Reserved", c_uint),
                    ("Filter", c_ubyte),
                    ("Timing0", c_ubyte),
                    ("Timing1", c_ubyte),
                    ("Mode", c_ubyte)]

    class VCI_CAN_OBJ(Structure):
        _fields_ = [("ID", c_uint),
                    ("TimeStamp", c_uint),
                    ("TimeFlag", c_ubyte),
                    ("SendType", c_ubyte),
                    ("RemoteFlag", c_ubyte),
                    ("ExternFlag", c_ubyte),
                    ("DataLen", c_ubyte),
                    ("Data", c_ubyte * 8),
                    ("Reserved", c_ubyte * 3)]

    def __init__(self, motor_id):
        self.motor_id = motor_id

    def open_device(self):
        self.canDLL = cdll.LoadLibrary('./arm_libcontrolcan.so')
        ret = self.canDLL.VCI_OpenDevice(self.VCI_USBCAN2, 0, 0)
        if ret == self.STATUS_OK:
            print('调用 VCI_OpenDevice 成功')
        else:
            print(f'调用 VCI_OpenDevice 出错, 错误码: {ret}')
            exit()

    def init_can_channel(self):
        vci_initconfig = self.VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x1C, 0)  # 波特率500k，正常模式
        ret = self.canDLL.VCI_InitCAN(self.VCI_USBCAN2, 0, 0, byref(vci_initconfig))
        if ret == self.STATUS_OK:
            print('初始化通道0成功')
        else:
            print(f'初始化通道0出错, 错误码: {ret}')
            exit()

    def close_device(self):
        ret = self.canDLL.VCI_CloseDevice(self.VCI_USBCAN2, 0)
        if ret == self.STATUS_OK:
            print('关闭设备成功')
        else:
            print(f'关闭设备失败, 错误码: {ret}')

    def start_can_channel(self):
        ret = self.canDLL.VCI_StartCAN(self.VCI_USBCAN2, 0, 0)
        if ret == self.STATUS_OK:
            print('启动通道0成功')
        else:
            print(f'启动通道0出错, 错误码: {ret}')
            exit()
            
    def send_command(self, vci_can_obj):
        ret = self.canDLL.VCI_Transmit(self.VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
        if ret == self.STATUS_OK:
            print(f'命令发送成功: {list(vci_can_obj.Data)}')
        else:
            print(f'命令发送失败, 错误码: {ret}')

    def receive_data(self):
        ubyte_3array = c_ubyte * 3
        reserved_array = ubyte_3array(0, 0, 0)
        vci_can_obj = self.VCI_CAN_OBJ(0, 0, 0, 0, 0, 0, 0, (c_ubyte * 8)(0, 0, 0, 0, 0, 0, 0, 0), reserved_array)
        ret = self.canDLL.VCI_Receive(self.VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1, 0)
        if ret > 0:
            data = list(vci_can_obj.Data)
            print('接收到数据:', data)
            return data
        else:
            print('接收数据失败, 错误码:', ret)
            return None
        
####################舵机基础功能####################

    def set_motor_id(self, motor_id, new_id):
        data_array = (c_ubyte * 8)(0xC3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, new_id)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)

    def set_zero_point(self, motor_id):
        data_array = (c_ubyte * 8)(0xC4, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)
        self.receive_data()

    def set_max_angle(self, motor_id, angle, direction):
        angle_data = (angle + 180) * 100
        data_high = (angle_data >> 8) & 0xFF
        data_low = angle_data & 0xFF
        if direction == 'positive':
            command_byte = 0xC4
            data_byte = 0x03
        elif direction == 'negative':
            command_byte = 0xC4
            data_byte = 0x02
        else:
            raise ValueError("Direction must be 'positive' or 'negative'")
        data_array = (c_ubyte * 8)(command_byte, data_byte, 0x00, 0x00, 0x00, 0x00, data_high, data_low)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)

    def send_angle(self, motor_id, angle):
        angle_data = (angle + 180) * 100
        data_high = (angle_data >> 8) & 0xFF
        data_low = angle_data & 0xFF
        data_array = (c_ubyte * 8)(0xC1, 0x00, 0x00, 0x00, 0x00, 0x00, data_high, data_low)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)

    def send_stop_command(self, motor_id):
        data_array = (c_ubyte * 8)(0xC2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)

    def send_terminal_resistance_command(self, motor_id, enable):
        data_array = (c_ubyte * 8)(0xC5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01 if enable else 0x00)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)

    def set_baud_rate(self, motor_id, baud_rate):
        data_array = (c_ubyte * 8)(0xC7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, baud_rate)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)

    def set_feedback_interval(self, motor_id, interval_s):
        interval_high = (interval_s >> 8) & 0xFF
        interval_low = interval_s & 0xFF
        data_array = (c_ubyte * 8)(0xC8, 0x00, 0x00, 0x00, 0x00, 0x00, interval_high, interval_low)
        vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
        self.send_command(vci_can_obj)
    
    def parse_status_byte(self, status_data):
        byte4 = (status_data >> 8) & 0xFF  # Extracting the high byte
        byte5 = status_data & 0xFF         # Extracting the low byte

        status_flags = {
            "终端电阻": (byte4 >> 7) & 1,
            "堵转故障": (byte4 >> 6) & 1,
            "过流故障": (byte4 >> 5) & 1,
            "漏水故障": (byte4 >> 4) & 1,
            "停止状态": (byte4 >> 3) & 1,
            "舵角负向超限": (byte4 >> 1) & 1,
            "舵角正向超限": byte4 & 1,
            "未收到上位机指令": (byte5 >> 7) & 1,
            "指令错误": (byte5 >> 6) & 1,
            "驱动故障": (byte5 >> 5) & 1,
            "驱动过热": (byte5 >> 4) & 1,
            "旋变异常1": (byte5 >> 3) & 1,
            "旋变异常2": (byte5 >> 2) & 1,
            "过压/欠压": byte5 & 1
        }
        return status_flags

    def parse_received_data(self, data):
        if data:
            status_byte = (data[4] << 8) | data[5]  # Combine the high and low bytes
            angle_high = data[6]
            angle_low = data[7]
            angle = ((angle_high << 8) | angle_low) / 100 - 180
            status = self.parse_status_byte(status_byte)
            print(f'状态字节: {status_byte}, 角度: {angle:.2f}度')
            print(f'状态解析: {status}')

####################执行功能封装####################
# 下发电机运动
    def set_angle_and_execute(self, angle, duration):
        self.open_device()
        self.init_can_channel()
        self.start_can_channel()
        # self.set_feedback_interval(self.motor_id, interval_s)
        
        for _ in range(duration):
            self.send_angle(self.motor_id, angle)
            data = self.receive_data()
            self.parse_received_data(data)
            time.sleep(1)

        data = self.receive_data()
        self.parse_received_data(data)
        self.close_device()
# 下发电机运动 循环
    def set_angle_and_execute_rand(self, angle1, angle2, duration):
        self.open_device()
        self.init_can_channel()
        self.start_can_channel()
        
        for _ in range(duration):
            # Send the first angle
            self.send_angle(self.motor_id, angle1)
            data = self.receive_data()
            self.parse_received_data(data)
            time.sleep(5)
            
            # Send the second angle
            self. send_angle(self.motor_id, angle2)  
            data = self.receive_data()
            self.parse_received_data(data)
            time.sleep(5)

        self.close_device()

# 初始化电机，设置零点和新ID 正反转
    def initialize_motor(self, motor_id, new_id):
        self.open_device()
        self.init_can_channel()
        self.start_can_channel()
        
        for _ in range(2):
            self.set_motor_id(motor_id, new_id)
            self.set_zero_point(motor_id)
            self.set_max_angle(motor_id=0x01, angle=270, direction='positive')
            self.set_max_angle(motor_id=0x01, angle=-90, direction='negative')
            self.parse_status_byte
            time.sleep(1)

        for _ in range(3):
            data = self.receive_data()
            self.parse_received_data(data)
            time.sleep(1)

        self.close_device()
        
 # 读取电机信息
    def state_motor(self):
        self.open_device()
        self.init_can_channel()
        self.start_can_channel()
        for _ in range(3):
            data = self.receive_data()
            self.parse_received_data(data)
            time.sleep(1)
        self.close_device()


# 示例用法/注意事项：
# 角度增大逆时针执行，角度减小顺时针执行
# 运行角度不宜设置为最大正反转角度

# 创建一个CANMotorController对象并使用它
# controller = CANMotorController(motor_id=0x01)
# 下发电机运动
# controller.set_angle_and_execute(angle= -90, duration=3)

################往复##########################

# controller.set_angle_and_execute_rand(angle1 = -90, angle2 = 0, duration=3)



################修复##########################

# 初始化电机，设置零点和新ID 正反转
# controller.initialize_motor(motor_id=0x01, new_id=0x01)


