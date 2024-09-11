# from ctypes import *
# import time

# class BodongqiController:
#     VCI_USBCAN2 = 4
#     STATUS_OK = 1

#     class VCI_INIT_CONFIG(Structure):
#         _fields_ = [("AccCode", c_uint),
#                     ("AccMask", c_uint),
#                     ("Reserved", c_uint),
#                     ("Filter", c_ubyte),
#                     ("Timing0", c_ubyte),
#                     ("Timing1", c_ubyte),
#                     ("Mode", c_ubyte)]

#     class VCI_CAN_OBJ(Structure):
#         _fields_ = [("ID", c_uint),
#                     ("TimeStamp", c_uint),
#                     ("TimeFlag", c_ubyte),
#                     ("SendType", c_ubyte),
#                     ("RemoteFlag", c_ubyte),
#                     ("ExternFlag", c_ubyte),
#                     ("DataLen", c_ubyte),
#                     ("Data", c_ubyte * 8),
#                     ("Reserved", c_ubyte * 3)]

#     def __init__(self, motor_id):
#         self.motor_id = motor_id

#     def open_device(self):
#         self.canDLL = cdll.LoadLibrary('../../lib/86_libcontrolcan.so')
#         ret = self.canDLL.VCI_OpenDevice(self.VCI_USBCAN2, 0, 0)
#         if ret == self.STATUS_OK:
#             print('调用 VCI_OpenDevice 成功')
#         else:
#             print(f'调用 VCI_OpenDevice 出错, 错误码: {ret}')
#             exit()

#     def init_can_channel(self):
#         vci_initconfig = self.VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x1C, 0)
#         ret = self.canDLL.VCI_InitCAN(self.VCI_USBCAN2, 0, 0, byref(vci_initconfig))
#         if ret == self.STATUS_OK:
#             print('初始化通道0成功')
#         else:
#             print(f'初始化通道0出错, 错误码: {ret}')
#             exit()

#     def close_device(self):
#         ret = self.canDLL.VCI_CloseDevice(self.VCI_USBCAN2, 0)
#         if ret == self.STATUS_OK:
#             print('关闭设备成功')
#         else:
#             print(f'关闭设备失败, 错误码: {ret}')

#     def start_can_channel(self):
#         ret = self.canDLL.VCI_StartCAN(self.VCI_USBCAN2, 0, 0)
#         if ret == self.STATUS_OK:
#             print('启动通道0成功')
#         else:
#             print(f'启动通道0出错, 错误码: {ret}')
#             exit()

#     def send_command(self, vci_can_obj):
#         ret = self.canDLL.VCI_Transmit(self.VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
#         if ret == self.STATUS_OK:
#             print(f'命令发送成功: {list(vci_can_obj.Data)}')
#         else:
#             print(f'命令发送失败, 错误码: {ret}')

#     def receive_data(self):
#         ubyte_3array = c_ubyte * 3
#         reserved_array = ubyte_3array(0, 0, 0)
#         vci_can_obj = self.VCI_CAN_OBJ(0, 0, 0, 0, 0, 0, 0, (c_ubyte * 8)(0, 0, 0, 0, 0, 0, 0, 0), reserved_array)
#         ret = self.canDLL.VCI_Receive(self.VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1, 0)
#         if ret > 0:
#             data = list(vci_can_obj.Data)
#             print('接收到数据:', data)
#             return data
#         else:
#             print('接收数据失败, 错误码:', ret)
#             return None

#     ####################舵机基础功能####################

#     def set_torque_control(self, motor_id, torque):
#         data_array = (c_ubyte * 8)(0x54, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00, torque)
#         vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
#         self.send_command(vci_can_obj)
#         self.receive_data()

#     def request_speed(self, motor_id):
#         data_array = (c_ubyte * 8)(0x51, 0x56, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
#         vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
#         self.send_command(vci_can_obj)
#         data = self.receive_data()
#         self.parse_received_data(data)

#     def request_current(self, motor_id):
#         data_array = (c_ubyte * 8)(0x51, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
#         vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
#         self.send_command(vci_can_obj)
#         data = self.receive_data()
#         self.parse_received_data(data)

#     def request_voltage(self, motor_id):
#         data_array = (c_ubyte * 8)(0x51, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
#         vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
#         self.send_command(vci_can_obj)
#         data = self.receive_data()
#         self.parse_received_data(data)

#     def request_temperature(self, motor_id):
#         data_array = (c_ubyte * 8)(0x51, 0x54, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
#         vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
#         self.send_command(vci_can_obj)
#         data = self.receive_data()
#         self.parse_received_data(data)

#     def request_error_status(self, motor_id):
#         data_array = (c_ubyte * 8)(0x45, 0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
#         vci_can_obj = self.VCI_CAN_OBJ(motor_id, 0, 0, 1, 0, 0, 8, data_array)
#         self.send_command(vci_can_obj)
#         data = self.receive_data()
#         self.parse_received_data(data)

#     def parse_received_data(self, data):
#         if data:
#             command = (data[0] << 8) | data[1]
#             value = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7]
#             print(f'命令: {hex(command)}, 数据: {value}')

#     ####################执行功能封装####################

#     def set_torque_and_execute(self, torque, duration):
#         self.open_device()
#         self.init_can_channel()
#         self.start_can_channel()
        
#         for _ in range(duration):
#             self.set_torque_control(self.motor_id, torque)
#             time.sleep(1)

#         self.close_device()

#     def request_status_and_execute(self, duration):
#         self.open_device()
#         self.init_can_channel()
#         self.start_can_channel()
        
#         for _ in range(duration):
#             self.request_speed(self.motor_id)
#             self.request_current(self.motor_id)
#             self.request_voltage(self.motor_id)
#             self.request_temperature(self.motor_id)
#             self.request_error_status(self.motor_id)
#             time.sleep(1)

#         self.close_device()

# # 示例用法：
# controller = CANMotorController(motor_id=0x30B)
# # 发送力矩控制命令并执行
# controller.set_torque_and_execute(torque=5, duration=3)
# # 请求电机状态并打印
# controller.request_status_and_execute(duration=3)
