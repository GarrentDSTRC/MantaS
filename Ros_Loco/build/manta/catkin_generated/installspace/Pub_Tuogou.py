#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool

def publish_control_signal():
    # 初始化节点
    rospy.init_node('Tuogou_control_publisher', anonymous=True)
    
    # 创建发布者，发布到 'motor_control_topic' 话题
    pub = rospy.Publisher('Tuogou_control', Bool, queue_size=10)
    
    # 设置发布频率
    rate = rospy.Rate(1)  # 1 Hz
    
    # 提示用户输入
    rospy.loginfo("Enter 'on' to publish True, 'off' to publish False. Type 'exit' to quit.")
    
    while not rospy.is_shutdown():
        user_input = input("Enter command: ").strip().lower()
        
        if user_input == 'on':
            control_signal = Bool(data=True)
            rospy.loginfo("Publishing: True")
        elif user_input == 'off':
            control_signal = Bool(data=False)
            rospy.loginfo("Publishing: False")
        elif user_input == 'exit':
            rospy.loginfo("Exiting publisher...")
            break
        else:
            rospy.loginfo("Invalid command. Please enter 'on', 'off', or 'exit'.")
            continue
        
        pub.publish(control_signal)
        rate.sleep()
    
    # 关闭节点
    rospy.signal_shutdown('Publisher task completed.')

if __name__ == '__main__':
    try:
        publish_control_signal()
    except rospy.ROSInterruptException:
        pass
