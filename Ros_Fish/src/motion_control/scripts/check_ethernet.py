import subprocess
import time
import logging
import psutil

class NetworkInterfaceChecker:
    def __init__(self, host='192.168.50.11', interface='eth0', check_interval=1, max_failures=1):
        self.host = host
        self.interface = interface
        self.check_interval = check_interval
        self.max_failures = max_failures
        self.consecutive_failures = 0
        self.callback = None  # 用于触发保护功能的回调函数
        self.running = False
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='/home/jetson/Dayu_Scripts/interface_status.log',
            level=logging.DEBUG,
            format='%(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.debug('日志系统设置完成。')

    def log_with_timestamp(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timestamp} - {message}")
        logging.info(message)

    def ping_host(self):
        try:
            result = subprocess.run(['ping', '-c', '1', self.host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return True
            else:
                self.log_with_timestamp(f"Error: {result.stderr.strip()}")
                return False
        except Exception as e:
            self.log_with_timestamp(f"An error occurred: {e}")
            return False

    def get_physical_network_interfaces(self):
        # 只返回指定的固定接口
        physical_interfaces = []
        interface = self.interface
        addrs = psutil.net_if_addrs().get(interface, [])
        for addr in addrs:
            if addr.family == psutil.AF_LINK:  # 检查是否为 MAC 地址
                physical_interfaces.append(interface)
                break
        logging.debug(f'物理网络接口：{physical_interfaces}')
        return physical_interfaces

    def set_callback(self, callback):
        self.callback = callback

    def check_interface_communication(self):
        self.running = True
        while self.running:
            interfaces = self.get_physical_network_interfaces()
            any_interface_communicating = False
            for interface in interfaces:
                self.log_with_timestamp(f"检查接口：{interface}")
                if self.ping_host():
                    self.log_with_timestamp(f"网络接口 {interface} 正常通信。")
                    any_interface_communicating = True
                    self.consecutive_failures = 0
                    break
                else:
                    self.log_with_timestamp(f"网络接口 {interface} 异常或无法通信。")
                    logging.warning(f"网络接口 {interface} 异常或无法通信。")
            
            if not any_interface_communicating:
                self.consecutive_failures += 1

            if self.consecutive_failures >= self.max_failures:
                self.log_with_timestamp("警报：100 秒内无网络接口正常通信。")
                logging.error("警报：100 秒内无网络接口正常通信。")
                if self.callback:
                    self.callback()  # 调用回调函数触发保护功能
                self.consecutive_failures = 0
                self.stop()      

            time.sleep(self.check_interval)  # 每1秒检测一次

    def stop(self):
        self.running = False

if __name__ == "__main__":
    checker = NetworkInterfaceChecker()
    try:
        checker.check_interface_communication()
    except KeyboardInterrupt:
        checker.stop()
    except Exception as e:
        logging.error(f"意外错误：{e}")
        checker.stop()
