#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def command_publisher():
    pub = rospy.Publisher('IO_control_zj', String, queue_size=10)
    rospy.init_node('IO_pub_node', anonymous=True)
    
    instructions = """
    请选择要发布的命令：
    1: 脱钩磁铁打开
    2: 脱钩磁铁关闭
    3: LED1关闭
    4: LED1打开
    5: LED2打开（无用）
    6: LED2关闭（无用）
    7: LED3关闭
    8: LED3打开
    输入对应的数字然后按Enter键:
    """

    while not rospy.is_shutdown():
        print(instructions)
        command = input("请输入指令 (1/2/3/4/5/6/7/8): ")
        
        if command == "1":
            tuogou_command = "tuogouon"
            rospy.loginfo(f"Publishing command: {tuogou_command}")
            pub.publish(tuogou_command)
        elif command == "2":
            tuogou_command = "tuogouoff"
            rospy.loginfo(f"Publishing command: {tuogou_command}")
            pub.publish(tuogou_command)
        elif command == "3":
            led1_command = "led1on"
            rospy.loginfo(f"Publishing command: {led1_command}")
            pub.publish(led1_command)
        elif command == "4":
            led1_command = "led1off"
            rospy.loginfo(f"Publishing command: {led1_command}")
            pub.publish(led1_command)
        elif command == "5":
            led2_command = "led2on"
            rospy.loginfo(f"Publishing command: {led2_command}")
            pub.publish(led2_command)
        elif command == "6":
            led2_command = "led2off"
            rospy.loginfo(f"Publishing command: {led2_command}")
            pub.publish(led2_command)
        elif command == "7":
            led3_command = "led3on"
            rospy.loginfo(f"Publishing command: {led3_command}")
            pub.publish(led3_command)
        elif command == "8":
            led3_command = "led3off"
            rospy.loginfo(f"Publishing command: {led3_command}")
            pub.publish(led3_command)
        else:
            rospy.logwarn("无效的命令，请输入 1, 2, 3, 4, 5, 6, 7 或 8")
        
        rospy.sleep(1)  # 暂停一秒钟以避免过快的循环

if __name__ == '__main__':
    try:
        command_publisher()
    except rospy.ROSInterruptException:
        pass
