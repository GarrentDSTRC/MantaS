import rospy
from std_msgs.msg import String

def publisher():
    pub = rospy.Publisher('relay_command', String, queue_size=10)
    rospy.init_node('relay_publisher', anonymous=True)
    rate = rospy.Rate(0.5)  # 0.5 Hz (2秒一次)

    paozai_state = False
    led_state = False
    xiaoyu_state = False
    read_sensor_state = False

    while not rospy.is_shutdown():
        # 切换抛载继电器的状态
        paozai_command = "paozaion" if paozai_state else "paozaioff"
        rospy.loginfo(f"Publishing command: {paozai_command}")
        pub.publish(paozai_command)
        paozai_state = not paozai_state
        rate.sleep()

        # 切换LED的状态
        led_command = "ledon" if led_state else "ledoff"
        rospy.loginfo(f"Publishing command: {led_command}")
        pub.publish(led_command)
        led_state = not led_state
        rate.sleep()

        # 切换小鱼抛载的状态
        xiaoyu_command = "xiaoyuon" if xiaoyu_state else "xiaoyuoff"
        rospy.loginfo(f"Publishing command: {xiaoyu_command}")
        pub.publish(xiaoyu_command)
        xiaoyu_state = not xiaoyu_state
        rate.sleep()

        # 发送读取传感器状态的命令
        read_sensor_command = "readsensors"
        rospy.loginfo(f"Publishing command: {read_sensor_command}")
        pub.publish(read_sensor_command)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
