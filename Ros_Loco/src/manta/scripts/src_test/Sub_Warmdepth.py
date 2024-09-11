import rospy
from manta.msg import Warmdepth  # 导入自定义消息类型

def sensor_data_callback(data):
    rospy.loginfo(f"Received sensor data - Height: {data.height} meters, Depth: {data.depth} meters")

def sensor_data_listener():
    rospy.init_node('sensor_data_listener', anonymous=True)

    rospy.Subscriber('/sensor_data', Warmdepth, sensor_data_callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        sensor_data_listener()
    except rospy.ROSInterruptException:
        pass
