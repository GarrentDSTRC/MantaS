#!/usr/bin/env python3

import rospy
import Jetson.GPIO as GPIO
from std_msgs.msg import String

####漏水传感器GPIO引脚#####
loushui_sensor_pin_qiangdian = 31
loushui_sensor_pin_ruodian = 33

def gpio_setup():
    GPIO.setmode(GPIO.BOARD)  # 或者GPIO.BCM，根据您的编号方式
    GPIO.setup(loushui_sensor_pin_qiangdian, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(loushui_sensor_pin_ruodian, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_sensor_states():
    qiangdian_state = GPIO.input(loushui_sensor_pin_qiangdian)
    ruodian_state = GPIO.input(loushui_sensor_pin_ruodian)
    return qiangdian_state, ruodian_state

def sensor_monitor():
    rospy.init_node('loushui_sensor_monitor', anonymous=True)
    qiangdian_pub = rospy.Publisher('qiangdian_leak_state', String, queue_size=10)
    ruodian_pub = rospy.Publisher('ruodian_leak_state', String, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        qiangdian_state, ruodian_state = read_sensor_states()
        
        if qiangdian_state:
            qiangdian_msg = "强电罐漏水"
        else:
            qiangdian_msg = "强电罐无漏水"
        
        if ruodian_state:
            ruodian_msg = "弱电罐漏水"
        else:
            ruodian_msg = "弱电罐无漏水"

        qiangdian_pub.publish(qiangdian_msg)
        ruodian_pub.publish(ruodian_msg)
        
        rospy.loginfo(f"发布强电罐状态: {qiangdian_msg}, 发布弱电罐状态: {ruodian_msg}")
        rate.sleep()

if __name__ == '__main__':
    gpio_setup()
    try:
        sensor_monitor()
    except rospy.ROSInterruptException:
        pass
    finally:
        GPIO.cleanup()