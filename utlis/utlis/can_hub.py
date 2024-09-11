from ctypes import *

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

class CANDevice:
    def __init__(self, device_id):
        self.VCI_USBCAN2 = VCI_USBCAN2
        self.STATUS_OK = STATUS_OK
        self.device_id = device_id
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
            print('接收数据失败, 错误码:', ret)
            return None

def main():
    # 初始化CAN设备，设定CAN盒子的ID
    device_id = 0
    can_device = CANDevice(device_id)

    # 打开设备
    can_device.open_device()

    # 初始化CAN通道
    can_device.init_can_channel()

    # 启动CAN通道
    can_device.start_can_channel()

    # 创建一个VCI_CAN_OBJ实例并发送命令
    vci_can_obj = VCI_CAN_OBJ(ID=0x01, TimeStamp=0, TimeFlag=0, SendType=0, RemoteFlag=0, ExternFlag=0, DataLen=8, Data=(c_ubyte * 8)(1, 2, 3, 4, 5, 6, 7, 8), Reserved=(c_ubyte * 3)(0, 0, 0))
    can_device.send_command(vci_can_obj)

    # 接收数据
    received_data = can_device.receive_data()

    # 关闭设备
    can_device.close_device()

if __name__ == "__main__":
    main()