#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def command_publisher():
    pub = rospy.Publisher('IO_control', String, queue_size=10)
    rospy.init_node('IO_pub_node', anonymous=True)
    
    instructions = """
    请选择要发布的命令：
    1: 抛载电磁铁脱开
    2: 抛载电磁铁吸附
    3: LED关闭
    4: LED打开
    5: 小鱼抛载关闭
    6: 小鱼抛载打开
    7: 读取传感器状态
    输入对应的数字然后按Enter键:
    """
    #待确认指令的复杂以及保险程度

    while not rospy.is_shutdown():
        print(instructions)
        command = input("请输入指令 (1/2/3/4/5/6/7): ")
        
        if command == "1":
            paozai_command = "paozaion"
            rospy.loginfo(f"Publishing command: {paozai_command}")
            pub.publish(paozai_command)
        elif command == "2":
            paozai_command = "paozaioff"
            rospy.loginfo(f"Publishing command: {paozai_command}")
            pub.publish(paozai_command)
        elif command == "3":
            led_command = "ledon"
            rospy.loginfo(f"Publishing command: {led_command}")
            pub.publish(led_command)
        elif command == "4":
            led_command = "ledoff"
            rospy.loginfo(f"Publishing command: {led_command}")
            pub.publish(led_command)
        elif command == "5":
            xiaoyu_command = "xiaoyuon"
            rospy.loginfo(f"Publishing command: {xiaoyu_command}")
            pub.publish(xiaoyu_command)
        elif command == "6":
            xiaoyu_command = "xiaoyuoff"
            rospy.loginfo(f"Publishing command: {xiaoyu_command}")
            pub.publish(xiaoyu_command)
        elif command == "7":
            read_sensor_command = "readsensors"
            rospy.loginfo(f"Publishing command: {read_sensor_command}")
            pub.publish(read_sensor_command)
        else:
            rospy.logwarn("无效的命令，请输入 1, 2, 3, 4, 5, 6 或 7")
        
        rospy.sleep(1)  # 暂停一秒钟以避免过快的循环

if __name__ == '__main__':
    try:
        command_publisher()
    except rospy.ROSInterruptException:
        pass
