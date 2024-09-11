####################rosrun中防止引用自定义类 无法找到####################
# 确保当前脚本目录在 sys.path 中
import sys
import os
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

import rospy
import Jetson.GPIO as GPIO
from std_msgs.msg import String
import threading
from check_ethernet import NetworkInterfaceChecker
import time
import signal
import sys


# 定义日志函数，带有时间戳
def log_with_timestamp(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    rospy.loginfo(f"{timestamp} - {message}")

# 定义继电器GPIO引脚
paozai_relay_pin = 18
led_relay_pin = 13
led_relay_pin_2 = 15
led_relay_pin_3 = 16
xiaoyu_relay_pin = 24

def gpio_setup():
    GPIO.setmode(GPIO.BOARD)  # 或者GPIO.BCM，根据您的编号方式
    GPIO.setup(paozai_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led_relay_pin_2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led_relay_pin_3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(xiaoyu_relay_pin, GPIO.OUT, initial=GPIO.LOW)

    # 默认LED灯打开3秒
    GPIO.output(led_relay_pin, GPIO.HIGH)
    GPIO.output(led_relay_pin_2, GPIO.HIGH)
    GPIO.output(led_relay_pin_3, GPIO.HIGH)
    log_with_timestamp("默认LED灯打开3秒")
    time.sleep(3)  # 延迟3秒
    GPIO.output(led_relay_pin, GPIO.LOW)
    GPIO.output(led_relay_pin_2, GPIO.LOW)
    GPIO.output(led_relay_pin_3, GPIO.LOW)
    log_with_timestamp("默认LED灯关闭")
def callback(data):
    log_with_timestamp(f"I heard: {data.data}")
    if data.data == "paozaion":
        GPIO.output(paozai_relay_pin, GPIO.HIGH)
        log_with_timestamp("抛载继电器打开")
    elif data.data == "paozaioff":
        GPIO.output(paozai_relay_pin, GPIO.LOW)
        log_with_timestamp("抛载继电器关闭")
    elif data.data == "ledon":
        GPIO.output(led_relay_pin, GPIO.HIGH)
        GPIO.output(led_relay_pin_2, GPIO.HIGH)
        GPIO.output(led_relay_pin_3, GPIO.HIGH)
        log_with_timestamp("LED灯打开")
    elif data.data == "ledoff":
        GPIO.output(led_relay_pin, GPIO.LOW)
        GPIO.output(led_relay_pin_2, GPIO.LOW)
        GPIO.output(led_relay_pin_3, GPIO.LOW)
        log_with_timestamp("LED灯关闭")
    elif data.data == "xiaoyuon":
        GPIO.output(xiaoyu_relay_pin, GPIO.HIGH)
        log_with_timestamp("小鱼抛载开")
    elif data.data == "xiaoyuoff":
        GPIO.output(xiaoyu_relay_pin, GPIO.LOW)
        log_with_timestamp("小鱼抛载关闭")

def listener():
    rospy.init_node('IO_sub_node', anonymous=True)
    rospy.Subscriber("IO_control", String, callback)
    log_with_timestamp("Relay control node started, waiting for commands...")
    rospy.spin()

def trigger_paozai():
    GPIO.output(paozai_relay_pin, GPIO.HIGH)
    log_with_timestamp("抛载继电器触发")

def signal_handler(sig, frame):
    log_with_timestamp("Received SIGTERM, shutting down gracefully")
    # checker.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    gpio_setup()
    signal.signal(signal.SIGTERM, signal_handler)
    checker = NetworkInterfaceChecker('192.168.50.10')
    checker.set_callback(trigger_paozai)  # 设置触发保护功能的回调函数
    checker_thread = threading.Thread(target=checker.check_interface_communication)
    checker_thread.start()
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
    finally:
        # checker.stop()  # 停止网络检查线程
        GPIO.cleanup()
