import rospy
from manta.msg import PropellerCommandMsg
from manta.msg import MotorCommandMsg
import time

import sys
import os
# 确保当前脚本目录在 sys.path 中
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)


def test_propeller_node(ID,Comand):
    # 初始化ROS节点
    rospy.init_node('actuation_node', anonymous=True)

    # 创建一个Publisher对象，发布到propeller_commands主题
    pub = rospy.Publisher('propeller_commands', PropellerCommandMsg, queue_size=10)

    # 创建PropellerCommandMsg消息实例
    command_msg = PropellerCommandMsg()

    # 等待节点准备好发布消息
    rospy.sleep(1)

    # 发送ID为1，命令为900的消息
    command_msg.ID = ID
    command_msg.command =Comand
    pub.publish(command_msg)
    rospy.loginfo("Sent command to propeller %s with command %s" % (ID, Comand))


    # 保持节点运行一段时间，以便命令被处理
    rospy.sleep(0.2)
def test_motor_node(ID,Comand):

    # 初始化ROS节点
    #rospy.init_node('actuation_node', anonymous=True)
    # 创建一个Publisher对象，发布到motor_commands主题
    pub = rospy.Publisher('motor_commands', MotorCommandMsg, queue_size=10)

    # 创建MotorCommandMsg消息实例
    command_msg = MotorCommandMsg()

    # 等待节点准备好发布消息
    rospy.sleep(1)

    # 发送ID为1，命令为900的消息
    command_msg.ID = ID
    command_msg.command = Comand
    pub.publish(command_msg)
    rospy.loginfo("Sent command to motor %s with command %s" % (ID, Comand))



    # 保持节点运行一段时间，以便命令被处理
    rospy.sleep(0.2)
if __name__ == '__main__':

	for i in range(6):
		test_propeller_node(i,0)
	test_motor_node(1,0)
	test_motor_node(2,0)



