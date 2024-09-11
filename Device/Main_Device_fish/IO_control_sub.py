#!/usr/bin/env python3

import rospy
import Jetson.GPIO as GPIO
from std_msgs.msg import String

########################GPIO定义#######################

# 灯光继电器引脚： 16
# LED灯继电器引脚： 12
# 小鱼抛载继电器引脚： 18
# 强电罐漏水传感器引脚： 11
# 弱电罐漏水传感器引脚： 13

######################################################

######定义继电器GPIO引脚#####
paozai_relay_pin = 18
led_relay_pin = 16
xiaoyu_relay_pin = 12

####漏水传感器GPIO引脚#####
loushui_sensor_pin_qiangdian = 31
loushui_sensor_pin_ruodian = 33

def gpio_setup():
    GPIO.setmode(GPIO.BOARD)  # 或者GPIO.BCM，根据您的编号方式
    GPIO.setup(paozai_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(led_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(xiaoyu_relay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(loushui_sensor_pin_qiangdian, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(loushui_sensor_pin_ruodian, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_sensor_states():
    qiangdian_state = GPIO.input(loushui_sensor_pin_qiangdian)
    ruodian_state = GPIO.input(loushui_sensor_pin_ruodian)
    return qiangdian_state, ruodian_state

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
    elif data.data == "readsensors":
        qiangdian_state, ruodian_state = read_sensor_states()
        rospy.loginfo(f"强电罐漏水传感器状态: {'有漏水' if qiangdian_state else '无漏水'}")
        rospy.loginfo(f"弱电罐漏水传感器状态: {'有漏水' if ruodian_state else '无漏水'}")

def listener():
    rospy.init_node('relay_control', anonymous=True)
    rospy.Subscriber("relay_command", String, callback)
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
