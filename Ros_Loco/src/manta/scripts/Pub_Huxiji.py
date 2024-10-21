#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Float32

def publish_steps():
    rospy.init_node('step_publisher', anonymous=True)
    position_pub = rospy.Publisher('/relative_position', Float32, queue_size=10)
    description_pub = rospy.Publisher('/absolute_description', Float32, queue_size=10)
    
    steps = [
        (1, 90),
        (0,-90),
    ]
    
    instructions = """
    请选择要发布的步骤：
    1: +90
    2: -90
    输入对应的数字然后按Enter键:
    """
    angle=0
    while not rospy.is_shutdown():
        print(instructions)
        command = input("请输入步骤 (1/2): ")
        
        if command in map(str, range(1, 3)):
            step_index = int(command) - 1
            absolute_position, description = steps[step_index]
            rospy.loginfo(f"相对位置指令: {absolute_position}")
            angle=angle+description
            rospy.loginfo(f"绝对位置: {angle}")
            position_pub.publish(absolute_position)
            description_pub.publish(angle)
        else:
            rospy.logwarn("无效的命令，请输入 1 到 9 之间的数字")
        
        rospy.sleep(1)  # 暂停一秒钟以避免过快的循环

if __name__ == '__main__':
    try:
        publish_steps()
    except rospy.ROSInterruptException:
        pass
