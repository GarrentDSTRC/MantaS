#!/usr/bin/env python3

import rospy
import Jetson.GPIO as GPIO
from std_msgs.msg import String

####漏水传感器GPIO引脚#####
loushui_sensor_pin_zhongji = 31

def gpio_setup():
    GPIO.setmode(GPIO.BOARD)  # 或者GPIO.BCM，根据您的编号方式
    GPIO.setup(loushui_sensor_pin_zhongji, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_sensor_states():
    zhongji_state = GPIO.input(loushui_sensor_pin_zhongji)
    return zhongji_state

def loushui_sensor_monitor_zhongji():
    rospy.init_node('loushui_sensor_monitor_zhongji', anonymous=True)
    ruodian_pub = rospy.Publisher('loushui_sensor_pin_zhongji', String, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        zhongji_state = read_sensor_states()
        

        if zhongji_state:
            zhongji_msg = "弱电罐漏水"
        else:
            zhongji_msg = "弱电罐无漏水"

        ruodian_pub.publish(zhongji_msg)
        
        rospy.loginfo(f"发布中继漏水传感状态: {zhongji_msg}")
        rate.sleep()

if __name__ == '__main__':
    gpio_setup()
    try:
        loushui_sensor_monitor_zhongji()
    except rospy.ROSInterruptException:
        pass
    finally:
        GPIO.cleanup()
