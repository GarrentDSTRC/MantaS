import sys
# Add ROS library path
sys.path.append('/opt/ros/noetic/lib/python3/dist-packages')

import threading
import rospy
from std_msgs.msg import Int32MultiArray
from ctypes import *

# Import the two configuration files
from bongdongqi import BodongqiController
from propeller import PropellerController

# Create instances of the controllers
bodongqi_controller = BodongqiController()
propeller_controller = PropellerController()

# Define VCI structures
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

class CANDevice:
    def __init__(self):
        self.VCI_USBCAN2 = 4
        self.STATUS_OK = 1
        self.device_id = 0
        self.library_path = "./86_libcontrolcan.so"  # 默认路径
        self.canDLL = cdll.LoadLibrary(self.library_path)
        
    def open_device(self):
        ret = self.canDLL.VCI_OpenDevice(self.VCI_USBCAN2, self.device_id, 0)
        if ret == self.STATUS_OK:
            print('调用 VCI_OpenDevice 成功')
        else:
            print(f'调用 VCI_OpenDevice 出错, 错误码: {ret}')
            exit()

    def init_can_channel(self):
        vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x1C, 0)  # 波特率500k，正常模式
        ret = self.canDLL.VCI_InitCAN(self.VCI_USBCAN2, self.device_id, 0, byref(vci_initconfig))
        if ret == self.STATUS_OK:
            print('初始化通道0成功')
        else:
            print(f'初始化通道0出错, 错误码: {ret}')
            exit()

    def close_device(self):
        ret = self.canDLL.VCI_CloseDevice(self.VCI_USBCAN2, self.device_id)
        if ret == self.STATUS_OK:
            print('关闭设备成功')
        else:
            print(f'关闭设备失败, 错误码: {ret}')

    def start_can_channel(self):
        ret = self.canDLL.VCI_StartCAN(self.VCI_USBCAN2, self.device_id, 0)
        if ret == self.STATUS_OK:
            print('启动通道0成功')
        else:
            print(f'启动通道0出错, 错误码: {ret}')
            exit()
            
    def send_command(self, vci_can_obj):
        ret = self.canDLL.VCI_Transmit(self.VCI_USBCAN2, self.device_id, 0, byref(vci_can_obj), 1)
        if ret == self.STATUS_OK:
            print(f'命令发送成功: {list(vci_can_obj.Data)}')
        else:
            print(f'命令发送失败, 错误码: {ret}')

    def receive_data(self):
        ubyte_3array = c_ubyte * 3
        reserved_array = ubyte_3array(0, 0, 0)
        vci_can_obj = VCI_CAN_OBJ(0, 0, 0, 0, 0, 0, 0, (c_ubyte * 8)(0, 0, 0, 0, 0, 0, 0, 0), reserved_array)  # 准备接收对象
        ret = self.canDLL.VCI_Receive(self.VCI_USBCAN2, self.device_id, 0, byref(vci_can_obj), 1, 0)
        if ret > 0:
            data = list(vci_can_obj.Data)
            data_hex = [f'0x{byte:02X}' for byte in data]
            print('接收到数据:', data_hex)
            return data
        else:
            # print('接收数据失败, 错误码:', ret)
            return None

# Define propeller IDs
ids = [0x100, 0x200, 0x300, 0x400, 0x500, 0x600, 0x700, 0x800]  # 2个电机 6个螺旋桨的ID

# Function to get signal commands
def getControl(v):
    signal_cmds = []
    for i in range(8):  # 生成8组速度数据
        if i < 2:
            command = bodongqi_controller.signal_control(v[i])
        else:
            command = propeller_controller.signal_control(v[i])
        signal_cmds.append(command)
    return signal_cmds

# Callback function to handle subscribed signal data
def callback(data):
    global signal_commands  # 声明为全局变量
    ros_signal = data.data  # 从消息中获取速度数组
    rospy.loginfo(f"Received signal: {ros_signal}")
    signal_commands = getControl(ros_signal)  # 获取速度指令
    
    for i, cmd in enumerate(signal_commands):
        if i < 2:
            print(f"Motor {i + 1} signal command: {list(cmd)}")
        else:
            print(f"Propeller {i - 1} signal command: {list(cmd)}")
    
    send_control_commands(signal_commands)  # 发送指令到CAN总线

def listener():
    rospy.init_node('propeller_speed_listener', anonymous=True)
    rospy.Subscriber('/propeller_speeds', Int32MultiArray, callback)
    rospy.spin()

# Function to handle received signal commands and send to CAN bus
def send_control_commands(signal_commands):
    for i, id in enumerate(ids):
        data = (c_ubyte * 8)(*signal_commands[i])
        vci_can_obj = VCI_CAN_OBJ(id, 0, 0, 1, 0, 0, 8, data, (c_ubyte * 3)(0, 0, 0))  # 单次发送
        can_device.send_command(vci_can_obj)

# Function to receive feedback from CAN bus
def receive_feedback():
    while True:
        for i in range(8):  # 假设有8个设备回传数据
            feedback = can_device.receive_data()
            if feedback:
                if i < 2:
                    analysis_result = bodongqi_controller.analyze_feedback(feedback)
                else:
                    analysis_result = propeller_controller.analyze_feedback(feedback)
                print(f'Device {i + 1} feedback: {analysis_result}')

if __name__ == '__main__':
    can_device = CANDevice()
    can_device.open_device()
    can_device.init_can_channel()
    can_device.start_can_channel()
    
    # 启动一个新线程来处理CAN总线的回传数据
    feedback_thread = threading.Thread(target=receive_feedback)
    feedback_thread.daemon = True  # 设置为守护线程，确保主线程结束时它也会结束
    feedback_thread.start()

    listener()
    
    # can_device.close_device()
