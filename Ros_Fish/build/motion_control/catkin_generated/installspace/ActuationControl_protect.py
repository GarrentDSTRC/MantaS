#!/usr/bin/env python3

####################rosrun中防止引用自定义类 无法找到####################
import sys
import os
# 确保当前脚本目录在 sys.path 中
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)


import os
import threading
import time
from ctypes import *
import ctypes
from threading import Thread
import csv
import binascii
import datetime
import rospy
from std_msgs.msg import UInt8  # 用于接收ID
from motion_control.msg import MotorCommandMsg
from motion_control.msg import PropellerCommandMsg 
from std_msgs.msg import String
from check_ethernet import NetworkInterfaceChecker  


VCI_USBCAN2 = 4
STATUS_OK = 1
CAN_POS = 0     # 0: CAN1    1: CAN2
# 0 表示左旋， 1表示右旋
vis = [0, 0, 1, 1, 1, 1, 1, 1]
ID = [0x0360, 0x0361, 0x035F, 0x0364, 0x0313, 0x0314, 0x303, 0x304]


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



# Construct the path to the shared library
lib_path = os.path.join(script_dir, '..', 'lib', 'arm_libcontrolcan.so')

# Load the shared library
canDLL = cdll.LoadLibrary(lib_path)

# CanDLLName = 'devel/lib/libcontrolcan.so'  # 把DLL放到对应的目录下
# lib_path = os.getcwd() + "\\function\\libs\\ControlCAN.dll"
# # canDLL = windll.LoadLibrary('../libs/ControlCAN.dll')
# canDLL = ctypes.cdll.LoadLibrary(CanDLLName)

ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
if ret == STATUS_OK:
    print('调用 VCI_OpenDevice成功\r\n')
else:
    print('调用 VCI_OpenDevice出错\r\n')

# 初始0通道
vci_initconfig = VCI_INIT_CONFIG(0x80000000, 0xFFFFFFFF, 0, 0, 0x00, 0x1C, 0)  # 波特率500k，正常模式
ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 0, byref(vci_initconfig))
if ret == STATUS_OK:
    print('调用 VCI_InitCAN1成功\r\n')
else:
    print('调用 VCI_InitCAN1出错\r\n')

ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 0)
if ret == STATUS_OK:
    print('调用 VCI_StartCAN1成功\r\n')
else:
    print('调用 VCI_StartCAN1出错\r\n')

# 初始1通道
ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 1, byref(vci_initconfig))
if ret == STATUS_OK:
    print('调用 VCI_InitCAN2 成功\r\n')
else:
    print('调用 VCI_InitCAN2 出错\r\n')

ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 1)
if ret == STATUS_OK:
    print('调用 VCI_StartCAN2 成功\r\n')
else:
    print('调用 VCI_StartCAN2 出错\r\n')

# 接收结构体数组类
class VCI_CAN_OBJ_ARRAY(Structure):
    _fields_ = [('SIZE', ctypes.c_uint16), ('STRUCT_ARRAY', ctypes.POINTER(VCI_CAN_OBJ))]

    def __init__(self, num_of_structs):
        self.STRUCT_ARRAY = ctypes.cast((VCI_CAN_OBJ * num_of_structs)(), ctypes.POINTER(VCI_CAN_OBJ))  # 结构体数组
        self.SIZE = num_of_structs  # 结构体长度
        self.ADDR = self.STRUCT_ARRAY[0]  # 结构体数组地址  byref()转c地址


def getRequest(form):
    ubyte_array = c_ubyte * 8
    if form == 11:      # 查故障
        return ubyte_array(0x45, 0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
    elif form == 12:    # 查速度
        return ubyte_array(0x51, 0x56, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
    elif form == 13:    # 查电流
        return ubyte_array(0x51, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
    elif form == 14:    # 查温度
        return ubyte_array(0x51, 0x54, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)


# 获取速度的命令数据
def getVelocityM(v):
    ubyte_array = c_ubyte * 8
    if v >= 0:
        return ubyte_array(0x54, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00, v & 0xFF)
    else:
        return ubyte_array(0x54, 0x43, 0x00, 0x00, 0xFF, 0xFF, 0xFF, v & 0xFF)

def getDataM(pid, v):
    if (pid >= 0) and (pid <= 7):
        if vis[pid] == 0:   # 左旋
            return getVelocityM(-v)
        else:               # 右旋
            return getVelocityM(v)

def getDataP(pid, v):
    ubyte_array = c_ubyte * 8
    if (pid >= 0) and (pid <= 7):
        if vis[pid] == 0:   # 左旋
            return ubyte_array(0x56, 0x43, 0x00, 0x00, 0x00, 0x00, (-v >> 8) & 0xFF, -v & 0xFF)
        else:               # 右旋
            return ubyte_array(0x56, 0x43, 0x00, 0x00, 0x00, 0x00, (v >> 8) & 0xFF, v & 0xFF)


# 查询信息：故障查询、速度查询、电流查询、温度查询
def getForm(form):
    if (form >= 11) and (form <= 14):
        return getRequest(form)


def PrintCommand(vci_can_obj, output=1):
    # 打印每个字段的16进制值
    if output:
        print("ID:", hex(vci_can_obj.ID))
        print("TimeStamp:", hex(vci_can_obj.TimeStamp))
        print("TimeFlag:", hex(vci_can_obj.TimeFlag))
        print("SendType:", hex(vci_can_obj.SendType))
        print("RemoteFlag:", hex(vci_can_obj.RemoteFlag))
        print("ExternFlag:", hex(vci_can_obj.ExternFlag))
        print("DataLen:", hex(vci_can_obj.DataLen))
    # 将列表转换为 bytes 对象
    Data_bytes = bytes(vci_can_obj.Data)
    # 使用 binascii.hexlify 将字节转换为16进制字符串
    Data_hex = binascii.hexlify(Data_bytes).decode('utf-8')
    print("DATA", Data_hex)
    print("Reserved:", list(vci_can_obj.Reserved))
    return hex(vci_can_obj.ID), Data_hex


# 通道1发送数据，通道2接收数据：pid表示哪个螺旋桨（1-7），form表示哪种信息查询：故障查询、速度查询、电流查询、温度查询（11-14）
def sendForm(pid, form):
    a = getForm(form)
    ubyte_3array = c_ubyte * 3
    b = ubyte_3array(0, 0, 0)
    # 向pid螺旋桨发送速度为v的命令
    vci_can_obj = VCI_CAN_OBJ(ID[pid], 0, 0, 1, 0, 0, 8, a, b)  # 单次发送

    res = canDLL.VCI_Transmit(VCI_USBCAN2, 0, CAN_POS, byref(vci_can_obj), 1)
    time.sleep(0.1)
    if res == STATUS_OK:
        print('CAN1通道发送成功\r\n')
    else:
        print('CAN1通道发送失败\r\n')
    time.sleep(1)
    return read_last_csv_data()


def read_last_csv_data(filename='Actuatordata.csv'):
    last_id = None
    last_data = None
    # 打开 CSV 文件用于读取
    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        # 遍历 CSV 文件中的每一行
        for row in csvreader:
            # 假设第一列是 ID，其余列是 Data
            last_id = row[1]  # 保存 ID
            last_data = row[2:]  # 保存除了 ID 之外的所有数据
    return last_id, last_data


# 将传入螺旋桨pid对应的螺旋桨停止
def StopPropeller(pids):
    for i in pids:
        handle_command(i, 0)
        handle_command(i, 0)
    # closeCanDLL()


# 关闭通道
def closeCanDLL():
    canDLL.VCI_CloseDevice(VCI_USBCAN2, 0)


def motor_command_callback(data):
    handle_command(data, 'motor')

def propeller_command_callback(data):
    handle_command(data, 'propeller')

def handle_command(data, device_type):
    pid = data.ID
    v = data.command  # 假设order消息中包含速度命令
    if device_type == 'motor':
        # 处理电机命令
        a = getDataM(pid, v)
    elif device_type == 'propeller':
        a = getDataP(pid, v)
    else:
        rospy.logerr("Unknown device type")
        return False
    ubyte_3array = c_ubyte * 3
    b = ubyte_3array(0, 0, 0)
    # 向pid螺旋桨发送速度为v的命令
    if device_type == 'propeller':
        vci_can_obj = VCI_CAN_OBJ(ID[pid], 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
    if device_type == 'motor':
        vci_can_obj = VCI_CAN_OBJ(ID[pid] , 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
        # time.sleep(0.1)
        # vci_can_obj = VCI_CAN_OBJ(0x0300 | 4, 0, 0, 1, 0, 0, 8, a, b)  # 单次发送
    PrintCommand(vci_can_obj)
    res = canDLL.VCI_Transmit(VCI_USBCAN2, 0, CAN_POS, byref(vci_can_obj), 1)
    time.sleep(0.1)
    if res == STATUS_OK:
        print('CAN1通道发送成功\r\n')
    else:
        print('CAN1通道发送失败\r\n')
        return False
    return True

def actuation_node():
    # 初始化ROS节点
    rospy.init_node('actuation_node', anonymous=True)

    # 创建Publisher对象，用于向电机和螺旋桨发送命令
    # 这里使用两个Publisher，实际使用时根据需要创建
    # motor_pub = rospy.Publisher('motor_commands', MotorCommandMsg, queue_size=10)
    # propeller_pub = rospy.Publisher('propeller_commands', PropellerCommandMsg, queue_size=10)

    # 订阅电机命令主题
    rospy.Subscriber('motor_commands', MotorCommandMsg, motor_command_callback)
    # 订阅螺旋桨命令主题
    rospy.Subscriber('propeller_commands', PropellerCommandMsg, propeller_command_callback)

    # 保持节点运行
    rospy.spin()


def receiveData():
    global stop_receiving
    open('Actuatordata.csv', 'a').close()
    while not rospy.is_shutdown():
        time.sleep(0.03)
        rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)  # 结构体数组
        res = canDLL.VCI_Receive(VCI_USBCAN2, 0, CAN_POS, byref(rx_vci_can_obj.ADDR), 2500, 0)
        if res > 0:  # 接收到一帧数据
            with open('Actuatordata.csv', 'a', newline='') as csvfile:
                csvwrite = csv.writer(csvfile)
                print('接收成功\r\n')

                # 将数据写入 CSV 文件
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ID, can_msg = PrintCommand(rx_vci_can_obj.ADDR)
                csvwrite.writerow([current_time, ID, can_msg])
                # 发布 CAN 消息数据
                pub = rospy.Publisher('can_messages', String, queue_size=10)
                msg = String()
                msg.data = str(can_msg)
                pub.publish(msg)
            # 检查错误条件并发布错误消息
            error_pub = rospy.Publisher('can_error_messages', String, queue_size=10)
            error_msg = String()
            if can_msg[-4:] == 'EEEE':
                error_msg.data = f"Error: Propeller blocked for ID {ID}"
                error_pub.publish(error_msg)
            elif can_msg[-4:] == '0000':
                error_msg.data = f"Error: Actuator stopped for ID {ID}"
                error_pub.publish(error_msg)


def stop_all_propellers():
    for pid in range(len(ID)):
        handle_command(MotorCommandMsg(ID=pid, command=0), 'propeller')
        handle_command(MotorCommandMsg(ID=pid, command=0), 'motor')


if __name__ == '__main__':
    # 初始化NetworkInterfaceChecker
    checker = NetworkInterfaceChecker('192.168.50.10')
    checker.set_callback(stop_all_propellers)  # 设置触发保护功能的回调函数
    checker_thread = threading.Thread(target=checker.check_interface_communication)
    checker_thread.start()  # 启动线程

    # 创建一个线程来运行receiveData函数
    thread = threading.Thread(target=receiveData)
    thread.start()  # 启动线程

    try:
        actuation_node()
    except rospy.ROSInterruptException:
        pass
    finally:
        checker.stop()  # 停止网络检查线程