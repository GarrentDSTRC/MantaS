#!/usr/bin/env python3

import rospy
import Jetson.GPIO as GPIO
from std_msgs.msg import String

########################GPIO定义#######################

# 灯光继电器引脚： 16
# LED灯继电器引脚： 12
# 小鱼抛载继电器引脚： 

######################################################

######定义继电器GPIO引脚#####
paozai_relay_pin = 18
led_relay_pin = 16
xiaoyu_relay_pin = 12


def gpio_setup():
    GPIO.setmode(GPIO.BOARD)  # 或者GPIO.BCM，根据您的编号方式
    GPIO.setup(paozai_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(xiaoyu_relay_pin, GPIO.OUT, initial=GPIO.LOW)


def callback(data):
    rospy.loginfo(f"I heard: {data.data}")
    if data.data == "paozaion":
        GPIO.output(paozai_relay_pin, GPIO.HIGH)
        rospy.loginfo("抛载继电器打开")
    elif data.data == "paozaioff":
        GPIO.output(paozai_relay_pin, GPIO.LOW)
        rospy.loginfo("抛载继电器关闭")
    elif data.data == "ledon":
        GPIO.output(led_relay_pin, GPIO.HIGH)
        rospy.loginfo("LED灯打开")
    elif data.data == "ledoff":
        GPIO.output(led_relay_pin, GPIO.LOW)
        rospy.loginfo("LED灯关闭")
    elif data.data == "xiaoyuon":
        GPIO.output(xiaoyu_relay_pin, GPIO.HIGH)
        rospy.loginfo("小鱼抛载开")
    elif data.data == "xiaoyuoff":
        GPIO.output(xiaoyu_relay_pin, GPIO.LOW)
        rospy.loginfo("小鱼抛载关闭")

def listener():
    rospy.init_node('IO_sub_node', anonymous=True)
    rospy.Subscriber("IO_control", String, callback)
    rospy.loginfo("Relay control node started, waiting for commands...")
    rospy.spin()

if __name__ == '__main__':
    gpio_setup()
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
    finally:
        GPIO.cleanup()
