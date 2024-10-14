import sys
import os
import rospy
import Jetson.GPIO as GPIO
from std_msgs.msg import String
import time
import signal

# 确保当前脚本目录在 sys.path 中
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 定义日志函数，带有时间戳
def log_with_timestamp(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    rospy.loginfo(f"{timestamp} - {message}")

# 定义继电器GPIO引脚
tuogou_relay_pin = 12  # 脱钩磁铁
led1_relay_pin = 18    # LED1
led2_relay_pin = 22    # LED2
led3_relay_pin = 24    # LED3

def gpio_setup():
    GPIO.setmode(GPIO.BOARD)  # 或者GPIO.BCM，根据您的编号方式
    GPIO.setup(tuogou_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led1_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led2_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led3_relay_pin, GPIO.OUT, initial=GPIO.LOW)

    # 默认LED灯打开3秒
    GPIO.output(led1_relay_pin, GPIO.LOW)
    GPIO.output(led2_relay_pin, GPIO.LOW)
    GPIO.output(led3_relay_pin, GPIO.LOW)
    log_with_timestamp("默认LED灯打开3秒")
    time.sleep(3)  # 延迟3秒
    GPIO.output(led1_relay_pin, GPIO.HIGH)
    GPIO.output(led2_relay_pin, GPIO.HIGH)
    GPIO.output(led3_relay_pin, GPIO.HIGH)
    log_with_timestamp("默认LED灯关闭")
    
def callback(data):
    log_with_timestamp(f"I heard: {data.data}")
    if data.data == "tuogouon":
        GPIO.output(tuogou_relay_pin, GPIO.HIGH)
        log_with_timestamp("脱钩磁铁打开")
    elif data.data == "tuogouoff":
        GPIO.output(tuogou_relay_pin, GPIO.LOW)
        log_with_timestamp("脱钩磁铁关闭")
    elif data.data == "led1on":
        GPIO.output(led1_relay_pin, GPIO.HIGH)
        log_with_timestamp("LED1打开")
    elif data.data == "led1off":
        GPIO.output(led1_relay_pin, GPIO.LOW)
        log_with_timestamp("LED1关闭")
    elif data.data == "led2on":
        GPIO.output(led2_relay_pin, GPIO.HIGH)
        log_with_timestamp("LED2打开")
    elif data.data == "led2off":
        GPIO.output(led2_relay_pin, GPIO.LOW)
        log_with_timestamp("LED2关闭")
    elif data.data == "led3on":
        GPIO.output(led3_relay_pin, GPIO.HIGH)
        log_with_timestamp("LED3打开")
    elif data.data == "led3off":
        GPIO.output(led3_relay_pin, GPIO.LOW)
        log_with_timestamp("LED3关闭")

def listener():
    rospy.init_node('IO_sub_node', anonymous=True)
    rospy.Subscriber("IO_control_zj", String, callback)
    log_with_timestamp("Relay control node started, waiting for commands...")
    rospy.spin()

def signal_handler(sig, frame):
    log_with_timestamp("Received SIGTERM, shutting down gracefully")
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    gpio_setup()
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
    finally:
        GPIO.cleanup()
