from ctypes import *

class PropellerController:

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

    # def __init__(self, motor_id):
    #     self.motor_id = motor_id

    ####################基础功能####################

    # 发送信号控制命令
    def signal_control(self, percentage):
        data_array = (c_ubyte * 8)(0x54, 0x43, 0x00, 0x00, 0x00, 0x00, (percentage >> 8) & 0xFF, percentage & 0xFF)
        return data_array
    
    # 读取信号控制命令
    def analyze_feedback(self, feedback):
        if feedback[0:4] == [0x54, 0x43, 0x00, 0x00]:
            if feedback[4] == 0x00 and feedback[5] == 0x00:
                if feedback[6] == 0x00:
                    return f"推进器正常，信号为+{feedback[7]}%"
                elif feedback[6] == 0xFF:
                    return f"推进器正常，信号为-{(0xFF - feedback[7] + 1)}%"
                elif feedback[6] == 0xEE and feedback[7] == 0xEE:
                    return "推进器故障"
        return "未知反馈数据"
    
    # 发送转速控制命令
    def speed_control(self, motor_id, speed):
        data_array = (c_ubyte * 8)(0x56, 0x43, 0x00, 0x00, 0x00, 0x00, (speed >> 8) & 0xFF, speed & 0xFF)
        return data_array

    # 请求当前转速
    def request_speed(self, motor_id):
        data_array = (c_ubyte * 4)(0x51, 0x56, 0x00, 0x00)
        return data_array

    # 请求当前电流
    def request_current(self, motor_id):
        data_array = (c_ubyte * 4)(0x51, 0x43, 0x00, 0x00)
        return data_array

    # 请求当前电压
    def request_voltage(self, motor_id):
        data_array = (c_ubyte * 4)(0x51, 0x50, 0x00, 0x00)
        return data_array

    # 请求电机温度
    def request_temperature(self, motor_id):
        data_array = (c_ubyte * 4)(0x51, 0x54, 0x00, 0x00)
        return data_array

    # 请求错误状态
    def request_error_status(self, motor_id):
        data_array = (c_ubyte * 4)(0x45, 0x46, 0x00, 0x00)
        return data_array

    # 解析接收到的数据
    def parse_received_data(self, data):
        if data:
            command = (data[0] << 8) | data[1]
            value = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7]
            print(f'命令: {hex(command)}, 数据: {value}')

    ####################执行功能封装####################

#     def signal_control_and_execute(self, percentage, duration):
#         data_array = self.signal_control(self.motor_id, percentage)
#         # Here you can add the code to send data_array using your new CAN communication file

#     def speed_control_and_execute(self, speed, duration):
#         data_array = self.speed_control(self.motor_id, speed)
#         # Here you can add the code to send data_array using your new CAN communication file

#     def request_status_and_execute(self, duration):
#         speed_data_array = self.request_speed(self.motor_id)
#         current_data_array = self.request_current(self.motor_id)
#         voltage_data_array = self.request_voltage(self.motor_id)
#         temperature_data_array = self.request_temperature(self.motor_id)
#         error_status_data_array = self.request_error_status(self.motor_id)
#         # Here you can add the code to send these data arrays using your new CAN communication file

# # 示例用法：
# controller = PropellerController()
# # 发送信号控制命令并执行
# controller.signal_control_and_execute(percentage=5, duration=3)
# # 发送转速控制命令并执行
# controller.speed_control_and_execute(speed=500, duration=3)
# # 请求电机状态并打印
# controller.request_status_and_execute(duration=3)
