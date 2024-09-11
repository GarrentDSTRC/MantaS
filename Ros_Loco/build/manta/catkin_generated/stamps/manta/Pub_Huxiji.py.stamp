#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Float32

def publish_steps():
    rospy.init_node('step_publisher', anonymous=True)
    position_pub = rospy.Publisher('/absolute_position', Float32, queue_size=10)
    description_pub = rospy.Publisher('/step_description', String, queue_size=10)
    
    steps = [
        (0, "开状态"),
        (-90, "一轮测量（关状态）"),
        (0, "换水"),
        (90, "二轮测量"),
        (180, "换水"),
        (90, "三轮测量"),
        (0, "换水"),
        (90, "四轮测量"),
        (0, "换水（开状态）")
    ]
    
    instructions = """
    请选择要发布的步骤：
    1: 开状态
    2: 一轮测量（关状态）
    3: 换水
    4: 二轮测量
    5: 换水
    6: 三轮测量
    7: 换水
    8: 四轮测量
    9: 换水（开状态）
    输入对应的数字然后按Enter键:
    """
    
    while not rospy.is_shutdown():
        print(instructions)
        command = input("请输入步骤 (1/2/3/4/5/6/7/8/9): ")
        
        if command in map(str, range(1, 10)):
            step_index = int(command) - 1
            absolute_position, description = steps[step_index]
            rospy.loginfo(f"当前绝对位置: {absolute_position}")
            rospy.loginfo(f"描述: {description}")
            position_pub.publish(absolute_position)
            description_pub.publish(description)
        else:
            rospy.logwarn("无效的命令，请输入 1 到 9 之间的数字")
        
        rospy.sleep(1)  # 暂停一秒钟以避免过快的循环

if __name__ == '__main__':
    try:
        publish_steps()
    except rospy.ROSInterruptException:
        pass
